import { Link, useParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { StatCard } from "../../components/ui/StatCard";
import { LoadingState } from "../../components/ui/LoadingState";
import { fetchWorkspaceDetail } from "./api";
import { fetchSources } from "../sources/api";
import { fetchBriefings } from "../briefings/api";

export function WorkspaceDetailPage() {
  const { workspaceId = "" } = useParams();

  const workspaceQuery = useQuery({
    queryKey: ["workspace", workspaceId],
    queryFn: () => fetchWorkspaceDetail(workspaceId),
  });

  const sourcesQuery = useQuery({
    queryKey: ["workspace-sources", workspaceId],
    queryFn: () => fetchSources(workspaceId),
  });

  const briefingsQuery = useQuery({
    queryKey: ["workspace-briefings", workspaceId],
    queryFn: () => fetchBriefings(workspaceId),
  });

  if (workspaceQuery.isLoading || sourcesQuery.isLoading || briefingsQuery.isLoading) {
    return <LoadingState label="Loading workspace..." />;
  }

  const workspace = workspaceQuery.data;
  const sources = sourcesQuery.data?.results ?? [];
  const briefings = briefingsQuery.data?.results ?? [];

  if (!workspace) {
    return <div>Workspace not found.</div>;
  }

  return (
    <section className="page-section">
      <div className="panel__header">
        <div>
          <h1>{workspace.title}</h1>
          <p>{workspace.description || "No description provided."}</p>
        </div>
        <div className="actions-row">
          <Link className="button button--secondary" to={`/workspaces/${workspaceId}/edit`}>
            Edit workspace
          </Link>
          <Link className="button button--secondary" to={`/workspaces/${workspaceId}/audit`}>
            Open audit
          </Link>
        </div>
      </div>

      <div className="stats-grid">
        <StatCard label="Source documents" value={workspace.source_document_count} />
        <StatCard label="Briefings" value={workspace.briefing_request_count} />
        <StatCard label="Evaluations" value={workspace.evaluation_run_count} />
        <StatCard label="Latest review" value={workspace.latest_review_decision || "—"} />
      </div>

      <div className="link-cluster">
        <Link className="button" to={`/workspaces/${workspaceId}/sources`}>
          Sources
        </Link>
        <Link className="button" to={`/workspaces/${workspaceId}/briefings`}>
          Briefings
        </Link>
        <Link className="button" to={`/workspaces/${workspaceId}/audit`}>
          Audit
        </Link>
      </div>

      <div className="two-column">
        <section className="panel">
          <div className="panel__header">
            <h2>Recent sources</h2>
            <Link className="button button--secondary" to={`/workspaces/${workspaceId}/sources/new`}>
              Add source
            </Link>
          </div>
          <div className="card-list">
            {sources.slice(0, 5).map((source) => (
              <Link
                key={source.id}
                className="list-card"
                to={`/workspaces/${workspaceId}/sources/${source.id}`}
              >
                <h3>{source.title}</h3>
                <p>{source.source_type}</p>
                <small>Excerpts: {source.excerpt_count}</small>
              </Link>
            ))}
          </div>
        </section>

        <section className="panel">
          <div className="panel__header">
            <h2>Recent briefings</h2>
            <Link className="button button--secondary" to={`/workspaces/${workspaceId}/briefings/new`}>
              New briefing
            </Link>
          </div>
          <div className="card-list">
            {briefings.slice(0, 5).map((briefing) => (
              <Link
                key={briefing.id}
                className="list-card"
                to={`/workspaces/${workspaceId}/briefings/${briefing.id}`}
              >
                <h3>{briefing.title}</h3>
                <p>{briefing.question}</p>
                <small>Status: {briefing.status}</small>
              </Link>
            ))}
          </div>
        </section>
      </div>
    </section>
  );
}
