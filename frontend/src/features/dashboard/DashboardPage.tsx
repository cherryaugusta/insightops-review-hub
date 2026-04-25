import { Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { StatCard } from "../../components/ui/StatCard";
import { LoadingState } from "../../components/ui/LoadingState";
import { fetchWorkspaces } from "../workspaces/api";

export function DashboardPage() {
  const query = useQuery({
    queryKey: ["workspaces", "dashboard"],
    queryFn: () => fetchWorkspaces(),
  });

  if (query.isLoading) {
    return <LoadingState label="Loading dashboard..." />;
  }

  const workspaces = query.data?.results ?? [];
  const workspaceCount = workspaces.length;
  const sourceCount = workspaces.reduce((sum, item) => sum + item.source_document_count, 0);
  const briefingCount = workspaces.reduce((sum, item) => sum + item.briefing_request_count, 0);

  return (
    <section className="page-section">
      <h1>Dashboard</h1>

      <div className="stats-grid">
        <StatCard label="Workspaces" value={workspaceCount} />
        <StatCard label="Source documents" value={sourceCount} />
        <StatCard label="Briefings" value={briefingCount} />
        <StatCard label="Review queue" value="Evaluation driven" />
      </div>

      <section className="panel">
        <div className="panel__header">
          <h2>Recent workspaces</h2>
          <Link className="button" to="/workspaces">
            Open workspaces
          </Link>
        </div>

        <div className="card-list">
          {workspaces.map((workspace) => (
            <Link
              key={workspace.id}
              className="list-card"
              to={`/workspaces/${workspace.id}`}
            >
              <h3>{workspace.title}</h3>
              <p>{workspace.description || "No description provided."}</p>
              <small>
                Sources: {workspace.source_document_count} · Briefings:{" "}
                {workspace.briefing_request_count}
              </small>
            </Link>
          ))}
        </div>
      </section>
    </section>
  );
}
