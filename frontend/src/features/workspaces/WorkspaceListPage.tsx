import { useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { Badge } from "../../components/ui/Badge";
import { EmptyState } from "../../components/ui/EmptyState";
import { LoadingState } from "../../components/ui/LoadingState";
import { fetchWorkspaces } from "./api";

export function WorkspaceListPage() {
  const [search, setSearch] = useState("");

  const query = useQuery({
    queryKey: ["workspaces", search],
    queryFn: () => fetchWorkspaces(search),
  });

  const results = useMemo(() => query.data?.results ?? [], [query.data]);

  if (query.isLoading) {
    return <LoadingState label="Loading workspaces..." />;
  }

  return (
    <section className="page-section">
      <div className="panel__header">
        <div>
          <h1>Workspaces</h1>
          <p>Operational containers for source packs, briefings, answers, and audit history.</p>
        </div>
        <Link className="button" to="/workspaces/new">
          Create workspace
        </Link>
      </div>

      <div className="toolbar">
        <input
          value={search}
          onChange={(event) => setSearch(event.target.value)}
          placeholder="Search title, description, or slug"
        />
      </div>

      {!results.length ? (
        <EmptyState
          title="No workspaces found"
          description="Create a workspace to begin storing source material and generating reviewable answers."
        />
      ) : (
        <div className="card-list">
          {results.map((workspace) => (
            <div className="list-card" key={workspace.id}>
              <div className="row-between">
                <h3>{workspace.title}</h3>
                <Badge tone={workspace.status === "active" ? "success" : "warning"}>
                  {workspace.status}
                </Badge>
              </div>
              <p>{workspace.description || "No description provided."}</p>
              <small>
                Sources: {workspace.source_document_count} · Briefings:{" "}
                {workspace.briefing_request_count}
              </small>
              <div className="actions-row">
                <Link className="button button--secondary" to={`/workspaces/${workspace.id}`}>
                  Open
                </Link>
                <Link className="button button--secondary" to={`/workspaces/${workspace.id}/edit`}>
                  Edit
                </Link>
              </div>
            </div>
          ))}
        </div>
      )}
    </section>
  );
}
