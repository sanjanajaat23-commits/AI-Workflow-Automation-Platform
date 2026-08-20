import { useEffect, useState } from "react";
import api from "../services/api";
import { getExecutions } from "../services/executionHistoryService";

type Execution = {
  id: number;
  workflow_id: number;
  status: string;
  started_at: string | null;
  finished_at: string | null;
};

type ExecutionLog = {
  id: number;
  execution_id: number;
  level: string;
  message: string;
  created_at: string;
};

function LevelBadge({ level }: { level: string }) {
  const normalized = level.toLowerCase();
  const background = normalized === "error" ? "#dc2626" : normalized === "warning" ? "#d97706" : "#16a34a";

  return (
    <span
      style={{
        display: "inline-block",
        background,
        color: "white",
        padding: "4px 9px",
        borderRadius: 999,
        fontSize: 12,
        fontWeight: 700,
        textTransform: "uppercase",
      }}
    >
      {normalized}
    </span>
  );
}

export default function Logs() {
  const [executions, setExecutions] = useState<Execution[]>([]);
  const [selectedExecutionId, setSelectedExecutionId] = useState<number | null>(null);
  const [logs, setLogs] = useState<ExecutionLog[]>([]);
  const [loading, setLoading] = useState(true);
  const [logsLoading, setLogsLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadExecutions() {
      try {
        setError("");
        const data = await getExecutions();
        setExecutions(data);
        if (data.length > 0) {
          setSelectedExecutionId(data[0].id);
        }
      } catch (err) {
        console.error(err);
        setError("Unable to load workflow executions.");
      } finally {
        setLoading(false);
      }
    }

    loadExecutions();
  }, []);

  useEffect(() => {
    if (selectedExecutionId === null) {
      setLogs([]);
      return;
    }

    async function loadLogs() {
      try {
        setLogsLoading(true);
        setError("");
        const response = await api.get(`/execution-logs/${selectedExecutionId}`);
        setLogs(response.data);
      } catch (err) {
        console.error(err);
        setLogs([]);
        setError("Unable to load logs for this execution.");
      } finally {
        setLogsLoading(false);
      }
    }

    loadLogs();
  }, [selectedExecutionId]);

  const selectedExecution = executions.find((execution) => execution.id === selectedExecutionId);

  if (loading) {
    return <div style={{ padding: 30 }}>Loading execution logs...</div>;
  }

  return (
    <div style={{ padding: 30, maxWidth: 1200 }}>
      <h1 style={{ marginBottom: 8 }}>Execution Logs</h1>
      <p style={{ marginTop: 0, opacity: 0.7 }}>
        Inspect node-level events recorded during workflow execution.
      </p>

      {error && (
        <div
          style={{
            marginTop: 20,
            padding: 14,
            borderRadius: 10,
            background: "#3f1d1d",
            color: "#fecaca",
          }}
        >
          {error}
        </div>
      )}

      {executions.length === 0 ? (
        <div style={{ marginTop: 30, padding: 24, borderRadius: 12, background: "#1f2937" }}>
          No workflow executions are available yet. Execute a workflow to generate logs.
        </div>
      ) : (
        <>
          <div
            style={{
              marginTop: 24,
              display: "flex",
              gap: 16,
              alignItems: "center",
              flexWrap: "wrap",
            }}
          >
            <label htmlFor="execution-select" style={{ fontWeight: 700 }}>
              Execution
            </label>
            <select
              id="execution-select"
              value={selectedExecutionId ?? ""}
              onChange={(event) => setSelectedExecutionId(Number(event.target.value))}
              style={{
                minWidth: 240,
                padding: "10px 12px",
                borderRadius: 8,
                border: "1px solid #475569",
                background: "#1e293b",
                color: "inherit",
              }}
            >
              {executions.map((execution) => (
                <option key={execution.id} value={execution.id}>
                  Execution #{execution.id} — Workflow #{execution.workflow_id}
                </option>
              ))}
            </select>

            {selectedExecution && (
              <span style={{ opacity: 0.75 }}>
                Status: <strong>{selectedExecution.status.toUpperCase()}</strong>
              </span>
            )}
          </div>

          <div
            style={{
              marginTop: 24,
              border: "1px solid #334155",
              borderRadius: 12,
              overflow: "hidden",
              background: "#111827",
            }}
          >
            {logsLoading ? (
              <div style={{ padding: 24 }}>Loading logs...</div>
            ) : logs.length === 0 ? (
              <div style={{ padding: 24, opacity: 0.75 }}>
                No log entries were recorded for this execution.
              </div>
            ) : (
              <table style={{ width: "100%", borderCollapse: "collapse" }}>
                <thead>
                  <tr style={{ background: "#1e293b", textAlign: "left" }}>
                    <th style={{ padding: 14 }}>Time</th>
                    <th style={{ padding: 14 }}>Level</th>
                    <th style={{ padding: 14 }}>Message</th>
                  </tr>
                </thead>
                <tbody>
                  {logs.map((log) => (
                    <tr key={log.id} style={{ borderTop: "1px solid #334155" }}>
                      <td style={{ padding: 14, whiteSpace: "nowrap", opacity: 0.75 }}>
                        {new Date(log.created_at).toLocaleString()}
                      </td>
                      <td style={{ padding: 14 }}>
                        <LevelBadge level={log.level} />
                      </td>
                      <td style={{ padding: 14 }}>{log.message}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        </>
      )}
    </div>
  );
}
