# Visualize graph
def visualize_graph(graph):
    with open("graph.png", "wb") as f:
        f.write(graph.get_graph(xray=True).draw_mermaid_png())
