from langchain_openai import ChatOpenAI
from langchain_core.runnables.config import RunnableConfig
from langchain_core.messages import ToolMessage
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

    response = query_agent_runnable.invoke(
        {"messages": state["messages"], "user_info": state["user_info"]}
    )

    return {**state, "messages": response}


def crm_agent(state: AgentStateGraph):
    # Append a tool message to the last route from query agent
    last_tool_call_id = state["messages"][-1].tool_calls[0]["id"]
    query_route_tool_message = ToolMessage(
        tool_call_id=last_tool_call_id,
        content="The CRM Agent will now look for information in the CRM data.",
    )
    state["messages"].append(query_route_tool_message)

    # crm_agent_tools = []
    crm_llm_with_tools = llm
    crm_agent_runnable = crm_agent_prompt_template | crm_llm_with_tools
    response = crm_agent_runnable.invoke(state)

    return {**state, "messages": response, "crm_agent_response": response}


def csm_agent(state: AgentStateGraph):
    # Append a tool message for the last route from query agent
    last_tool_call_id = state["messages"][-1].tool_calls[0]["id"]
    query_route_tool_message = ToolMessage(
        tool_call_id=last_tool_call_id,
        content="The CSM agent will now look for necessary information.",
    )
    state["messages"].append(query_route_tool_message)

    # csm_agent_tools = []
    csm_llm_with_tools = llm
    csm_agent_runnable = csm_agent_prompt_template | csm_llm_with_tools
    response = csm_agent_runnable.invoke(state)

    return {**state, "messages": response, "csm_agent_response": response}


def helpdesk_agent(state: AgentStateGraph):
    # Append a tool message to the last route from query agent
    last_tool_call_id = state["messages"][-1].tool_calls[0]["id"]
    query_route_tool_message = ToolMessage(
        tool_call_id=last_tool_call_id,
        content="The Help Desk Agent will now look for necessary information",
    )
    state["messages"].append(query_route_tool_message)

    # helpdesk_agent_tools = []
    helpdesk_llm_with_tools = llm
    helpdesk_agent_runnable = helpdesk_agent_prompt_template | helpdesk_llm_with_tools
    response = helpdesk_agent_runnable.invoke(state)

    return {**state, "messages": response, "helpdesk_agent_response": response}


def chatdata_agent(state: AgentStateGraph):
    # Append a tool message to the last route from query agent
    last_tool_call_id = state["messages"][-1].tool_calls[0]["id"]
    query_route_tool_message = ToolMessage(
        tool_call_id=last_tool_call_id,
        content="The Chat Data Agent will now look for necessary information",
    )
    state["messages"].append(query_route_tool_message)

    # chatdata_agent_tools = []
    chatdata_llm_with_tools = llm
    chatdata_agent_runnable = chatdata_agent_prompt_template | chatdata_llm_with_tools
    response = chatdata_agent_runnable.invoke(state)

    return {**state, "messages": response, "chatdata_agent_response": response}


def insights_agent(state: AgentStateGraph):
    # insights_agent_tools = []
    insights_llm_with_tools = llm
    insights_agent_runnable = insights_agent_prompt_template | insights_llm_with_tools
    response = insights_agent_runnable.invoke(
        {
            "crm_agent_response": state.get("crm_agent_response", ""),
            "csm_agent_response": state.get("csm_agent_response", ""),
            "helpdesk_agent_response": state.get("helpdesk_agent_response", ""),
            "chatdata_agent_response": state.get("chatdata_agent_response", ""),
            "message": state["messages"],
        }
    )

    return {**state, "messages": response}
