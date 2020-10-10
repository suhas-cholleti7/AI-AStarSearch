import node


class Graph:
    list_of_nodes = {}

    def add_node(self, name):
        """
        Adds a node to the graph
        """
        if name not in self.list_of_nodes:
            self.list_of_nodes[name] = node.GraphNode(name)
        # self.list_of_nodes.append(node.GraphNode(name))

    def add_edge(self, node1, node2):
        """
        Adds an edge between the input nodes
        """
        if node1 not in self.list_of_nodes.keys():
            self.add_node(node1)
        if node2 not in self.list_of_nodes.keys():
            self.add_node(node2)
        self.list_of_nodes[node1].connect_to(self.list_of_nodes[node2])
        # self.list_of_nodes[node2].connect_to(self.list_of_nodes[node1])

    def get_node(self, name):
        """
        return the node with the input name
        """
        return self.list_of_nodes[name]
