from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver


from state import AgentStateGraph
from agents import (
    fetch_user_info,
    query_agent,
    crm_agent,
    csm_agent,
    helpdesk_agent,
    chatdata_agent,
    insights_agent,
)


def route_query_agent(state: AgentStateGraph):
    last_message = state["messages"][-1]
    if not last_message.tool_calls:
        return "__end__"
    elif last_message.tool_calls[0]["name"] == "ToCSMAgent":
        return "csm_agent"
    elif last_message.tool_calls[0]["name"] == "ToCRMAgent":
        return "crm_agent"
    elif last_message.tool_calls[0]["name"] == "ToHelpDeskAgent":
        return "helpdesk_agent"
    elif last_message.tool_calls[0]["name"] == "ToChatDataAgent":
        return "chatdata_agent"


def create_graph():
    graph_builder = StateGraph(AgentStateGraph)

    graph_builder.add_node("fetch_user_info", fetch_user_info)
    graph_builder.add_node("query_agent", query_agent)
    graph_builder.add_node("crm_agent", crm_agent)
    graph_builder.add_node("csm_agent", csm_agent)
    graph_builder.add_node("helpdesk_agent", helpdesk_agent)
    graph_builder.add_node("chatdata_agent", chatdata_agent)
    graph_builder.add_node("insights_agent", insights_agent)

    graph_builder.add_edge(START, "fetch_user_info")
    graph_builder.add_edge("fetch_user_info", "query_agent")
    graph_builder.add_conditional_edges(
        "query_agent",
        route_query_agent,
        {
            "crm_agent": "crm_agent",
            "csm_agent": "csm_agent",
            "helpdesk_agent": "helpdesk_agent",
            "chatdata_agent": "chatdata_agent",
            "__end__": END,
        },
    )
    graph_builder.add_edge("crm_agent", "insights_agent")
    graph_builder.add_edge("csm_agent", "insights_agent")
    graph_builder.add_edge("helpdesk_agent", "insights_agent")
    graph_builder.add_edge("chatdata_agent", "insights_agent")
    graph_builder.add_edge("insights_agent", END)

    memory = MemorySaver()
    graph = graph_builder.compile(checkpointer=memory)

    return graph
