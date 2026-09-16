import { NavLink } from "react-router-dom";

const menu = [
  { name: "Dashboard", icon: "⌂", path: "/dashboard" },
  { name: "Workflow Builder", icon: "✦", path: "/workflow" },
  { name: "Executions", icon: "▶", path: "/executions" },
  { name: "Execution Logs", icon: "≡", path: "/logs" },
];

const workspace = [
  { name: "AI Copilot", icon: "✧", path: "/ai" },
  { name: "Settings", icon: "⚙", path: "/settings" },
];

export default function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="brand">
        <div className="brand-mark">✦</div>
        <div>
          <strong>AI Workflow</strong>
          <span>Automation Cloud</span>
        </div>
      </div>

      <nav className="sidebar-nav" aria-label="Main navigation">
        <span className="nav-label">OPERATIONS</span>
        {menu.map((item) => (
          <NavLink key={item.path} to={item.path} className={({ isActive }) => `nav-item ${isActive ? "active" : ""}`}>
            <span className="nav-icon">{item.icon}</span>
            <span>{item.name}</span>
          </NavLink>
        ))}

        <span className="nav-label workspace-label">WORKSPACE</span>
        {workspace.map((item) => (
          <NavLink key={item.path} to={item.path} className={({ isActive }) => `nav-item ${isActive ? "active" : ""}`}>
            <span className="nav-icon">{item.icon}</span>
            <span>{item.name}</span>
            {item.path === "/ai" && <span className="nav-badge">AI</span>}
          </NavLink>
        ))}
      </nav>

      <div className="sidebar-footer">
        <span className="online-dot" />
        <div>
          <strong>Workspace online</strong>
          <span>API + scheduler connected</span>
        </div>
      </div>
    </aside>
  );
}
