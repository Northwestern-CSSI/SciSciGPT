##### Data Extraction Tools
from tools.sql import SQLListTableTool, SQLGetSchemaTool, SQLQueryTool
from langchain_community.utilities import SQLDatabase
import os


from dotenv import load_dotenv
load_dotenv()

bigquery_uri = os.getenv("GOOGLE_BIGQUERY_URI")
db_name = bigquery_uri.split("/")[-1]
# Initialize tools
db_dict = {
	db_name: SQLDatabase.from_uri(
		database_uri=bigquery_uri, 
		sample_rows_in_table_info=0, 
	)
}

sql_list_table_tool = SQLListTableTool(db_dict=db_dict)
sql_get_schema_tool = SQLGetSchemaTool(db_dict=db_dict)
sql_query_tool = SQLQueryTool(db_dict=db_dict)

from tools.name import search_name_tool

##### Data Analysis Tools
from tools.sandbox import python_jupyter_tool, r_jupyter_tool, julia_jupyter_tool

##### Literature Review
from tools.literature import search_literature_advanced_tool

tools = [
    sql_list_table_tool, sql_get_schema_tool, sql_query_tool, 
    search_name_tool, 
	python_jupyter_tool, r_jupyter_tool, julia_jupyter_tool,
    search_literature_advanced_tool
]

enabled_tools = [
    sql_list_table_tool, sql_get_schema_tool, sql_query_tool, search_name_tool,
    python_jupyter_tool, r_jupyter_tool, julia_jupyter_tool, 
    search_literature_advanced_tool
]