from typing import Literal
from langgraph.graph import END, START, StateGraph
from functools import partial
from agents.nodes import call_research_manager, call_specialist, call_toolset, call_specialistset, AgentState
from agents.evaluation import call_evaluation


def select_next(state: AgentState, verbose: bool = False) -> Literal[
	"node_research_manager", "node_database_specialist", "node_analytics_specialist", "node_literature_specialist", 
	"node_evaluation_specialist", "node_specialistset", "node_toolset", END]:

	current, next = state["current"], state["next"]
	return next.split(":")[0]

from agents.specialists import database_specialist as DS
from agents.specialists import analytics_specialist as AS
from agents.specialists import literature_specialist as LS
from agents.specialists import evaluation_specialist as ES

all_tools = [ *DS.tools, *AS.tools, *LS.tools, *ES.tools ]
all_specialists = [DS, AS, LS, ES]


from agents.utils.messages import _remove_xml_tags_from_messages
pruning_func = partial(_remove_xml_tags_from_messages, tags=["thinking"])
identity_func = lambda x: x


def define_sciscigpt_graph(llm_dict):
	node_research_manager = partial(
		call_research_manager, llm_dict, [DS, AS, LS], pruning_func)

	# Allowing all specialists to see the full workflow
	node_database_specialist = partial(call_specialist, llm_dict, DS.tools + [ES], identity_func)
	node_analytics_specialist = partial(call_specialist, llm_dict, AS.tools + [ES], identity_func)
	node_literature_specialist = partial(call_specialist, llm_dict, LS.tools + [ES], identity_func)
	node_evaluation_specialist = partial(call_evaluation, llm_dict, [DS, AS, LS], identity_func)

	node_specialistset = partial(call_specialistset, [DS, AS, LS])
	node_toolset = partial(call_toolset, [ *DS.tools, *AS.tools, *LS.tools ])

	sciscigpt_graph = StateGraph(AgentState)
	sciscigpt_graph.add_node("node_research_manager", node_research_manager)
	sciscigpt_graph.add_node("node_database_specialist", node_database_specialist)
	sciscigpt_graph.add_node("node_analytics_specialist", node_analytics_specialist)
	sciscigpt_graph.add_node("node_literature_specialist", node_literature_specialist)
	sciscigpt_graph.add_node("node_evaluation_specialist", node_evaluation_specialist)
	sciscigpt_graph.add_node("node_specialistset", node_specialistset)
	sciscigpt_graph.add_node("node_toolset", node_toolset)

	sciscigpt_graph.add_edge(START, "node_research_manager")
	sciscigpt_graph.add_conditional_edges("node_research_manager", select_next)
	sciscigpt_graph.add_conditional_edges("node_database_specialist", select_next)
	sciscigpt_graph.add_conditional_edges("node_analytics_specialist", select_next)
	sciscigpt_graph.add_conditional_edges("node_literature_specialist", select_next)
	sciscigpt_graph.add_conditional_edges("node_evaluation_specialist", select_next)
	sciscigpt_graph.add_conditional_edges("node_specialistset", select_next)
	sciscigpt_graph.add_conditional_edges("node_toolset", select_next)

	return sciscigpt_graph


__all__ = [
	"AgentState", "all_tools", "all_specialists", "define_sciscigpt_graph"
]