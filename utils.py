# Visualize graph


def visualize_graph(graph):
    with open("graph.png", "r") as f:
        f.write(graph.get_graph(x_ray=True).draw_mermaid_png())
