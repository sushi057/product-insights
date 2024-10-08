from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableConfig

from state import AgentStateGraph
from tools import ToCRMAgent, ToChatDataAgent, ToCSMAgent, ToHelpDeskAgent
from prompts import (
    query_agent_prompt_template,
    crm_agent_prompt_template,
    csm_agent_prompt_template,
    helpdesk_agent_prompt_template,
    chatdata_agent_prompt_template,
    insights_agent_prompt_template,
)

llm = ChatOpenAI(model="gpt-4o")


class Agent:
    def __init__(self, state: AgentStateGraph, llm):
        self.state = state
        self.llm = ChatOpenAI(model="gpt-4o")


def fetch_user_info(config: RunnableConfig):
    # configurable = config.get("configurable")
    # user_id = configurable["user_id"]

    # fetch user_info for user_id
    user_info = {}

    return {"user_info": user_info}


def query_agent(state: AgentStateGraph):
    query_agent_tools = [ToCRMAgent, ToCSMAgent, ToChatDataAgent, ToHelpDeskAgent]
    query_llm_with_tools = llm.bind_tools(query_agent_tools)

    query_agent_runnable = query_agent_prompt_template | query_llm_with_tools

    response = query_agent_runnable.invoke({"messages": state["messages"]})

    return {**state, "messages": response}
