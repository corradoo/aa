import networkx as nx
import matplotlib.pyplot as plt

colors = {
    "free": "lightblue",
    "locked": "green",
    "blocked": "gray",
    "conflict": "red",
}

states = ["free", "locked", "blocked", "conflict"]


class Node:
    def __init__(self, id, st="free"):
        self.id = id
        self.status = st
        self.independent_set = set()


def get_state(graph, node_id, independent_set):
    if independent_set[node_id]:
        if all(
            [independent_set[n] == False for n in graph[node_id]]
        ):  # n in S all Neigh not in S
            return "locked"
        else:  # n in S 1< Neigh in S
            return "conflict"
    else:
        if all(
            [independent_set[n] == False for n in graph[node_id]]
        ):  # n NOT in S NO Neigh in S
            return "free"
        else:  # n NOT in S 1< Neigh in S
            return "blocked"


def self_stabilizing_max_independent_set(graph):
    # Init nodes
    num_nodes = len(graph)
    nodes = []
    independent_set = [random.random() < 0.5 for _ in range(num_nodes)]
    # independent_set = [False]*num_nodes

    for node_id in range(num_nodes):
        print(f"Node {node_id} -> {get_state(graph,node_id,independent_set)}")
        nodes.append(Node(node_id, get_state(graph, node_id, independent_set)))

    rounds = 0
    while True:
        rounds += 1

        # node = nodes[rounds%num_nodes]
        node = random.choice(nodes)
        visualize(graph, nodes, rounds, node.id)

        node.status = get_state(graph, node.id, independent_set)
        if "conflict" == node.status:
            independent_set[node.id] = False
        elif "free" == node.status:
            independent_set[node.id] = True
        node.status = get_state(graph, node.id, independent_set)
        # print(f"Node {node.id} -> {node.status}")

        #Check if state switch possible for any node, otherwise terminate
        if all(["locked" == node.status or "blocked" == node.status for node in nodes]):
            stable = True
            for id in range(num_nodes):
                stable = stable and nodes[id].status == get_state(
                    graph, id, independent_set
                )

            if stable:
                break  # System is in stable state

    print(f"System stabilized in {rounds} steps.")
    max_independent_set = set([n.id for n in nodes if n.status == "locked"])
    visualize(graph, nodes, rounds)
    return max_independent_set


import random


def gen_graph(num_vertices=10):
    # Generate a random graph with 10 vertices
    graph = {}

    # Create vertices
    for i in range(num_vertices):
        graph[i] = []

    # Add random edges to the graph
    for i in range(num_vertices):
        for j in range(i + 1, num_vertices):
            if random.random() < 0.2:  # Adjust the probability of having an edge
                graph[i].append(j)
                graph[j].append(i)

    # Print the generated graph
    print("Graph:", graph)
    return graph


def visualize(g, nodes, round, id=None):
    # Generate a random graph with 10 vertices
    num_vertices = len(g)
    graph = nx.Graph()

    # Add nodes to the graph
    graph.add_nodes_from(range(num_vertices))

    # Add random edges to the graph
    # for i in range(num_vertices):
    #     for j in range(i + 1, num_vertices):
    #         if random.random() < 0.3:  # Adjust the probability of having an edge
    #             graph.add_edge(i, j)

    for v in g:
        # print(v, end=": ")
        for e in g[v]:
            # print(f"{(v,e)}", end=" ")
            graph.add_edge(v, e)
        # print()

    # Visualize the graph
    pos = nx.spring_layout(graph)

    edge_color = "gray"
    node_alpha = 0.7
    edge_alpha = 0.3

    color_map = [colors[n.status] for n in nodes]

    print(f"f{(color_map.count('red'),color_map.count('lightblue'),color_map.count('green')+color_map.count('gray'))}")
    plt.figure(figsize=(8, 6))
    nx.draw_networkx_nodes(graph, pos, node_color=color_map, alpha=node_alpha)
    nx.draw_networkx_edges(graph, pos, edge_color=edge_color, alpha=edge_alpha)
    nx.draw_networkx_labels(graph, pos)
    plt.axis("off")
    if id:
        plt.title(f"Graph Visualization - step: {round} node: {id} f{(color_map.count('red'),color_map.count('lightblue'),color_map.count('green')+color_map.count('gray'))}")
        plt.savefig(f"out/graph_step{round}.png")
    else:
        plt.title(
            f"Graph Visualization - step: {round} STABILIZED{(color_map.count('red'),color_map.count('lightblue'),color_map.count('green')+color_map.count('gray'))}"
        )
        plt.savefig(f"out/graph_stabilized.png")
    plt.clf()


# Example usage

graph = {
    0: [2, 3, 5],
    1: [5],
    2: [0, 7, 8, 9],
    3: [0, 5, 6, 7, 9],
    4: [6, 7, 9],
    5: [0, 1, 3, 8],
    6: [3, 4],
    7: [2, 3, 4],
    8: [2, 5, 9],
    9: [2, 3, 4, 8],
}
graph = {0: [1, 4], 1: [0, 2, 4], 2: [1, 3], 3: [2, 4, 5], 4: [0, 1, 3], 5: [3], 6: []}

graph = {
    0: [4, 8, 11, 14, 16],
    1: [5, 13],
    2: [],
    3: [14],
    4: [0, 9, 10, 16, 19],
    5: [1, 18],
    6: [15],
    7: [10, 13],
    8: [0, 16],
    9: [4, 12],
    10: [4, 7, 13],
    11: [0, 18],
    12: [9, 19],
    13: [1, 7, 10, 18],
    14: [0, 3, 19],
    15: [6],
    16: [0, 4, 8],
    17: [],
    18: [5, 11, 13],
    19: [4, 12, 14],
}
graph = gen_graph(20)
graph = {
    0: [3, 9, 16],
    1: [4, 8, 11, 18, 19],
    2: [7, 9, 17],
    3: [0, 4, 10, 12],
    4: [1, 3, 6, 15, 18],
    5: [10, 13, 16, 17, 19],
    6: [4, 11, 19],
    7: [2],
    8: [1, 9, 12, 13, 14],
    9: [0, 2, 8, 10, 11, 16],
    10: [3, 5, 9, 15, 18, 19],
    11: [1, 6, 9, 13],
    12: [3, 8, 13],
    13: [5, 8, 11, 12],
    14: [8],
    15: [4, 10, 16, 17],
    16: [0, 5, 9, 15, 17, 18],
    17: [2, 5, 15, 16],
    18: [1, 4, 10, 16],
    19: [1, 5, 6, 10],
}

graph = {
    0: [1, 2],
    1: [0, 2],
    2: [0, 1, 3],
    3: [2, 5],
    4: [5],
    5: [3, 4, 6, 7],
    6: [5, 8],
    7: [5, 8],
    8: [6, 7],
}
max_independent_set = self_stabilizing_max_independent_set(graph)
# visualize(graph, max_independent_set)

print("Maximum Independent Set:", max_independent_set)
