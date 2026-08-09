from collections import defaultdict


class WorkflowGraph:
    def __init__(self, nodes, connections):
        self.nodes = {node.id: node for node in nodes}
        self.connections = connections
        self.graph = defaultdict(list)

        for connection in connections:
            self.graph[connection.source_node_id].append(
                connection.target_node_id
            )

    def get_start_nodes(self):
        targets = {
            connection.target_node_id
            for connection in self.connections
        }

        return [
            node
            for node in self.nodes.values()
            if node.id not in targets
        ]

    def get_next_nodes(self, node_id):
        return [
            self.nodes[next_id]
            for next_id in self.graph.get(node_id, [])
            if next_id in self.nodes
        ]
