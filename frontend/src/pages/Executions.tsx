import { useEffect, useState } from "react";
import { getExecutions } from "../services/executionHistoryService";

type Execution = {
  id: number;
  workflow_id: number;
  status: string;
  started_at: string | null;
  finished_at: string | null;
};

function StatusBadge({ status }: { status: string }) {
  let background = "#6b7280";

  if (status === "completed") background = "#16a34a";
  if (status === "running") background = "#f59e0b";
  if (status === "failed") background = "#dc2626";

  return (
    <span
      style={{
        background,
        color: "white",
        padding: "4px 10px",
        borderRadius: 20,
        fontSize: 13,
        fontWeight: 600,
      }}
    >
      {status.toUpperCase()}
    </span>
  );
}

export default function Executions() {
  const [executions, setExecutions] = useState<Execution[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadExecutions();
  }, []);

  async function loadExecutions() {
    try {
      const data = await getExecutions();
      setExecutions(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  if (loading) {
    return <div style={{ padding: 30 }}>Loading...</div>;
  }

  return (
    <div style={{ padding: 30 }}>
      <h1>Workflow Executions</h1>

      <table
        style={{
          width: "100%",
          marginTop: 20,
          borderCollapse: "collapse",
        }}
      >
        <thead>
          <tr>
            <th>ID</th>
            <th>Workflow</th>
            <th>Status</th>
            <th>Started</th>
            <th>Finished</th>
          </tr>
        </thead>

        <tbody>
          {executions.map((execution) => (
            <tr key={execution.id}>
              <td>{execution.id}</td>

              <td>{execution.workflow_id}</td>

              <td>
                <StatusBadge
                  status={execution.status}
                />
              </td>

              <td>
                {execution.started_at
                  ? new Date(
                      execution.started_at
                    ).toLocaleString()
                  : "-"}
              </td>

              <td>
                {execution.finished_at
                  ? new Date(
                      execution.finished_at
                    ).toLocaleString()
                  : "-"}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}