import random
import networkx as nx
import matplotlib.pyplot as plt


class Edge:
    def __init__(self, node1, node2):
        self.nodes = [node1, node2]
        self.value = 0
        node1.add_edge(self)
        node2.add_edge(self)

    def add_value(self, value):
        self.value += value

    def can_add(self):
        return min([node.cost - sum([edge.value for edge in node.edge_list]) for node in self.nodes])


class Node:
    def __init__(self, cost):
        self.cost = cost
        self.color = 'Cyan'
        self.edge_list = []

    def add_edge(self, edge: Edge):
        self.edge_list.append(edge)

    def is_tight(self):
        return sum([edge.value for edge in self.edge_list]) == self.cost


class VertexCover:
    def __init__(self, node_num):
        self.nodes = []
        self.edges = []
        for i in range(node_num):
            self.nodes.append(Node(random.randint(1, 100)))
        all_edge = [set() for i in range(node_num)]
        for i in range(node_num):
            num = 0
            while num == 0:
                num = sum([1 if i in all_edge[j] else 0 for j in range(node_num)])
                for j in range(node_num):
                    if i != j:
                        if random.random() < 0.3:
                            if i not in all_edge[j]:
                                self.edges.append(Edge(self.nodes[i], self.nodes[j]))
                                num += 1
                                all_edge[i].add(j)
                        if num > min(max(2, node_num // 3), 10):
                            break
                break
    #
    # def __init__(self, node_num):
    #     self.nodes = []
    #     self.edges = []
    #     center = Node(9)
    #     for i in range(node_num-1):
    #         self.nodes.append(Node(2**i))
    #         self.edges.append(Edge(self.nodes[i], center))
    #     self.nodes.append(center)


    def print_map(self, draw_edge=False, figure_size=None, name='1'):
        if figure_size:
            plt.figure('Draw', figsize=(figure_size, figure_size))
        plt.clf()
        plt.axis('off')
        G = nx.Graph()
        for n in self.nodes:
            G.add_node(n, value="{}".format(n.cost))
        for e in self.edges:
            G.add_edge(e.nodes[0], e.nodes[1], value=e.value)
        node_labels = nx.get_node_attributes(G, 'value')
        edge_labels = nx.get_edge_attributes(G, 'value')
        pos = nx.circular_layout(G)
        nx.draw(G, pos, node_size=1200, node_color=[node.color for node in self.nodes])
        nx.draw_networkx_labels(G, pos, labels=node_labels)
        if draw_edge:
            nx.draw_networkx_edge_labels(G, pos, font_size=16, edge_labels=edge_labels, rotate=False,
                                         bbox=dict(boxstyle="round,pad=0", fc="1", ec="1", alpha=1), label_pos=0.3,
                                         horizontalalignment='left', verticalalignment='center_baseline')
        plt.gca().xaxis.set_major_locator(plt.NullLocator())
        plt.gca().yaxis.set_major_locator(plt.NullLocator())
        plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
        plt.margins(0.1, 0.1)
        plt.savefig('./result/{}.png'.format(name), dpi=1000)
        plt.show()

    def is_all_tight(self):
        for n in self.nodes:
            if not n.is_tight():
                return False
        return True

    def no_update(self):
        for e in self.edges:
            if e.can_add() > 0:
                return False
        return True

    def reset_color_and_edge(self):
        for edge in self.edges:
            edge.value = 0
        for node in self.nodes:
            node.color = 'Cyan'

    def build_wolfram_data(self):
        node_index = {}
        node_cost = []
        adj_matrix = [[0 for i in range(len(self.nodes))] for j in range(len(self.nodes))]
        for node in range(len(self.nodes)):
            node_index[self.nodes[node]] = node
            node_cost.append(self.nodes[node].cost)
        for edge in self.edges:
            adj_matrix[node_index[edge.nodes[0]]][node_index[edge.nodes[1]]] = 1
        return adj_matrix, node_cost
