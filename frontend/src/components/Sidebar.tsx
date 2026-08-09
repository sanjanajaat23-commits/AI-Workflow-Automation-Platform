import { NavLink } from "react-router-dom";

const menu = [
  {
    name: "Dashboard",
    icon: "🏠",
    path: "/",
  },
  {
    name: "Workflow Builder",
    icon: "⚡",
    path: "/workflow",
  },
  {
    name: "Executions",
    icon: "▶",
    path: "/executions",
  },
  {
    name: "Execution Logs",
    icon: "📜",
    path: "/logs",
  },
  {
    name: "AI Assistant",
    icon: "🤖",
    path: "/ai",
  },
  {
    name: "Settings",
    icon: "⚙",
    path: "/settings",
  },
];

export default function Sidebar() {
  return (
    <aside
      style={{
        width: 250,
        background: "#111827",
        color: "white",
        padding: 20,
        display: "flex",
        flexDirection: "column",
      }}
    >
      <h2
        style={{
          marginBottom: 30,
        }}
      >
        ⚡ AI Workflow
      </h2>

      <nav
        style={{
          display: "flex",
          flexDirection: "column",
          gap: 10,
        }}
      >
        {menu.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            style={({ isActive }) => ({
              textDecoration: "none",
              color: "white",
              padding: "12px 14px",
              borderRadius: 8,
              background: isActive
                ? "#2563eb"
                : "transparent",
              transition: "0.2s",
            })}
          >
            {item.icon} {item.name}
          </NavLink>
        ))}
      </nav>
    </aside>
  );
}