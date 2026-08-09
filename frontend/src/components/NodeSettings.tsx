import { useEffect, useState } from "react";

type Props = {
  node: any;
  onClose: () => void;
  onSave: (config: any) => void;
};

export default function NodeSettings({
  node,
  onClose,
  onSave,
}: Props) {
  const [config, setConfig] = useState<Record<string, any>>({});

  useEffect(() => {
    setConfig(node?.data?.config || {});
  }, [node]);

  if (!node) return null;

  const nodeType = String(node.data.label).toLowerCase();

  function handleSave() {
    if (nodeType === "http" && !String(config.url || "").trim()) {
      alert("HTTP node requires a URL.");
      return;
    }

    if (nodeType === "ai" && !String(config.prompt || "").trim()) {
      alert("AI node requires a prompt.");
      return;
    }

    onSave(config);
  }

  return (
    <div
      style={{
        width: 340,
        height: "100%",
        background: "#111827",
        color: "white",
        padding: 20,
        borderLeft: "1px solid #374151",
        overflowY: "auto",
      }}
    >
      <h2 style={{ marginBottom: 20 }}>{node.data.label} Settings</h2>

      {nodeType === "http" && (
        <>
          <label>URL</label>
          <input
            value={config.url || ""}
            onChange={(e) =>
              setConfig({ ...config, url: e.target.value })
            }
            placeholder="https://example.com/api"
            style={inputStyle}
          />

          <label>Method</label>
          <select
            value={config.method || "GET"}
            onChange={(e) =>
              setConfig({ ...config, method: e.target.value })
            }
            style={inputStyle}
          >
            <option>GET</option>
            <option>POST</option>
            <option>PUT</option>
            <option>DELETE</option>
            <option>PATCH</option>
          </select>

          <label>Timeout (seconds)</label>
          <input
            type="number"
            min={1}
            value={config.timeout ?? 30}
            onChange={(e) =>
              setConfig({
                ...config,
                timeout: Number(e.target.value),
              })
            }
            style={inputStyle}
          />
        </>
      )}

      {nodeType === "ai" && (
        <>
          <label>Prompt</label>
          <textarea
            rows={7}
            value={config.prompt || ""}
            onChange={(e) =>
              setConfig({ ...config, prompt: e.target.value })
            }
            placeholder="Ask the AI to do something..."
            style={inputStyle}
          />

          <label>Model</label>
          <input
            value={config.model || "gpt-4.1-mini"}
            onChange={(e) =>
              setConfig({ ...config, model: e.target.value })
            }
            style={inputStyle}
          />

          <label>Temperature</label>
          <input
            type="number"
            min={0}
            max={2}
            step="0.1"
            value={config.temperature ?? 0.7}
            onChange={(e) =>
              setConfig({
                ...config,
                temperature: Number(e.target.value),
              })
            }
            style={inputStyle}
          />
        </>
      )}

      <div style={{ display: "flex", gap: 10, marginTop: 30 }}>
        <button onClick={handleSave} style={saveButton}>
          Save
        </button>
        <button onClick={onClose} style={closeButton}>
          Close
        </button>
      </div>
    </div>
  );
}

const inputStyle = {
  width: "100%",
  padding: "10px",
  marginTop: 8,
  marginBottom: 20,
  borderRadius: 8,
  border: "1px solid #374151",
  background: "#1f2937",
  color: "white",
} as const;

const saveButton = {
  flex: 1,
  padding: "10px",
  border: "none",
  borderRadius: 8,
  background: "#2563eb",
  color: "white",
  cursor: "pointer",
} as const;

const closeButton = {
  flex: 1,
  padding: "10px",
  border: "none",
  borderRadius: 8,
  background: "#4b5563",
  color: "white",
  cursor: "pointer",
} as const;
