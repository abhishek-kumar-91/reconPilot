import {
  Activity,
  Boxes,
  Code2,
  Cpu,
  FolderKanban,
  Gauge,
  Globe2,
  ListChecks,
  Network,
  Radar,
  Settings,
} from "lucide-react";
import { NavLink } from "react-router-dom";

const primaryLinks = [
  { to: "/dashboard", label: "Dashboard", icon: Gauge },
  { to: "/projects", label: "Projects", icon: FolderKanban },
  { to: "/assets", label: "Assets", icon: Globe2 },
  { to: "/endpoints", label: "Endpoints", icon: Network },
  { to: "/javascript", label: "JavaScript", icon: Code2 },
  { to: "/apis", label: "APIs", icon: Boxes },
  { to: "/technologies", label: "Technologies", icon: Cpu },
  { to: "/testing-queue", label: "Testing Queue", icon: ListChecks },
];

export function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="brand">
        <div className="brand-mark"><Radar size={22} /></div>
        <div>
          <div className="brand-name">ReconPilot</div>
          <div className="brand-subtitle">Security Recon</div>
        </div>
      </div>

      <div className="sidebar-section-label">Workspace</div>
      <nav className="sidebar-nav">
        {primaryLinks.map(({ to, label, icon: Icon }) => (
          <NavLink
            key={to}
            to={to}
            className={({ isActive }) =>
              `nav-item ${isActive ? "active" : ""}`
            }
          >
            <Icon size={18} />
            <span>{label}</span>
          </NavLink>
        ))}
      </nav>

      <div className="sidebar-spacer" />

      <div className="scope-card">
        <div className="scope-card-title">
          <Activity size={15} />
          Authorized testing
        </div>
        <p>Keep targets inside the defined program scope.</p>
      </div>

      <NavLink
        to="/settings"
        className={({ isActive }) =>
          `nav-item ${isActive ? "active" : ""}`
        }
      >
        <Settings size={18} />
        <span>Settings</span>
      </NavLink>

      <div className="sidebar-footer">
        <span>v0.1.0</span>
        <span>Built by Abhishek Kumar</span>
      </div>
    </aside>
  );
}