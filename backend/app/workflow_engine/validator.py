from collections import defaultdict, deque

from backend.app.workflow_engine.exceptions import (
    CircularWorkflowError,
    WorkflowValidationError,
)


class WorkflowValidator:
    """
    Validates workflow structure before execution.
    """

    @staticmethod
    def validate(workflow) -> bool:
        """
        Validate the complete workflow.
        """

        if workflow is None:
            raise WorkflowValidationError("Workflow not found.")

        if not getattr(workflow, "nodes", None):
            raise WorkflowValidationError(
                "Workflow must contain at least one node."
            )

        WorkflowValidator._validate_unique_node_ids(workflow)
        WorkflowValidator._validate_connections(workflow)
        WorkflowValidator._detect_cycles(workflow)

        return True

    @staticmethod
    def _validate_unique_node_ids(workflow):
        ids = set()

        for node in workflow.nodes:

            if node.id in ids:
                raise WorkflowValidationError(
                    f"Duplicate node id '{node.id}'."
                )

            ids.add(node.id)

    @staticmethod
    def _validate_connections(workflow):

        node_ids = {node.id for node in workflow.nodes}

        for connection in getattr(workflow, "connections", []):

            if connection.source_node_id not in node_ids:
                raise WorkflowValidationError(
                    f"Source node '{connection.source_node_id}' does not exist."
                )

            if connection.target_node_id not in node_ids:
                raise WorkflowValidationError(
                    f"Target node '{connection.target_node_id}' does not exist."
                )

    @staticmethod
    def _detect_cycles(workflow):

        graph = defaultdict(list)
        indegree = defaultdict(int)

        for node in workflow.nodes:
            indegree[node.id] = 0

        for connection in getattr(workflow, "connections", []):
            graph[connection.source_node_id].append(
                connection.target_node_id
            )
            indegree[connection.target_node_id] += 1

        queue = deque(
            node_id
            for node_id, degree in indegree.items()
            if degree == 0
        )

        visited = 0

        while queue:

            current = queue.popleft()
            visited += 1

            for neighbour in graph[current]:

                indegree[neighbour] -= 1

                if indegree[neighbour] == 0:
                    queue.append(neighbour)

        if visited != len(workflow.nodes):
            raise CircularWorkflowError(
                "Circular dependency detected in workflow."
            )