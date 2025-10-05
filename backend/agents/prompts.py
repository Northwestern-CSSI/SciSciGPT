from langchain.hub import pull

tool_eval_prompt = pull("erzhuoshao/sciscigpt-tool-eval:3452c5e1")
visual_eval_prompt = pull("erzhuoshao/sciscigpt-visual-eval:4be9277a")
task_eval_prompt = pull("erzhuoshao/sciscigpt-task-eval:7d5d09e8")

research_manager_prompt = pull("erzhuoshao/sciscigpt_research_manager:1e49a915")

specialist_prompt_dict = {
    "literature_specialist": pull("erzhuoshao/sciscigpt_literature_specialist:93d1f28f"),
    "database_specialist": pull("erzhuoshao/sciscigpt_database_specialist:b8fb5bcb"),
    "analytics_specialist": pull("erzhuoshao/sciscigpt_analytics_specialist:30738185"),
}