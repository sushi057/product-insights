from langchain_openai import ChatOpenAI
from langchain_core.runnables.config import RunnableConfig

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


# class Agent:
#     def __init__(self, state: AgentStateGraph, llm):
#         self.state = state
#         self.llm = ChatOpenAI(model="gpt-4o")


def fetch_user_info(state: AgentStateGraph, config: RunnableConfig):
    # configurable = config.get("configurable")
    # user_id = configurable["user_id"]

    # fetch user_info for user_id
    user_info = {
        "user_id": "123",
        "organization_id": "123",
        "zendesk_id": "123",
        "hubspot_id": "123",
        "churnzero_id": "123",
        "salesforce_id": "123",
    }

    return {"user_info": user_info}


def query_agent(state: AgentStateGraph):
    query_agent_tools = [ToCRMAgent, ToCSMAgent, ToChatDataAgent, ToHelpDeskAgent]
    query_llm_with_tools = llm.bind_tools(query_agent_tools)

    query_agent_runnable = query_agent_prompt_template | query_llm_with_tools

    response = query_agent_runnable.invoke(state)

    return {**state, "messages": response}


def crm_agent(state: AgentStateGraph):
    crm_agent_tools = []
    crm_llm_with_tools = llm.bind_tools(crm_agent_tools)

    crm_agent_runnable = crm_agent_prompt_template | crm_llm_with_tools

    response = crm_agent_runnable.invoke(state)

    return {**state, "crm_agent_response": response}


def csm_agent(state: AgentStateGraph):
    csm_agent_tools = []
    csm_llm_with_tools = llm.bind_tools(csm_agent_tools)

    csm_agent_runnable = csm_agent_prompt_template | csm_llm_with_tools

    response = csm_agent_runnable.invoke(state)

    return {**state, "csm_agent_response": response}


def helpdesk_agent(state: AgentStateGraph):
    helpdesk_agent_tools = []
    helpdesk_llm_with_tools = llm.bind_tools(helpdesk_agent_tools)

    helpdesk_agent_runnable = helpdesk_agent_prompt_template | helpdesk_llm_with_tools

    response = helpdesk_agent_runnable.invoke(state)

    return {**state, "helpdesk_agent_response": response}


def chatdata_agent(state: AgentStateGraph):
    chatdata_agent_tools = []
    chatdata_llm_with_tools = llm.bind_tools(chatdata_agent_tools)

    chatdata_agent_runnable = chatdata_agent_prompt_template | chatdata_llm_with_tools

    response = chatdata_agent_runnable.invoke(state)

    return {**state, "chatdata_agent_response": response}


def insights_agent(state: AgentStateGraph):
    insights_agent_tools = []
    insights_llm_with_tools = llm.bind_tools(insights_agent_tools)

    insights_agent_runnable = insights_agent_prompt_template | insights_llm_with_tools

    response = insights_agent_runnable.invoke(state)

    return {**state, "messages": response}
