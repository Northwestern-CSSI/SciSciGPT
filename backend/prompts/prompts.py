from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.hub import pull


HyDE_pre_retrieval_xml = pull("erzhuoshao/sciscigpt_literature_specialist_hyde_pre")
HyDE_post_retrieval_xml = pull("erzhuoshao/sciscigpt_literature_specialist_hyde_post")


sql_query_tool_description_2 = """
Function: Executes a SQL query on Google BigQuery.
Output:
1. The header of the result table (top 10 rows). 
2. The file path where the complete result is stored.
Dependencies:
1. Use `sql_get_schema` and `sql_list_table` to retrieve the schema of relevant tables (if necessary).
2. Use `search_name` for accurate name matching if needed (if necessary).

Note: 
1. Ensure your query is well-formed
2. Ensure all tables and columns actually exist in the database

Custom functions:
`SciSciNet_US_V5.TEXT_EMBEDDING` is defined to convert text to embeddings.
`VECTOR_SEARCH` is defined to perform similarity search (Note that the result sub-table is named as `base`).

Example query:
```sql
-- Get papers that are relevant to the search query
SELECT
  vs.base.*, vs.distance
FROM VECTOR_SEARCH(
  TABLE SciSciNet_US_V5.papers,
  "abstract_embedding",
  (SELECT SciSciNet_US_V5.TEXT_EMBEDDING('YOUR SEARCH QUERY')), 
  top_k => NUMBER_OF_RESULTS
) vs
```"""