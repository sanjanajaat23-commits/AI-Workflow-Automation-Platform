import { Handle, Position } from "@xyflow/react";

type Props = {
  data: {
    label: string;
  };
};

export default function WorkflowNode({ data }: Props) {
  const label = String(data.label || "Node");
  const type = label.toLowerCase();
  const isStart = type === "start";

  const accent = isStart ? "#16a34a" : type === "ai" ? "#7c3aed" : "#2563eb";
  const icon = isStart ? "▶" : type === "ai" ? "✦" : "↗";

  return (
    <div
      style={{
        minWidth: 190,
        padding: "13px 16px",
        borderRadius: 12,
        border: `1.5px solid ${accent}`,
        background: "#ffffff",
        color: "#111827",
        boxShadow: "0 4px 14px rgba(15, 23, 42, 0.10)",
        fontWeight: 700,
        display: "flex",
        alignItems: "center",
        gap: 10,
        position: "relative",
      }}
    >
      {!isStart && (
        <Handle
          type="target"
          position={Position.Left}
          style={{ background: accent, width: 9, height: 9 }}
        />
      )}

      <span
        style={{
          width: 28,
          height: 28,
          borderRadius: 8,
          display: "grid",
          placeItems: "center",
          background: `${accent}15`,
          color: accent,
          fontSize: 14,
          flexShrink: 0,
        }}
      >
        {icon}
      </span>

      <span style={{ flex: 1, textAlign: "left" }}>{label}</span>

      <Handle
        type="source"
        position={Position.Right}
        style={{ background: accent, width: 9, height: 9 }}
      />
    </div>
  );
}
