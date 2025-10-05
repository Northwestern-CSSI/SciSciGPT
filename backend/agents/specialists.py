from pydantic import BaseModel, Field
from typing import Type
from langchain.tools import BaseTool
from tools import sql_list_table_tool, sql_get_schema_tool, sql_query_tool
from tools import python_jupyter_tool, r_jupyter_tool, julia_jupyter_tool
from tools import search_name_tool, search_literature_advanced_tool


class SpecialistInput(BaseModel):
	task: str = Field(..., description="""
The assigned task to the specialist. Needs to include: 
	1. A detailed execution plan of the task, including critical steps and key details.
	2. A thorough introduction of the data source to be used (if any, prioritize to provide file path rather than data content).
""")
	memory: bool = Field(..., description="""If True, the specialist will be able to see your previous interactions. If False, the specialist will start from the current task.""")


class DatabaseSpecialist(BaseTool):
	name: str = "database_specialist"
	description: str = """
	`database_specialist` is a specialized agent focused on scholarly data preparation and preprocessing. It helps with:
	1. Navigate complex scholarly databases
	2. Identify and extract relevant data segments
	3. Clean and transform data through preprocessing steps
	4. Conduct necessary data statistics and aggregation.
	Invoke this tool to assign a task to `database_specialist`.
	"""

	args_schema: Type[BaseModel] = SpecialistInput
	tools: list[BaseTool] = []
	def _run(self, task: str, memory: bool):
		return {"response": "Connected to DatabaseSpecialist:"}
	
class AnalyticsSpecialist(BaseTool):
	name: str = "analytics_specialist"
	description: str = """
	`analytics_specialist` is a specialized agent focused on data analysis and visualization tasks. It helps with:
	1. Designing and implementing analytical approaches (statistical analysis, modeling, etc.)
	2. Creating data visualizations and plots
	3. Writing and executing analysis code in Python/R/Julia
	
	Important notes:
	- Does not directly access data - requires data source references (paths, query results, etc.)
	- Works with data provided by database_specialist
	- Focuses on analysis strategy and implementation, not data retrieval
	
	Invoke this tool to assign analytical tasks to `analytics_specialist`.
	"""
	args_schema: Type[BaseModel] = SpecialistInput
	tools: list[BaseTool] = []
	def _run(self, task: str, memory: bool):
		return {"response": "Connected to AnalyticsSpecialist:"}
	
class LiteratureSpecialist(BaseTool):
	name: str = "literature_specialist"
	description: str = """
	`literature_specialist` is a specialized agent focused on literature understanding Science of Science literature. It helps with:
	1. Locating and retrieving relevant papers from the Science of Science literature
	2. Extracting key methodological approaches and findings from papers
	3. Highlighting implications and applications of existing Science of Science research
	Call this agent when the user explicitly asks for the Science of Science literature.
	Invoke this tool to assign a task to `literature_specialist`.
	"""
	args_schema: Type[BaseModel] = SpecialistInput
	tools: list[BaseTool] = []
	def _run(self, task: str, memory: bool):
		return {"response": "Connected to LiteratureSpecialist:"}
	
class EvaluationSpecialist(BaseTool):
	name: str = "evaluation_specialist"
	description: str = "After finish the task, call this tool. It will help to comprehensively evaluate the task and generate an execution report."
	tools: list[BaseTool] = []
	def _run(self):
		return {"response": "Evaluation Specialist: Evaluating the task."}
	
database_specialist = DatabaseSpecialist(tools=[sql_list_table_tool, sql_get_schema_tool, sql_query_tool, search_name_tool])
analytics_specialist = AnalyticsSpecialist(tools=[python_jupyter_tool, r_jupyter_tool, julia_jupyter_tool])
literature_specialist = LiteratureSpecialist(tools=[search_literature_advanced_tool])
evaluation_specialist = EvaluationSpecialist(tools=[])

__all__ = [database_specialist, analytics_specialist, literature_specialist, evaluation_specialist]