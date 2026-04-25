import { Link, useParams } from "react-router-dom";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { fetchBriefingDetail, generateAnswer } from "./api";
import { LoadingState } from "../../components/ui/LoadingState";
import { Badge } from "../../components/ui/Badge";

export function BriefingDetailPage() {
  const { workspaceId = "", briefingId = "" } = useParams();
  const queryClient = useQueryClient();

  const query = useQuery({
    queryKey: ["briefing-detail", workspaceId, briefingId],
    queryFn: () => fetchBriefingDetail(workspaceId, briefingId),
  });

  const mutation = useMutation({
    mutationFn: () => generateAnswer(briefingId),
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: ["briefing-detail", workspaceId, briefingId] });
      await queryClient.invalidateQueries({ queryKey: ["briefings", workspaceId] });
    },
  });

  if (query.isLoading) {
    return <LoadingState label="Loading briefing..." />;
  }

  const briefing = query.data;
  if (!briefing) {
    return <div>Briefing not found.</div>;
  }

  const latestAnswer = briefing.answers[0];

  return (
    <section className="page-section">
      <div className="panel__header">
        <div>
          <h1>{briefing.title}</h1>
          <p>{briefing.question}</p>
        </div>
        <button className="button" onClick={() => mutation.mutate()} disabled={mutation.isPending}>
          {mutation.isPending ? "Generating answer..." : "Generate answer"}
        </button>
      </div>

      <div className="detail-card">
        <p><strong>Audience:</strong> {briefing.audience || "—"}</p>
        <p><strong>Goal:</strong> {briefing.goal || "—"}</p>
        <p><strong>Status:</strong> <Badge tone="info">{briefing.status}</Badge></p>
      </div>

      <section className="panel">
        <h2>Answers</h2>
        <div className="card-list">
          {briefing.answers.map((answer) => (
            <div className="list-card" key={answer.id}>
              <div className="row-between">
                <h3>Answer #{answer.id}</h3>
                <Badge tone="info">{answer.confidence_band}</Badge>
              </div>
              <p>{answer.answer_text.slice(0, 280)}...</p>
              <div className="actions-row">
                <Link className="button button--secondary" to={`/answers/${answer.id}`}>
                  Open answer
                </Link>
                {answer.latest_evaluation ? (
                  <Link
                    className="button button--secondary"
                    to={`/evaluations/${answer.latest_evaluation.id}`}
                  >
                    Open evaluation
                  </Link>
                ) : null}
              </div>
            </div>
          ))}
        </div>
      </section>

      {latestAnswer?.latest_evaluation ? (
        <section className="panel">
          <h2>Latest evaluation summary</h2>
          <p><strong>Verdict:</strong> {latestAnswer.latest_evaluation.verdict}</p>
          <p><strong>Overall score:</strong> {latestAnswer.latest_evaluation.overall_score}</p>
          <p><strong>Notes:</strong> {latestAnswer.latest_evaluation.notes}</p>
        </section>
      ) : null}

      {latestAnswer?.latest_review_decision ? (
        <section className="panel">
          <h2>Latest review decision</h2>
          <p><strong>Decision:</strong> {latestAnswer.latest_review_decision.decision}</p>
          <p><strong>Comment:</strong> {latestAnswer.latest_review_decision.comment}</p>
        </section>
      ) : null}
    </section>
  );
}
