import { NavLink } from "react-router-dom";

export function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="sidebar__brand">
        <h1>InsightOps</h1>
        <p>Review Hub</p>
      </div>

      <nav className="sidebar__nav">
        <NavLink to="/dashboard" className="nav-link">
          Dashboard
        </NavLink>
        <NavLink to="/workspaces" className="nav-link">
          Workspaces
        </NavLink>
        <NavLink to="/profile" className="nav-link">
          Profile
        </NavLink>
      </nav>
    </aside>
  );
}
