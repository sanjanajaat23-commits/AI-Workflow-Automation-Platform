import api from "./api";

export async function executeWorkflow(workflowId: number) {
  const response = await api.post(
    `/executions/${workflowId}/execute`
  );

  return response.data;
}

export async function getExecutionLogs(
  executionId: number
) {
  const response = await api.get(
    `/execution-logs/${executionId}`
  );

  return response.data;
}