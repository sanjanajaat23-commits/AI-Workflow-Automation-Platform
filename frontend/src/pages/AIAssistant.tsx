import { useState } from "react";
import api from "../services/api";

type Message = { role: "user" | "assistant"; text: string };

type AIResponse = {
  response?: string;
  mode?: string;
  model?: string;
};

export default function AIAssistant() {
  const [prompt, setPrompt] = useState("");
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      text: "Tell me what you want to automate. I can turn a business request into a workflow plan, node sequence, and execution checklist.",
    },
  ]);
  const [loading, setLoading] = useState(false);
  const [mode, setMode] = useState("ready");

  async function sendPrompt() {
    const value = prompt.trim();
    if (!value || loading) return;

    setMessages((current) => [...current, { role: "user", text: value }]);
    setPrompt("");
    setLoading(true);
    setMode("thinking");

    try {
      const response = await api.post<AIResponse>("/ai/assistant", {
        prompt: value,
      });
      setMessages((current) => [
        ...current,
        {
          role: "assistant",
          text: response.data.response ?? "I could not generate a response.",
        },
      ]);
      setMode(response.data.mode === "openai" ? "connected" : "demo");
    } catch (error) {
      console.error(error);
      setMessages((current) => [
        ...current,
        {
          role: "assistant",
          text: "The AI service is unavailable right now. Check the backend deployment and AI settings, then try again.",
        },
      ]);
      setMode("error");
    } finally {
      setLoading(false);
    }
  }

  const suggestions = [
    "Automate customer lead follow-up from a web form",
    "Track freight updates and alert operations when delayed",
    "Reconcile invoices against shipment records every morning",
  ];

  return (
    <section className="page ai-page">
      <div className="page-heading">
        <div>
          <span className="eyebrow">AI COPILOT</span>
          <h1>Build workflows with AI</h1>
          <p>Describe the process in plain English. The copilot turns it into an automation plan.</p>
        </div>
        <span className={`status-pill ${mode}`}>
          <span className="status-dot" />
          {mode === "connected" ? "AI connected" : mode === "demo" ? "Demo mode" : mode}
        </span>
      </div>

      <div className="ai-shell">
        <div className="ai-chat">
          <div className="ai-chat-header">
            <div>
              <strong>Workflow Copilot</strong>
              <span>GPT-powered when OPENAI_API_KEY is configured</span>
            </div>
            <div className="model-chip">AI</div>
          </div>

          <div className="message-list">
            {messages.map((message, index) => (
              <div className={`message-row ${message.role}`} key={`${message.role}-${index}`}>
                <div className="message-avatar">{message.role === "assistant" ? "✦" : "You"}</div>
                <div className="message-bubble">{message.text}</div>
              </div>
            ))}
            {loading && (
              <div className="message-row assistant">
                <div className="message-avatar">✦</div>
                <div className="message-bubble typing">Analyzing workflow…</div>
              </div>
            )}
          </div>

          <div className="ai-composer">
            <textarea
              value={prompt}
              onChange={(event) => setPrompt(event.target.value)}
              onKeyDown={(event) => {
                if (event.key === "Enter" && !event.shiftKey) {
                  event.preventDefault();
                  void sendPrompt();
                }
              }}
              placeholder="Example: When a shipment is delayed, notify the customer, update the TMS, and create a follow-up task."
              rows={4}
            />
            <div className="composer-footer">
              <span>Enter to send · Shift + Enter for a new line</span>
              <button className="primary-button" onClick={() => void sendPrompt()} disabled={loading || !prompt.trim()}>
                {loading ? "Working…" : "Generate workflow →"}
              </button>
            </div>
          </div>
        </div>

        <aside className="ai-side-panel">
          <div className="panel-block">
            <span className="eyebrow">TRY THESE</span>
            {suggestions.map((item) => (
              <button className="suggestion" key={item} onClick={() => setPrompt(item)}>
                {item}
              </button>
            ))}
          </div>

          <div className="panel-block workflow-output">
            <span className="eyebrow">WHAT AI CAN DO</span>
            <div><b>1.</b> Understand the business goal</div>
            <div><b>2.</b> Propose trigger + action nodes</div>
            <div><b>3.</b> Explain conditions and handoffs</div>
            <div><b>4.</b> Give you an execution checklist</div>
          </div>
        </aside>
      </div>
    </section>
  );
}
