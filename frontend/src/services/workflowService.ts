import api from "./api";

export async function getWorkflows() {
  const response = await api.get("/workflows/");
  return response.data;
}

export async function createWorkflow(name: string) {
  const response = await api.post("/workflows/", {
    name,
    description: "",
    is_active: true,
  });

  return response.data;
}