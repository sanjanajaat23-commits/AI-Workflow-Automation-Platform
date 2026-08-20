import "./App.css";

import {
  Navigate,
  Route,
  Routes,
} from "react-router-dom";

import Sidebar from "./components/Sidebar";

import Dashboard from "./pages/Dashboard";
import WorkflowBuilder from "./workflow/WorkflowBuilder";
import Executions from "./pages/Executions";
import Logs from "./pages/Logs";

function Placeholder({
  title,
}: {
  title: string;
}) {
  return (
    <div style={{ padding: 40 }}>
      <h1>{title}</h1>
      <p>Coming Soon...</p>
    </div>
  );
}

export default function App() {
  return (
    <div className="layout">
      <Sidebar />

      <main className="content">
        <Routes>
          <Route
            path="/"
            element={<Navigate to="/dashboard" replace />}
          />

          <Route
            path="/dashboard"
            element={<Dashboard />}
          />

          <Route
            path="/workflow/:workflowId?"
            element={<WorkflowBuilder />}
          />

          <Route
            path="/executions"
            element={<Executions />}
          />

          <Route
            path="/logs"
            element={<Logs />}
          />

          <Route
            path="/ai"
            element={
              <Placeholder title="AI Assistant" />
            }
          />

          <Route
            path="/settings"
            element={
              <Placeholder title="Settings" />
            }
          />
        </Routes>
      </main>
    </div>
  );
}