import { NavLink } from "react-router-dom";
import { LayoutDashboard, TrendingUp, Newspaper, Key, FileText } from "lucide-react";

const links = [
  { to: "/", label: "Overview", icon: LayoutDashboard },
  { to: "/trends", label: "Trends", icon: TrendingUp },
  { to: "/sources", label: "Sources", icon: Newspaper },
  { to: "/keywords", label: "Keywords", icon: Key },
  { to: "/articles", label: "Articles", icon: FileText },
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
            <l.icon size={18} className="nav-icon" />
            {l.label}
          </NavLink>
        ))}
      </nav>
    </aside>
  );
}
