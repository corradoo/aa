import networkx as nx
import matplotlib.pyplot as plt


class Node:
    def __init__(self, id):
        self.id = id
        self.status = "free"
        self.independent_set = set()

    def send_message(self, neighbor):
        # Send current status and independent set to neighbor
        return self.status, self.independent_set

    def receive_message(self, neighbor_status, neighbor_independent_set):
        print(f"Node {self.id} status: {self.status}")
        # Update independent set based on neighbor's set
        if len(neighbor_independent_set) > len(self.independent_set):
            self.independent_set = neighbor_independent_set.copy()

    def update_independent_set(self, graph):
        # Check if adding itself to the independent set is possible without conflicts
        neighbors = graph[self.id]
        for neighbor in neighbors:
            if neighbor in self.independent_set:
                self.status = "blocked"
                return
        self.independent_set.add(self.id)
        self.status = "locked"


def self_stabilizing_max_independent_set(graph):
    nodes = []
    for node_id in range(len(graph)):
        nodes.append(Node(node_id))

    rounds = 0
    while True:
        rounds += 1
        stable = True

        for node in nodes:
            # Node already in IS
            # if node.status == 'passive':
            #     continue

            messages = []
            for neighbor in graph[node.id]:
                neighbor_status, neighbor_independent_set = nodes[
                    neighbor
                ].send_message(node.id)
                messages.append((neighbor_status, neighbor_independent_set))
            # breakpoint()
            for neighbor_status, neighbor_independent_set in messages:
                node.receive_message(neighbor_status, neighbor_independent_set)

            previous_independent_set = node.independent_set.copy()
            node.update_independent_set(graph)

            if previous_independent_set != node.independent_set:
                stable = False

        if stable:
            break

    print(f"System stabilized in {rounds} rounds.")
    max_independent_set = set()
    for node in nodes:
        max_independent_set |= node.independent_set
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


def visualize(g, in_set):
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
        print(v, end=": ")
        for e in g[v]:
            print(f"{(v,e)}", end=" ")
            graph.add_edge(v, e)
        print()

    # Visualize the graph
    pos = nx.spring_layout(graph)
    node_color = "lightblue"
    node_color_is = "red"
    edge_color = "gray"
    node_alpha = 0.7
    edge_alpha = 0.3

    color_map = [node_color] * num_vertices
    for n in in_set:
        color_map[n] = node_color_is

    plt.figure(figsize=(8, 6))
    nx.draw_networkx_nodes(graph, pos, node_color=color_map, alpha=node_alpha)
    nx.draw_networkx_edges(graph, pos, edge_color=edge_color, alpha=edge_alpha)
    nx.draw_networkx_labels(graph, pos)
    plt.title("Random Graph Visualization")
    plt.axis("off")
    plt.savefig("graph.png")


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
    8: [6, 7]
}
max_independent_set = self_stabilizing_max_independent_set(graph)
visualize(graph, max_independent_set)
# visualize(graph, max_independent_set)

print("Maximum Independent Set:", max_independent_set)
