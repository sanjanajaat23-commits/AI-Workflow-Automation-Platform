import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import {
  ReactFlow,
  Background,
  Controls,
  MiniMap,
  addEdge,
  applyEdgeChanges,
  applyNodeChanges,
} from "@xyflow/react";

import type {
  Node,
  Edge,
  Connection,
  NodeChange,
  EdgeChange,
} from "@xyflow/react";

import "@xyflow/react/dist/style.css";

import NodePalette from "../components/NodePalette";
import NodeSettings from "../components/NodeSettings";
import ExecutionPanel from "../components/ExecutionPanel";
import { nodeTypes } from "../components/nodes/nodeTypes";

import {
  saveNode,
  updateNode,
  getNodes,
} from "../services/nodeService";
import {
  saveConnections,
  getConnections,
} from "../services/connectionService";
import {
  executeWorkflow,
} from "../services/executionService";
import {
  createWorkflow,
  getWorkflows,
} from "../services/workflowService";

const DEFAULT_WORKFLOW_NAME = "My Workflow";

type WorkflowNodeData = {
  label: string;
  config: Record<string, any>;
  dbId: number | null;
};

type WorkflowNode = Node<WorkflowNodeData>;

const createInitialNode = (): WorkflowNode => ({
  id: "start",
  type: "workflow",
  position: { x: 100, y: 260 },
  data: {
    label: "Start",
    config: {},
    dbId: null,
  },
});

