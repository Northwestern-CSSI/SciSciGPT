import asyncio
import time
import uuid
import re
import threading
from queue import Empty
from typing import Dict, Optional, List, Any, AsyncIterator

from jupyter_client import KernelManager
try:
    # 新版 jupyter_client 直接导出 AsyncKernelClient
    from jupyter_client import AsyncKernelClient
except Exception:
    # 旧版兼容路径
    from jupyter_client.asynchronous.client import AsyncKernelClient

from IPython.core.ultratb import FormattedTB


class JupyterSandbox:
    """
    Unified sync/async Jupyter kernel sandbox.
    One kernel per session; both BlockingKernelClient (sync)
    and AsyncKernelClient (async) attach to the same connection.
    """

    def __init__(self, working_dir: str, kernel_name: Optional[str] = None):
        self.working_dir = working_dir
        self.kernel_name = kernel_name
        # sessions[session_id] = {
        #   "km": KernelManager, "kc": BlockingKernelClient|None,
        #   "akc": AsyncKernelClient|None, "initialized": bool,
        #   "last_used": float, "tlock": threading.RLock, "alock": asyncio.Lock
        # }
        self.sessions: Dict[str, Dict[str, Any]] = {}
        self.tb_formatter = FormattedTB(mode="Plain")

    # ---------------------- internals ----------------------

    def _ansi_strip(self, s: str) -> str:
        ansi = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
        return ansi.sub("", s)

    def _format_traceback(self, tb_list: List[str]) -> str:
        return "\n".join(self._ansi_strip(line) for line in tb_list)

    def _sanitize_path(self, p: str) -> str:
        return p.replace("\\", "\\\\").replace("'", "\\'")

    def _ensure_session_struct(self, session_id: str) -> Dict[str, Any]:
        sess = self.sessions.get(session_id)
        if not sess:
            sess = {
                "km": KernelManager(kernel_name=self.kernel_name) if self.kernel_name else KernelManager(),
                "kc": None,
                "akc": None,
                "initialized": False,
                "last_used": time.monotonic(),
                "tlock": threading.RLock(),
                "alock": asyncio.Lock(),
            }
            self.sessions[session_id] = sess
        else:
            sess["last_used"] = time.monotonic()
        return sess

    # ---------------------- kernel bring-up ----------------------

    def _start_kernel_blocking(self, sess: Dict[str, Any]) -> None:
        """Start kernel if not started (blocking)."""
        km = sess["km"]
        if not km.is_alive():
            km.start_kernel()

    async def _start_kernel_async(self, sess: Dict[str, Any]) -> None:
        """Start kernel if not started, but offload blocking start to a thread."""
        km = sess["km"]
        if not km.is_alive():
            await asyncio.to_thread(km.start_kernel)

    def _ensure_blocking_client_ready(self, sess: Dict[str, Any], timeout: float = 60.0) -> None:
        """Create & ready BlockingKernelClient if needed."""
        if sess["kc"] is None:
            kc = sess["km"].client()  # BlockingKernelClient
            kc.start_channels()
            kc.wait_for_ready(timeout=timeout)
            sess["kc"] = kc

    async def _ensure_async_client_ready(self, sess: Dict[str, Any], timeout: float = 60.0) -> None:
        """Create & ready AsyncKernelClient if needed by loading the same connection info."""
        if sess["akc"] is None:
            info = sess["km"].get_connection_info()  # same connection for both clients
            akc = AsyncKernelClient()
            akc.load_connection_info(info)
            akc.start_channels()
            await akc.wait_for_ready(timeout=timeout)
            sess["akc"] = akc

    def _init_once_sync(self, sess: Dict[str, Any]) -> None:
        if sess["initialized"]:
            return
        kc = sess["kc"]
        # best-effort init; ignore failures to keep kernel usable
        try:
            for code in [
                "%load_ext rpy2.ipython",
                "from juliacall import Main as jl",
                f"import os; os.chdir('{self._sanitize_path(self.working_dir)}')",
            ]:
                msg_id = kc.execute(code)
                # drain until idle for this msg_id
                while True:
                    msg = kc.get_iopub_msg(timeout=2)
                    if msg.get("parent_header", {}).get("msg_id") != msg_id:
                        continue
                    if msg["header"]["msg_type"] == "status" and msg["content"].get("execution_state") == "idle":
                        break
        except Exception:
            pass
        finally:
            sess["initialized"] = True

    async def _init_once_async(self, sess: Dict[str, Any]) -> None:
        if sess["initialized"]:
            return
        akc = sess["akc"]
        try:
            for code in [
                "%load_ext rpy2.ipython",
                "from juliacall import Main as jl",
                f"import os; os.chdir('{self._sanitize_path(self.working_dir)}')",
            ]:
                msg_id = akc.execute(code)
                while True:
                    try:
                        msg = await akc.get_iopub_msg(timeout=2)
                    except Empty:
                        continue
                    if msg.get("parent_header", {}).get("msg_id") != msg_id:
                        continue
                    if msg["header"]["msg_type"] == "status" and msg["content"].get("execution_state") == "idle":
                        break
        except Exception:
            pass
        finally:
            sess["initialized"] = True

    # ---------------------- sync API ----------------------

    def get_or_create_session(self, session_id: str) -> Dict[str, Any]:
        """Sync: ensure session with a started kernel & blocking client."""
        sess = self._ensure_session_struct(session_id)
        with sess["tlock"]:
            self._start_kernel_blocking(sess)
            self._ensure_blocking_client_ready(sess)
            self._init_once_sync(sess)
        return sess

    def execute_code(
        self, code: str, session_id: str, cell_id: str, timeout: int = 120
    ) -> List[Dict[str, Any]]:
        """Sync execute; returns a list of outputs."""
        sess = self.get_or_create_session(session_id)
        kc = sess["kc"]

        outputs: List[Dict[str, Any]] = []
        deadline = time.monotonic() + float(timeout)

        msg_id = kc.execute(code)
        while True:
            if time.monotonic() > deadline:
                outputs.append({"type": "text", "text": f"Execution timeout after {timeout} seconds"})
                break
            try:
                msg = kc.get_iopub_msg(timeout=1.0)
            except Empty:
                continue
            if msg.get("parent_header", {}).get("msg_id") != msg_id:
                continue

            mtype = msg["header"]["msg_type"]
            content = msg["content"]

            if mtype == "stream":
                outputs.append({"type": "text", "text": content.get("text", "")})

            elif mtype == "execute_result":
                data = content.get("data", {})
                outputs.append({"type": "text", "text": str(data.get("text/plain", ""))})

            elif mtype == "display_data":
                data = content.get("data", {})
                if "image/png" in data:
                    img = data["image/png"]
                    if not str(img).startswith("data:image/png;base64,"):
                        img = "data:image/png;base64," + img
                    outputs.append({"type": "image_url", "image_url": {"url": img}})
                elif "image/jpeg" in data:
                    img = data["image/jpeg"]
                    if not str(img).startswith("data:image/jpeg;base64,"):
                        img = "data:image/jpeg;base64," + img
                    outputs.append({"type": "image_url", "image_url": {"url": img}})
                elif "text/plain" in data:
                    outputs.append({"type": "text", "text": data["text/plain"]})

            elif mtype == "error":
                outputs.append({"type": "text", "text": self._format_traceback(content.get("traceback", []))})

            elif mtype == "status" and content.get("execution_state") == "idle":
                break

        for o in outputs:
            o["cell_id"] = cell_id
            o["session_id"] = session_id
        return outputs

    def close_session(self, session_id: str) -> None:
        """Sync close: stop channels and shutdown kernel."""
        sess = self.sessions.get(session_id)
        if not sess:
            return
        with sess["tlock"]:
            try:
                if sess.get("kc") is not None:
                    sess["kc"].stop_channels()
                if sess.get("akc") is not None:
                    # Async client也有 stop_channels；在同步上下文直接调用即可
                    sess["akc"].stop_channels()
            finally:
                try:
                    sess["km"].shutdown_kernel(now=True)
                finally:
                    self.sessions.pop(session_id, None)

    def close_all_sessions(self) -> None:
        for sid in list(self.sessions.keys()):
            self.close_session(sid)

    def cleanup_inactive_sessions(self, max_idle_time: int = 3600) -> None:
        now = time.monotonic()
        for sid, s in list(self.sessions.items()):
            if now - s["last_used"] > max_idle_time:
                self.close_session(sid)

    # ---------------------- async API ----------------------

    async def aget_or_create_session(self, session_id: str) -> Dict[str, Any]:
        """Async: ensure session with started kernel & async client."""
        sess = self._ensure_session_struct(session_id)
        async with sess["alock"]:
            await self._start_kernel_async(sess)
            await self._ensure_async_client_ready(sess)
            await self._init_once_async(sess)
        return sess

    async def aexecute_code(
        self, code: str, session_id: str, cell_id: str, timeout: int = 120
    ) -> List[Dict[str, Any]]:
        """Async execute; returns a list of outputs."""
        sess = await self.aget_or_create_session(session_id)
        akc = sess["akc"]

        outputs: List[Dict[str, Any]] = []
        deadline = time.monotonic() + float(timeout)

        msg_id = akc.execute(code)
        while True:
            if time.monotonic() > deadline:
                outputs.append({"type": "text", "text": f"Execution timeout after {timeout} seconds"})
                break
            try:
                msg = await akc.get_iopub_msg(timeout=1.0)
            except Empty:
                continue
            if msg.get("parent_header", {}).get("msg_id") != msg_id:
                continue

            mtype = msg["header"]["msg_type"]
            content = msg["content"]

            if mtype == "stream":
                outputs.append({"type": "text", "text": content.get("text", "")})

            elif mtype == "execute_result":
                data = content.get("data", {})
                outputs.append({"type": "text", "text": str(data.get("text/plain", ""))})

            elif mtype == "display_data":
                data = content.get("data", {})
                if "image/png" in data:
                    img = data["image/png"]
                    if not str(img).startswith("data:image/png;base64,"):
                        img = "data:image/png;base64," + img
                    outputs.append({"type": "image_url", "image_url": {"url": img}})
                elif "image/jpeg" in data:
                    img = data["image/jpeg"]
                    if not str(img).startswith("data:image/jpeg;base64,"):
                        img = "data:image/jpeg;base64," + img
                    outputs.append({"type": "image_url", "image_url": {"url": img}})
                elif "text/plain" in data:
                    outputs.append({"type": "text", "text": data["text/plain"]})

            elif mtype == "error":
                outputs.append({"type": "text", "text": self._format_traceback(content.get("traceback", []))})

            elif mtype == "status" and content.get("execution_state") == "idle":
                break

        for o in outputs:
            o["cell_id"] = cell_id
            o["session_id"] = session_id
        return outputs

    async def astream_execute_code(
        self, code: str, session_id: str, cell_id: str, timeout: int = 120
    ) -> AsyncIterator[Dict[str, Any]]:
        """Async streaming variant: yields outputs incrementally."""
        sess = await self.aget_or_create_session(session_id)
        akc = sess["akc"]
        deadline = time.monotonic() + float(timeout)

        msg_id = akc.execute(code)
        while True:
            if time.monotonic() > deadline:
                yield {"type": "text", "text": f"Execution timeout after {timeout} seconds",
                       "cell_id": cell_id, "session_id": session_id}
                break
            try:
                msg = await akc.get_iopub_msg(timeout=1.0)
            except Empty:
                continue
            if msg.get("parent_header", {}).get("msg_id") != msg_id:
                continue

            mtype = msg["header"]["msg_type"]
            content = msg["content"]

            if mtype == "stream":
                yield {"type": "text", "text": content.get("text", ""),
                       "cell_id": cell_id, "session_id": session_id}

            elif mtype == "execute_result":
                data = content.get("data", {})
                yield {"type": "text", "text": str(data.get("text/plain", "")),
                       "cell_id": cell_id, "session_id": session_id}

            elif mtype == "display_data":
                data = content.get("data", {})
                if "image/png" in data:
                    img = data["image/png"]
                    if not str(img).startswith("data:image/png;base64,"):
                        img = "data:image/png;base64," + img
                    yield {"type": "image_url", "image_url": {"url": img},
                           "cell_id": cell_id, "session_id": session_id}
                elif "image/jpeg" in data:
                    img = data["image/jpeg"]
                    if not str(img).startswith("data:image/jpeg;base64,"):
                        img = "data:image/jpeg;base64," + img
                    yield {"type": "image_url", "image_url": {"url": img},
                           "cell_id": cell_id, "session_id": session_id}
                elif "text/plain" in data:
                    yield {"type": "text", "text": data["text/plain"],
                           "cell_id": cell_id, "session_id": session_id}

            elif mtype == "error":
                yield {"type": "text", "text": self._format_traceback(content.get("traceback", [])),
                       "cell_id": cell_id, "session_id": session_id}

            elif mtype == "status" and content.get("execution_state") == "idle":
                break

    async def aclose_session(self, session_id: str) -> None:
        """Async close: stop channels and shutdown kernel without blocking the loop."""
        sess = self.sessions.get(session_id)
        if not sess:
            return
        async with sess["alock"]:
            try:
                if sess.get("kc") is not None:
                    sess["kc"].stop_channels()
                if sess.get("akc") is not None:
                    sess["akc"].stop_channels()
            finally:
                try:
                    await asyncio.to_thread(sess["km"].shutdown_kernel, True)
                finally:
                    self.sessions.pop(session_id, None)

    async def aclose_all_sessions(self) -> None:
        for sid in list(self.sessions.keys()):
            await self.aclose_session(sid)

    async def acleanup_inactive_sessions(self, max_idle_time: int = 3600) -> None:
        now = time.monotonic()
        stale = [sid for sid, s in self.sessions.items() if now - s["last_used"] > max_idle_time]
        for sid in stale:
            await self.aclose_session(sid)
