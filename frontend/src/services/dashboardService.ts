import api from "./api";

export type DashboardStats = {
  workflows: number;
  running: number;
  completed: number;
  failed: number;
};

export async function getDashboardStats(): Promise<DashboardStats> {
  const response = await api.get("/dashboard/stats");
  return response.data;
}