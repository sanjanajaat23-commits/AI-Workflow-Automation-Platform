import { useEffect, useState } from "react";
import api from "../services/api";

type AIStatus = {
  configured: boolean;
  demo_mode: boolean;
  model: string;
};

export default function Settings() {
  const [apiBase, setApiBase] = useState(() => localStorage.getItem("workflow_api_base") ?? "/api/v1");
  const [autoSave, setAutoSave] = useState(() => localStorage.getItem("workflow_autosave") !== "false");
  const [notifications, setNotifications] = useState(() => localStorage.getItem("workflow_notifications") !== "false");
  const [darkMode, setDarkMode] = useState(() => localStorage.getItem("workflow_theme") !== "light");
  const [saved, setSaved] = useState(false);
  const [aiStatus, setAiStatus] = useState<AIStatus | null>(null);

  useEffect(() => {
    api.get<AIStatus>("/ai/status").then((response) => setAiStatus(response.data)).catch(() => setAiStatus(null));
  }, []);

  function saveSettings() {
    localStorage.setItem("workflow_api_base", apiBase || "/api/v1");
    localStorage.setItem("workflow_autosave", String(autoSave));
    localStorage.setItem("workflow_notifications", String(notifications));
    localStorage.setItem("workflow_theme", darkMode ? "dark" : "light");
    setSaved(true);
    window.setTimeout(() => setSaved(false), 1800);
  }

  return (
    <section className="page settings-page">
      <div className="page-heading">
        <div>
          <span className="eyebrow">WORKSPACE</span>
          <h1>Settings</h1>
          <p>Control workspace behavior, API routing, and the AI copilot connection.</p>
        </div>
        {saved && <span className="save-badge">Saved</span>}
      </div>

      <div className="settings-grid">
        <div className="settings-card">
          <div className="settings-card-heading">
            <div><h2>Workspace</h2><p>Preferences are stored locally in this browser.</p></div>
          </div>

          <label className="field-label" htmlFor="api-base">API base URL</label>
          <input id="api-base" className="text-input" value={apiBase} onChange={(event) => setApiBase(event.target.value)} placeholder="/api/v1" />
          <p className="field-help">Use /api/v1 for the deployed Vercel app. A full URL is supported for local development.</p>

          <div className="toggle-row">
            <div><strong>Autosave workflows</strong><span>Keep builder changes saved automatically.</span></div>
            <button className={`toggle ${autoSave ? "on" : ""}`} onClick={() => setAutoSave((value) => !value)} aria-label="Toggle autosave"><span /></button>
          </div>

          <div className="toggle-row">
            <div><strong>Execution notifications</strong><span>Show local success and failure feedback.</span></div>
            <button className={`toggle ${notifications ? "on" : ""}`} onClick={() => setNotifications((value) => !value)} aria-label="Toggle notifications"><span /></button>
          </div>

          <div className="toggle-row">
            <div><strong>Dark workspace</strong><span>Use the operations-style dark interface.</span></div>
            <button className={`toggle ${darkMode ? "on" : ""}`} onClick={() => setDarkMode((value) => !value)} aria-label="Toggle dark workspace"><span /></button>
          </div>

          <button className="primary-button settings-save" onClick={saveSettings}>Save preferences</button>
        </div>

        <div className="settings-card">
          <div className="settings-card-heading">
            <div><h2>AI Copilot</h2><p>AI credentials stay on the backend, never in the browser.</p></div>
            <span className={`status-pill ${aiStatus?.configured ? "connected" : "demo"}`}><span className="status-dot" />{aiStatus?.configured ? "Connected" : "Demo"}</span>
          </div>

          <div className="connection-card">
            <span className="connection-icon">✦</span>
            <div>
              <strong>{aiStatus?.model ?? "gpt-4.1-mini"}</strong>
              <p>{aiStatus?.configured ? "OpenAI API key detected on the server." : "Demo mode is active. Add OPENAI_API_KEY in Vercel Environment Variables for live AI."}</p>
            </div>
          </div>

          <div className="settings-note">
            <strong>Security</strong>
            <p>Do not paste an OpenAI key into the frontend. Configure it only as a server-side environment variable.</p>
          </div>

          <div className="settings-note">
            <strong>AI workflow flow</strong>
            <p>Describe the business process → AI analyzes the goal → the copilot returns a proposed automation plan and implementation checklist.</p>
          </div>
        </div>
      </div>
    </section>
  );
}
