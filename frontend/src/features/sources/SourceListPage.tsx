import { Link, useParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { Badge } from "../../components/ui/Badge";
import { EmptyState } from "../../components/ui/EmptyState";
import { LoadingState } from "../../components/ui/LoadingState";
import { fetchSources } from "./api";

export function SourceListPage() {
  const { workspaceId = "" } = useParams();

  const query = useQuery({
    queryKey: ["sources", workspaceId],
    queryFn: () => fetchSources(workspaceId),
  });

  if (query.isLoading) {
    return <LoadingState label="Loading source documents..." />;
  }

  const sources = query.data?.results ?? [];

  return (
    <section className="page-section">
      <div className="panel__header">
        <div>
          <h1>Source documents</h1>
          <p>Store raw source material and generate excerpts for answer grounding.</p>
        </div>
        <Link className="button" to={`/workspaces/${workspaceId}/sources/new`}>
          Create source
        </Link>
      </div>

      {!sources.length ? (
        <EmptyState
          title="No source documents"
          description="Add the first source document to begin excerpt generation."
        />
      ) : (
        <div className="card-list">
          {sources.map((source) => (
            <Link
              className="list-card"
              key={source.id}
              to={`/workspaces/${workspaceId}/sources/${source.id}`}
            >
              <div className="row-between">
                <h3>{source.title}</h3>
                <Badge tone="info">{source.source_type}</Badge>
              </div>
              <p>Filename: {source.filename || "—"}</p>
              <small>Excerpts: {source.excerpt_count}</small>
            </Link>
          ))}
        </div>
      )}
    </section>
  );
}
