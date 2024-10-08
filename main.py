import uuid

from graph import create_graph
from utils import visualize_graph

graph = create_graph()


# Visualize Graph
visualize_graph(graph)

thread_id = str(uuid.uuid4())

config = {"configurable": {"thread_id": thread_id}}

while True:
    user_input = input("User: ")

    if user_input in ["q", "quit", "exit"]:
        print("goodbye")
        break

    for event in graph.stream({"messages": ("user", user_input)}, stream_mode="values"):
        event["messages"][-1].pretty_print()
