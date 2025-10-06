import uuid, re
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, AnyMessage
import json
from typing import Literal, List

from langchain_core.load import dumps, loads
import os


def convert_to_langchain_messages(data, format: Literal["events", "messages"]) -> List[AnyMessage]:
	if format == "events":
		messages = []
		for event_str in loads(data):
			output = loads(loads(event_str)["data"])
			
			for message in output["messages"]:
				message.metadata = { "current": output.get("current", None), "next": output.get("next", None), "name": output.get("name", None) }
				messages.append(message)

		return messages

	else:
		messages = loads(data)
		if isinstance(messages[0], (HumanMessage, AIMessage, ToolMessage)):
			return messages
		else:
			messages = [loads(message) for message in messages]
			return messages


import json
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

def display_message(message):
	# ANSI color codes
	BLUE = '\033[94m'
	GREEN = '\033[92m'
	YELLOW = '\033[93m'
	RED = '\033[91m'
	PURPLE = '\033[95m'
	BOLD = '\033[1m'
	ENDC = '\033[0m'
	
	if isinstance(message, AIMessage):
		content = message.content
		print(f"{BLUE}{BOLD}AI Message:{ENDC}")
		if type(content) == str:
			print(f"{BLUE}{content}{ENDC}")
		else:
			for i in content:
				if i["type"] == "text":
					print(f"{BLUE}{i['text']}{ENDC}")

		if message.tool_calls:
			print(f"\n{YELLOW}{BOLD}Tool Calls:{ENDC}")
			print(f"{YELLOW}{BOLD}name:{ENDC} {YELLOW}{message.tool_calls[0]['name']}{ENDC}")
			print(f"{YELLOW}{BOLD}args:{ENDC} {YELLOW}{message.tool_calls[0]['args']}{ENDC}")
		print("\n")

	elif isinstance(message, ToolMessage):
		content = message.content
		if not isinstance(content, str):
			content = content[0]['text']
		else:
			content = content

		print(f"{PURPLE}{BOLD}Tool Response:{ENDC}")
		print(f"{PURPLE}{eval(content)['response']}{ENDC}")
		print("\n")
		
	elif isinstance(message, HumanMessage):
		content = message.content
		print(f"{GREEN}{BOLD}Human Message:{ENDC}")
		print(f"{GREEN}{content}{ENDC}")
		print("\n")




from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, SystemMessage, AnyMessage
import json
from copy import deepcopy
def reformat_messages(messages: list[AnyMessage]):
	# If the last message is an AIMessage, reformat the messages
	# by adding the content of the last message to the second last message (ToolMessage)
	messages = deepcopy(messages)
	if isinstance(messages[-1], AIMessage):
		message_0_content = messages[-1].content
		message_0_content = [{"type": "text", "text": message_0_content}] if isinstance(message_0_content, str) else message_0_content
		message_1_content = messages[-2].content
		message_1_content = [{"type": "text", "text": message_1_content}] if isinstance(message_1_content, str) else message_1_content
		content = message_1_content + message_0_content
		content = [{"type": "text", "text": i['text']} for i in content]
		
		temp_message = deepcopy(messages[-2])
		temp_message.content = content
		messages[-2] = temp_message
		return messages[:-1]
	else:
		return messages


def to_human_message(message: AnyMessage):
	return HumanMessage(content=message.content)


def system_to_human(messages: list[AnyMessage]):
	# If the message is a SystemMessage, convert it to a HumanMessage
	human_messages = []
	for message in messages:
		if isinstance(message, SystemMessage):
			human_messages.append(HumanMessage(content=message.content))
		else:
			human_messages.append(message)
	return human_messages



	

from langchain_core.messages import HumanMessage, AIMessage, AnyMessage
from copy import deepcopy
import re
def remove_inner_monologue(messages: list[AnyMessage], monologue_tags: list[str]):
	messages = deepcopy(messages)
	
	for tag in monologue_tags:
		pattern = re.compile(fr'<{tag}>(.*?)</{tag}>', re.DOTALL)
		for message in messages:
			if isinstance(message, AIMessage):
				message.content = pattern.sub("", message.text()).strip()

	return messages



def remove_bad_tool_call_responses(messages: list[AnyMessage]):
	messages = deepcopy(messages)

	all_tool_calls = []
	all_tool_responses = []

	for message in messages:
		if isinstance(message, ToolMessage):
			all_tool_responses.append(message)
		elif isinstance(message, AIMessage):
			if message.tool_calls:
				all_tool_calls.extend(message.tool_calls)

	all_tool_call_ids = set([call["id"] for call in all_tool_calls])
	all_tool_response_ids = set([response.tool_call_id for response in all_tool_responses])

	# remove tool calls that are not in the response and all responses that are not in the tool call
	to_be_removed = (all_tool_call_ids - all_tool_response_ids) | (all_tool_response_ids - all_tool_call_ids)

	messages_2 = []
	for message in messages:
		if isinstance(message, ToolMessage):
			if message.tool_call_id not in to_be_removed:
				messages_2.append(message)

		elif isinstance(message, AIMessage):
			if message.tool_calls:
				message.tool_calls = [call for call in message.tool_calls if call["id"] not in to_be_removed]
			messages_2.append(message)

		else:
			messages_2.append(message)

	return messages_2