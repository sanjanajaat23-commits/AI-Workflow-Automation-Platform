import api from "./api";

export async function getExecutions() {
  const response = await api.get("/executions");
  return response.data;
}