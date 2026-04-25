import { useMemo } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { useAuthStore } from "../../features/auth/store";

function getPageLabel(pathname: string): string {
  if (pathname.startsWith("/dashboard")) return "Dashboard";
  if (pathname.startsWith("/workspaces")) return "Workspace Operations";
  if (pathname.startsWith("/answers/")) return "Answer Detail";
  if (pathname.startsWith("/evaluations/")) return "Evaluation Detail";
  if (pathname.startsWith("/profile")) return "Profile";
  return "InsightOps Review Hub";
}

export function Topbar() {
  const location = useLocation();
  const navigate = useNavigate();
  const { user, logout } = useAuthStore();

  const label = useMemo(() => getPageLabel(location.pathname), [location.pathname]);

  return (
    <header className="topbar">
      <div>
        <div className="eyebrow">Internal control surface</div>
        <h2>{label}</h2>
      </div>

      <div className="topbar__actions">
        <div className="topbar__identity">
          <strong>{user?.display_name ?? "Signed in user"}</strong>
          <span>{user?.email ?? "No email loaded"}</span>
        </div>
        <button
          className="button button--secondary"
          onClick={() => {
            logout();
            navigate("/login");
          }}
        >
          Logout
        </button>
      </div>
    </header>
  );
}
