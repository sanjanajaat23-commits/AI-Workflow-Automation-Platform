import "./App.css";

import { Navigate, Route, Routes } from "react-router-dom";
import Sidebar from "./components/Sidebar";
import Dashboard from "./pages/Dashboard";
import WorkflowBuilder from "./workflow/WorkflowBuilder";
import Executions from "./pages/Executions";
import Logs from "./pages/Logs";
import AIAssistant from "./pages/AIAssistant";
import Settings from "./pages/Settings";

export default function App() {
  return (
    <div className="layout">
      <Sidebar />
      <main className="content">
        <Routes>
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/workflow/:workflowId?" element={<WorkflowBuilder />} />
          <Route path="/executions" element={<Executions />} />
          <Route path="/logs" element={<Logs />} />
          <Route path="/ai" element={<AIAssistant />} />
          <Route path="/settings" element={<Settings />} />
        </Routes>
      </main>
    </div>
  );
}
