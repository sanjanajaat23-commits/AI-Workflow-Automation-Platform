import api from "./api";

export async function saveConnections(
  workflowId: number,
  edges: any[]
) {
  const response = await api.post(
    `/workflows/${workflowId}/connections`,
    edges
  );

  return response.data;
}

export async function getConnections(
  workflowId: number
) {
  const response = await api.get(
    `/workflows/${workflowId}/connections`
  );

  return response.data;
}