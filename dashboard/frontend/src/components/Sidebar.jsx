import { NavLink } from "react-router-dom";

const links = [
  { to: "/", label: "Overview", icon: "📊" },
  { to: "/trends", label: "Trends", icon: "📈" },
  { to: "/sources", label: "Sources", icon: "📰" },
  { to: "/keywords", label: "Keywords", icon: "🔑" },
  { to: "/articles", label: "Articles", icon: "📝" },
];

export default function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="sidebar-brand">
        <img src="/logo.png" alt="MediaPulse" className="sidebar-logo" />
        <span>MediaPulse</span>
      </div>
      <nav>
        {links.map((l) => (
          <NavLink
            key={l.to}
            to={l.to}
            className={({ isActive }) => (isActive ? "nav-link active" : "nav-link")}
          >
            <span className="nav-icon">{l.icon}</span>
            {l.label}
          </NavLink>
        ))}
      </nav>
    </aside>
  );
}
