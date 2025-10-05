from typing import Any, List, Dict, Any, Optional
from langchain_core.messages import AnyMessage
from pydantic import BaseModel
import httpx, json, os
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from langserve import add_routes
app = FastAPI(
	title="LangChain Server",
	version="1.0",
	description="Spin up a simple api server using LangChain's Runnable interfaces",
)

# All claude models: https://docs.anthropic.com/en/docs/about-claude/models
from langchain_google_vertexai.model_garden import ChatAnthropicVertex
# Initialise the Model
model_config = {
	"project": "ksm-rch-sciscigpt",
	"location": "us-east5",
	"temperature": 0.0
}

llm_dict = {
	"claude-3.5": ChatAnthropicVertex(
		model_name="claude-3-5-sonnet-v2@20241022", max_output_tokens=8192, **model_config
	),
	"claude-3.7": ChatAnthropicVertex(
		model_name="claude-3-7-sonnet@20250219", max_output_tokens=8192 * 4, **model_config
	),
	"claude-4.0": ChatAnthropicVertex(
		model_name="claude-sonnet-4@20250514", max_output_tokens=8192 * 4, **model_config
	)
}

from agents.sciscigpt import AgentState, all_tools, all_specialists, define_sciscigpt_graph
for tool in all_tools:
    add_routes(app, tool, path=f"/tools/{tool.name}")

# from langchain.globals import set_debug
sciscigpt_graph = define_sciscigpt_graph(llm_dict)
sciscigpt = sciscigpt_graph.compile(debug=False)

class Input(BaseModel):
	messages_str: Optional[str]
	messages: Optional[List[AnyMessage]]
	metadata_str: Optional[str]
	metadata: Optional[Dict[str, Any]]
class Output(BaseModel):
	output: Any


from langchain_core.runnables import RunnableLambda
from func.messages import convert_to_langchain_messages, remove_bad_tool_call_responses
def node_sciscigpt(agent_state):
	agent_state["metadata"] = json.loads(agent_state["metadata_str"])

	agent_state["messages"] = remove_bad_tool_call_responses(convert_to_langchain_messages(
		agent_state["messages_str"], agent_state["metadata"]["format"]))
		
	return agent_state

from langchain_core.runnables.config import RunnableConfig
config = RunnableConfig(recursion_limit=500, run_name="SciSciGPT")

add_routes(
	app,
	RunnableLambda(node_sciscigpt) | sciscigpt.with_types(input_type=Input).with_config(config),
	path="/sciscigpt",
)


if __name__ == "__main__":
	import uvicorn
	uvicorn.run(app, host="0.0.0.0", port=8080)