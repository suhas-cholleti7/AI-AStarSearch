class GraphNode:
    name = ()
    connected_node = None

    def __init__(self, name):
        self.name = name

    def connect_to(self, node):
        """
        connects the current node to the input node
        """
        self.connected_node = node

    def get_name(self):
        """
        returns the name of the present node
        """
        return self.name

    def get_connected_node(self):
        """
        returns the node object to which the current code in connected
        """
        return self.connected_node