export default function WorkflowBuilder() {
  const [workflowId, setWorkflowId] = useState<number | null>(null);
  const [workflowName, setWorkflowName] = useState(DEFAULT_WORKFLOW_NAME);
  const [nodes, setNodes] = useState<WorkflowNode[]>([
    createInitialNode(),
  ]);
  const [edges, setEdges] = useState<Edge[]>([]);
  const [selectedNode, setSelectedNode] =
    useState<WorkflowNode | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [executing, setExecuting] = useState(false);
  const [executionId, setExecutionId] = useState<number | null>(null);
  const initialized = useRef(false);

  const hasNodes = useMemo(() => nodes.length > 0, [nodes]);

  useEffect(() => {
    if (initialized.current) return;
    initialized.current = true;
    initializeWorkflow();
  }, []);

  async function initializeWorkflow() {
    try {
      setLoading(true);

      const workflows = await getWorkflows();
      let workflow = Array.isArray(workflows)
        ? workflows[0]
        : null;

      if (!workflow) {
        workflow = await createWorkflow(DEFAULT_WORKFLOW_NAME);
      }

      setWorkflowId(workflow.id);
      setWorkflowName(workflow.name);
      await loadWorkflow(workflow.id);
    } catch (error) {
      console.error(error);
      alert("Failed to initialize workflow.");
    } finally {
      setLoading(false);
    }
  }

  async function loadWorkflow(id: number) {
    const [nodeResponse, connectionResponse] = await Promise.all([
      getNodes(id),
      getConnections(id),
    ]);

    if (nodeResponse.length > 0) {
      const loadedNodes: WorkflowNode[] = nodeResponse.map(
        (node: any) => ({
          id: node.node_key,
          type: "workflow",
          position: {
            x: node.position_x,
            y: node.position_y,
          },
          data: {
            label: node.name,
            config: node.config ?? {},
            dbId: node.id,
          },
        }),
      );

      setNodes(loadedNodes);
    } else {
      setNodes([createInitialNode()]);
    }

    if (connectionResponse.length > 0) {
      const loadedEdges: Edge[] = connectionResponse
        .filter(
          (connection: any) =>
            connection.source_node_key !== connection.target_node_key &&
            connection.target_node_key !== "start",
        )
        .map((connection: any) => ({
          id: `${connection.source_node_key}-${connection.target_node_key}`,
          source: connection.source_node_key,
          target: connection.target_node_key,
          sourceHandle: connection.source_handle,
          targetHandle: connection.target_handle,
        }));

      setEdges(loadedEdges);
    } else {
      setEdges([]);
    }
  }

  const onNodesChange = useCallback((changes: NodeChange[]) => {
    setNodes((current) =>
      applyNodeChanges(changes, current) as WorkflowNode[],
    );
  }, []);

  const onEdgesChange = useCallback((changes: EdgeChange[]) => {
    setEdges((current) => applyEdgeChanges(changes, current));
  }, []);

  const onConnect = useCallback((connection: Connection) => {
    if (!connection.source || !connection.target) return;
    if (connection.source === connection.target) return;
    if (connection.target === "start") return;

    setEdges((current) => {
      const duplicate = current.some(
        (edge) =>
          edge.source === connection.source &&
          edge.target === connection.target,
      );
      return duplicate ? current : addEdge(connection, current);
    });
  }, []);

  const onNodeClick = useCallback((_event: unknown, node: Node) => {
    setSelectedNode(node as WorkflowNode);
  }, []);

  function defaultConfig(type: string): Record<string, any> {
    switch (type.toLowerCase()) {
      case "http":
        return { method: "GET", url: "", headers: {}, body: {}, timeout: 30 };
      case "ai":
        return { prompt: "", model: "gpt-4.1-mini", temperature: 0.7 };
      default:
        return {};
    }
  }

  function addNode(type: string) {
    const id = crypto.randomUUID();
    const workflowNodes = nodes.filter(
      (node) => node.id !== "start",
    );
    const node: WorkflowNode = {
      id,
      type: "workflow",
      position: {
        x: 360 + workflowNodes.length * 250,
        y: 260,
      },
      data: {
        label: type,
        config: defaultConfig(type),
        dbId: null,
      },
    };

    setNodes((current) => [...current, node]);
  }

  function autoArrange() {
    setNodes((current) => {
      const start = current.find((node) => node.id === "start");
      const others = current.filter((node) => node.id !== "start");

      const arranged: WorkflowNode[] = [];
      if (start) {
        arranged.push({
          ...start,
          position: { x: 100, y: 260 },
        });
      }

      others.forEach((node, index) => {
        arranged.push({
          ...node,
          position: {
            x: 360 + index * 250,
            y: 260,
          },
        });
      });

      return arranged;
    });
  }

  function saveNodeConfig(config: Record<string, any>) {
    if (!selectedNode) return;

    setNodes((current) =>
      current.map((node) =>
        node.id === selectedNode.id
          ? {
              ...node,
              data: {
                ...node.data,
                config: { ...config },
              },
            }
          : node,
      ),
    );

    setSelectedNode(null);
  }

  async function handleSaveWorkflow(): Promise<WorkflowNode[]> {
    if (!workflowId) {
      throw new Error("No workflow is loaded.");
    }

    setSaving(true);

    try {
      const savedNodes: WorkflowNode[] = [];

      for (const node of nodes) {
        if (node.data.dbId) {
          const updated = await updateNode(node.data.dbId, node);
          savedNodes.push({
            ...node,
            data: {
              ...node.data,
              dbId: updated.id,
            },
          });
        } else {
          const created = await saveNode(workflowId, node);
          savedNodes.push({
            ...node,
            data: {
              ...node.data,
              dbId: created.id,
            },
          });
        }
      }

      await saveConnections(workflowId, edges);
      setNodes(savedNodes);

      return savedNodes;
    } finally {
      setSaving(false);
    }
  }

  async function handleSaveClick() {
    try {
      await handleSaveWorkflow();
      alert("Workflow saved successfully.");
    } catch (error) {
      console.error(error);
      alert("Failed to save workflow.");
    }
  }

  async function handleExecuteWorkflow() {
    if (!workflowId) return;

    try {
      setExecuting(true);

      // Always persist the latest node configuration and connections.
      await handleSaveWorkflow();

      const execution = await executeWorkflow(workflowId);
      setExecutionId(execution.id);
      alert("Workflow execution started.");
    } catch (error: any) {
      console.error(error);
      const message =
        error?.response?.data?.detail ||
        error?.message ||
        "Failed to execute workflow.";
      alert(message);
    } finally {
      setExecuting(false);
    }
  }

  return (
    <div
      style={{
        display: "flex",
        width: "100%",
        height: "100vh",
        overflow: "hidden",
        background: "#f8fafc",
      }}
    >
      <NodePalette onAddNode={addNode} />

      <div style={{ flex: 1, position: "relative" }}>
        <div
          style={{
            position: "absolute",
            top: 20,
            right: 20,
            zIndex: 1000,
            display: "flex",
            gap: 12,
            alignItems: "center",
          }}
        >
          <span style={{ fontWeight: 600, color: "#111827" }}>
            {workflowName}
          </span>

          <button
            onClick={autoArrange}
            disabled={loading || saving || nodes.length < 2}
            style={{
              padding: "10px 16px",
              border: "1px solid #cbd5e1",
              borderRadius: 8,
              background: "#ffffff",
              color: "#334155",
              cursor: "pointer",
              fontWeight: 600,
            }}
          >
            Auto Arrange
          </button>

          <button
            onClick={handleExecuteWorkflow}
            disabled={executing || saving || loading || !hasNodes}
            style={{
              padding: "10px 18px",
              border: "none",
              borderRadius: 8,
              background: "#16a34a",
              color: "#fff",
              cursor: "pointer",
              fontWeight: 600,
              minWidth: 180,
            }}
          >
            {executing ? "Executing..." : "Execute Workflow"}
          </button>

          <button
            onClick={handleSaveClick}
            disabled={saving || loading}
            style={{
              padding: "10px 18px",
              border: "none",
              borderRadius: 8,
              background: "#2563eb",
              color: "#fff",
              cursor: "pointer",
              fontWeight: 600,
              minWidth: 160,
            }}
          >
            {saving ? "Saving..." : "Save Workflow"}
          </button>
        </div>

        {loading ? (
          <div
            style={{
              height: "100%",
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
              fontSize: 18,
              fontWeight: 600,
            }}
          >
            Loading workflow...
          </div>
        ) : (
          <ReactFlow
            nodes={nodes}
            edges={edges}
            nodeTypes={nodeTypes}
            fitView
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            onConnect={onConnect}
            onNodeClick={onNodeClick}
          >
            <Background />
            <MiniMap />
            <Controls />
          </ReactFlow>
        )}

        {selectedNode && (
          <div
            style={{
              position: "absolute",
              top: 0,
              right: 0,
              width: 360,
              height: "100%",
              background: "#ffffff",
              borderLeft: "1px solid #e5e7eb",
              boxShadow: "-4px 0 10px rgba(0,0,0,0.08)",
              overflowY: "auto",
              zIndex: 1001,
            }}
          >
            <NodeSettings
              node={selectedNode}
              onClose={() => setSelectedNode(null)}
              onSave={saveNodeConfig}
            />
          </div>
        )}

        {executionId && <ExecutionPanel executionId={executionId} />}
      </div>
    </div>
  );
}
