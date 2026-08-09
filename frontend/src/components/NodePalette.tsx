type Props = {
  onAddNode: (type: string) => void;
};

// Only expose nodes that are implemented by the current execution engine.
const nodes = ["HTTP", "AI"];

export default function NodePalette({ onAddNode }: Props) {
  return (
    <div
      style={{
        width: 220,
        background: "#111827",
        padding: 20,
        borderRight: "1px solid #1f2937",
      }}
    >
      <h3 style={{ marginBottom: 20, color: "white" }}>Nodes</h3>

      {nodes.map((node) => (
        <button
          key={node}
          onClick={() => onAddNode(node)}
          style={{
            width: "100%",
            marginBottom: 12,
            padding: "12px",
            border: "none",
            borderRadius: 8,
            background: "#1e293b",
            color: "white",
            cursor: "pointer",
          }}
        >
          {node}
        </button>
      ))}
    </div>
  );
}
