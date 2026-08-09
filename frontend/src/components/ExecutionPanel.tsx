import { useEffect, useState } from "react";
import { getExecutionLogs } from "../services/executionService";

type Log = {
  id: number;
  level: string;
  message: string;
  created_at: string;
};

type Props = {
  executionId: number | null;
};

export default function ExecutionPanel({
  executionId,
}: Props) {
  const [logs, setLogs] = useState<Log[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!executionId) {
      setLogs([]);
      return;
    }

    loadLogs();

    const timer = setInterval(() => {
      loadLogs();
    }, 2000);

    return () => clearInterval(timer);
  }, [executionId]);

  async function loadLogs() {
    try {
      setLoading(true);

      const data = await getExecutionLogs(
        executionId!
      );

      setLogs(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div
      style={{
        width: 340,
        height: "100%",
        background: "#111827",
        color: "white",
        borderLeft: "1px solid #374151",
        padding: 20,
        overflowY: "auto",
      }}
    >
      <h2
        style={{
          marginBottom: 20,
        }}
      >
        Execution Logs
      </h2>

      {!executionId && (
        <p>Execute a workflow first.</p>
      )}

      {loading && (
        <p>Refreshing...</p>
      )}

      {logs.map((log) => (
        <div
          key={log.id}
          style={{
            background: "#1f2937",
            padding: 12,
            borderRadius: 8,
            marginBottom: 12,
          }}
        >
          <div
            style={{
              fontWeight: 700,
              color:
                log.level === "error"
                  ? "#ef4444"
                  : "#22c55e",
            }}
          >
            {log.level.toUpperCase()}
          </div>

          <div
            style={{
              marginTop: 6,
              marginBottom: 6,
            }}
          >
            {log.message}
          </div>

          <small
            style={{
              color: "#9ca3af",
            }}
          >
            {new Date(
              log.created_at
            ).toLocaleString()}
          </small>
        </div>
      ))}
    </div>
  );
}