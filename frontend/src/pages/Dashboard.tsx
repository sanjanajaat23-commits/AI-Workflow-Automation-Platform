import { useEffect, useState } from "react";
import DashboardCards from "../components/DashboardCards";
import { getDashboardStats } from "../services/dashboardService";

export default function Dashboard() {
  const [stats, setStats] = useState({
    workflows: 0,
    running: 0,
    completed: 0,
    failed: 0,
  });

  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboard();
  }, []);

  async function loadDashboard() {
    try {
      const data = await getDashboardStats();
      setStats(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  if (loading) {
    return (
      <div style={{ padding: 30 }}>
        Loading Dashboard...
      </div>
    );
  }

  return (
    <div style={{ padding: 30 }}>
      <h1
        style={{
          marginBottom: 30,
        }}
      >
        AI Workflow Dashboard
      </h1>

      <DashboardCards
        workflows={stats.workflows}
        running={stats.running}
        completed={stats.completed}
        failed={stats.failed}
      />
    </div>
  );
}