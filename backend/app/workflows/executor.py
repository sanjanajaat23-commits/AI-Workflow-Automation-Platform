from backend.app.workflows.context import WorkflowContext
from backend.app.workflows.graph import WorkflowGraph
from backend.app.workflows.node_factory import NodeFactory


class WorkflowExecutor:

    def __init__(self):
        self.context = WorkflowContext()
        self.visited = set()

    def execute(self, nodes, connections):

        graph = WorkflowGraph(
            nodes=nodes,
            connections=connections,
        )

        results = []

        for start_node in graph.get_start_nodes():
            self._execute_node(
                start_node,
                graph,
                results,
            )

        return results

    def _execute_node(
        self,
        node,
        graph,
        results,
    ):

        if node.id in self.visited:
            return

        self.visited.add(node.id)

        runner = NodeFactory.get_node(
            node.node_type,
        )

        output = runner.execute(
            node=node,
            context=self.context,
        )

        self.context.set(
            str(node.id),
            output,
        )

        results.append(
            {
                "node_id": node.id,
                "node_type": node.node_type,
                "output": output,
            }
        )

        for next_node in graph.get_next_nodes(node.id):
            self._execute_node(
                next_node,
                graph,
                results,
            )
