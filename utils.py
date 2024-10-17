from langchain_core.runnables import RunnableLambda
from langgraph.prebuilt import ToolNode
from langchain_core.messages import ToolMessage


def handle_tool_error(state) -> dict:
    """
    Handle tool error and return a dictionary containing error messages.

    Args:
        state: A dictionary representing the state of the tool.

    Returns:
        A dictionary containing error messages.

    """
    error = state.get("error")
    tool_calls = state["messages"][-1].tool_calls
    return {
        "messages": [
            ToolMessage(
                content=f"Error: {repr(error)}\n please fix your mistakes.",
                tool_call_id=tc["id"],
            )
            for tc in tool_calls
        ]
    }


# Visualize graph
def visualize_graph(graph):
    with open("graph.png", "wb") as f:
        f.write(graph.get_graph(xray=True).draw_mermaid_png())


def create_tool_node_with_fallback(tools: list) -> dict:
    """
    Creates a tool node with fallbacks.

    Args:
        tools (list): A list of tools.

    Returns:
        dict: The tool node with fallbacks.
    """
    return ToolNode(tools).with_fallbacks(
        [RunnableLambda(handle_tool_error)], exception_key="error"
    )
