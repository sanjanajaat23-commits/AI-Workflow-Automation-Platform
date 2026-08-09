type Props = {
  workflows: number;
  running: number;
  completed: number;
  failed: number;
};

function Card({
  title,
  value,
  color,
}: {
  title: string;
  value: number;
  color: string;
}) {
  return (
    <div
      style={{
        flex: 1,
        background: "#ffffff",
        borderRadius: 12,
        padding: 20,
        boxShadow: "0 2px 10px rgba(0,0,0,0.08)",
      }}
    >
      <div
        style={{
          fontSize: 14,
          color: "#6b7280",
        }}
      >
        {title}
      </div>

      <div
        style={{
          marginTop: 12,
          fontSize: 34,
          fontWeight: 700,
          color,
        }}
      >
        {value}
      </div>
    </div>
  );
}

export default function DashboardCards({
  workflows,
  running,
  completed,
  failed,
}: Props) {
  return (
    <div
      style={{
        display: "grid",
        gridTemplateColumns:
          "repeat(4,1fr)",
        gap: 20,
      }}
    >
      <Card
        title="Workflows"
        value={workflows}
        color="#2563eb"
      />

      <Card
        title="Running"
        value={running}
        color="#f59e0b"
      />

      <Card
        title="Completed"
        value={completed}
        color="#16a34a"
      />

      <Card
        title="Failed"
        value={failed}
        color="#dc2626"
      />
    </div>
  );
}