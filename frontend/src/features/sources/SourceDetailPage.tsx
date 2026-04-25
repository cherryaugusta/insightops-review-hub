import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useParams } from "react-router-dom";
import { generateExcerpts, fetchExcerpts, fetchSourceDetail } from "./api";
import { LoadingState } from "../../components/ui/LoadingState";
import { Badge } from "../../components/ui/Badge";

export function SourceDetailPage() {
  const { workspaceId = "", sourceId = "" } = useParams();
  const queryClient = useQueryClient();

  const sourceQuery = useQuery({
    queryKey: ["source", workspaceId, sourceId],
    queryFn: () => fetchSourceDetail(workspaceId, sourceId),
  });

  const excerptsQuery = useQuery({
    queryKey: ["source-excerpts", sourceId],
    queryFn: () => fetchExcerpts(sourceId),
  });

  const mutation = useMutation({
    mutationFn: () => generateExcerpts(sourceId),
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: ["source", workspaceId, sourceId] });
      await queryClient.invalidateQueries({ queryKey: ["source-excerpts", sourceId] });
      await queryClient.invalidateQueries({ queryKey: ["sources", workspaceId] });
    },
  });

  if (sourceQuery.isLoading || excerptsQuery.isLoading) {
    return <LoadingState label="Loading source detail..." />;
  }

  const source = sourceQuery.data;
  const excerpts = excerptsQuery.data?.results ?? [];

  if (!source) {
    return <div>Source document not found.</div>;
  }

  return (
    <section className="page-section">
      <div className="panel__header">
        <div>
          <h1>{source.title}</h1>
          <p>Detailed source record and excerpt generation control.</p>
        </div>
        <button className="button" onClick={() => mutation.mutate()} disabled={mutation.isPending}>
          {mutation.isPending ? "Generating excerpts..." : "Generate excerpts"}
        </button>
      </div>

      <div className="detail-card">
        <p><strong>Type:</strong> <Badge tone="info">{source.source_type}</Badge></p>
        <p><strong>Filename:</strong> {source.filename || "—"}</p>
        <p><strong>Source URL:</strong> {source.source_url || "—"}</p>
        <p><strong>Status:</strong> {source.status}</p>
        <p><strong>Excerpt count:</strong> {source.excerpt_count}</p>
      </div>

      <section className="panel">
        <h2>Raw text</h2>
        <pre className="text-block">{source.raw_text}</pre>
      </section>

      <section className="panel">
        <h2>Excerpts</h2>
        <div className="card-list">
          {excerpts.map((excerpt) => (
            <div className="list-card" key={excerpt.id}>
              <h3>Excerpt #{excerpt.order_index}</h3>
              <p>{excerpt.text}</p>
              <small>
                Tokens: {excerpt.token_count} · Range: {excerpt.char_start}–{excerpt.char_end}
              </small>
            </div>
          ))}
        </div>
      </section>
    </section>
  );
}
