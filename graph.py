from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver


from state import AgentStateGraph
from agents import fetch_user_info, query_agent


def create_graph():
    graph_builder = StateGraph(AgentStateGraph)

    graph_builder.add_node("fetch_user_info", fetch_user_info)
    graph_builder.add_node("query_agent", query_agent)

    graph_builder.add_edge(START, "fetch_user_info")
    graph_builder.add_edge("fetch_user_info", "query_agent")
    graph_builder.add_edge("query_agent", END)

    memory = MemorySaver()
    graph = graph_builder.compile(checkpointer=memory)
    return graph
