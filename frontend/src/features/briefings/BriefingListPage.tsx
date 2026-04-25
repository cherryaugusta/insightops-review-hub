import { Link, useParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { Badge } from "../../components/ui/Badge";
import { LoadingState } from "../../components/ui/LoadingState";
import { EmptyState } from "../../components/ui/EmptyState";
import { fetchBriefings } from "./api";

function verdictTone(verdict: string | null) {
  if (verdict === "pass") return "success";
  if (verdict === "fail") return "danger";
  if (verdict === "review") return "warning";
  return "neutral";
}

export function BriefingListPage() {
  const { workspaceId = "" } = useParams();

  const query = useQuery({
    queryKey: ["briefings", workspaceId],
    queryFn: () => fetchBriefings(workspaceId),
  });

  if (query.isLoading) {
    return <LoadingState label="Loading briefings..." />;
  }

  const briefings = query.data?.results ?? [];

  return (
    <section className="page-section">
      <div className="panel__header">
        <div>
          <h1>Briefing requests</h1>
          <p>Create questions, generate answers, inspect evaluations, and capture reviews.</p>
        </div>
        <Link className="button" to={`/workspaces/${workspaceId}/briefings/new`}>
          New briefing
        </Link>
      </div>

      {!briefings.length ? (
        <EmptyState
          title="No briefings"
          description="Create a briefing request to generate a citation-backed answer."
        />
      ) : (
        <div className="card-list">
          {briefings.map((briefing) => (
            <Link
              key={briefing.id}
              className="list-card"
              to={`/workspaces/${workspaceId}/briefings/${briefing.id}`}
            >
              <div className="row-between">
                <h3>{briefing.title}</h3>
                <Badge tone="info">{briefing.status}</Badge>
              </div>
              <p>{briefing.question}</p>
              <div className="actions-row">
                <Badge tone={verdictTone(briefing.latest_evaluation_verdict)}>
                  {briefing.latest_evaluation_verdict || "no verdict"}
                </Badge>
              </div>
            </Link>
          ))}
        </div>
      )}
    </section>
  );
}
