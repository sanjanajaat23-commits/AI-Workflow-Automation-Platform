import api from "./api";

function normalizeNodeType(label: string) {
  return label
    .toLowerCase()
    .replace(/\s+/g, "_")
    .replace("_node", "")
    .replace(" node", "");
}

export async function saveNode(
  workflowId: number,
  node: any
) {
  const response = await api.post(
    `/workflows/${workflowId}/nodes`,
    {
      node_key: node.id,
      node_type: normalizeNodeType(node.data.label),
      name: node.data.label,
      config: node.data.config || {},
      position_x: Math.round(node.position.x),
      position_y: Math.round(node.position.y),
    }
  );

  return response.data;
}

export async function updateNode(
  nodeId: number,
  node: any
) {
  const response = await api.put(
    `/workflows/nodes/${nodeId}`,
    {
      node_type: normalizeNodeType(node.data.label),
      name: node.data.label,
      config: node.data.config || {},
      position_x: Math.round(node.position.x),
      position_y: Math.round(node.position.y),
    }
  );

  return response.data;
}

export async function getNodes(
  workflowId: number
) {
  const response = await api.get(
    `/workflows/${workflowId}/nodes`
  );

  return response.data;
}