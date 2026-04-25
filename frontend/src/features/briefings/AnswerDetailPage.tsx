import type { FormEvent } from "react";
import { useMemo, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { useMutation, useQueries, useQuery, useQueryClient } from "@tanstack/react-query";
import { fetchWorkspaces } from "../workspaces/api";
import { fetchBriefingDetail, fetchBriefings, submitReviewDecision } from "./api";
import { LoadingState } from "../../components/ui/LoadingState";
import { Badge } from "../../components/ui/Badge";

export function AnswerDetailPage() {
  const { answerId = "" } = useParams();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const [decision, setDecision] = useState<"approved" | "changes_requested" | "rejected">(
    "approved",
  );
  const [comment, setComment] = useState("Suitable for sharing.");

  const workspacesQuery = useQuery({
    queryKey: ["answer-detail-workspaces"],
    queryFn: () => fetchWorkspaces(),
  });

  const workspaceIds = useMemo(
    () => (workspacesQuery.data?.results ?? []).map((workspace) => String(workspace.id)),
    [workspacesQuery.data],
  );

  const briefingsQueries = useQueries({
    queries: workspaceIds.map((workspaceId) => ({
      queryKey: ["answer-detail-briefings", workspaceId],
      queryFn: () => fetchBriefings(workspaceId),
      enabled: workspaceIds.length > 0,
    })),
  });

  const combined = useMemo(() => {
    for (let index = 0; index < workspaceIds.length; index += 1) {
      const workspaceId = workspaceIds[index];
      const briefings = briefingsQueries[index]?.data?.results ?? [];
      for (const briefing of briefings) {
        if (briefing.latest_answer_id === Number(answerId)) {
          return { workspaceId, briefingId: String(briefing.id) };
        }
      }
    }
    return null;
  }, [workspaceIds, briefingsQueries, answerId]);

  const briefingDetailQuery = useQuery({
    queryKey: ["answer-detail-briefing-detail", combined?.workspaceId, combined?.briefingId],
    queryFn: async () => {
      if (!combined) return null;
      return fetchBriefingDetail(combined.workspaceId, combined.briefingId);
    },
    enabled: Boolean(combined),
  });

  const answer = briefingDetailQuery.data?.answers.find((item) => String(item.id) === answerId);

  const mutation = useMutation({
    mutationFn: () =>
      submitReviewDecision(answerId, {
        decision,
        comment,
      }),
    onSuccess: async () => {
      if (combined) {
        await queryClient.invalidateQueries({
          queryKey: ["answer-detail-briefing-detail", combined.workspaceId, combined.briefingId],
        });
      }
    },
  });

  function handleSubmit(event: FormEvent) {
    event.preventDefault();
    mutation.mutate();
  }

  const isBriefingsLoading = briefingsQueries.some((query) => query.isLoading);

  if (workspacesQuery.isLoading || isBriefingsLoading || briefingDetailQuery.isLoading) {
    return <LoadingState label="Loading answer detail..." />;
  }

  if (!answer) {
    return <div>Answer not found.</div>;
  }

  return (
    <section className="page-section">
      <div className="panel__header">
        <div>
          <h1>Answer detail</h1>
          <p>Inspect generated answer text, citations, evaluation link, and review actions.</p>
        </div>
        {answer.latest_evaluation ? (
          <Link className="button" to={`/evaluations/${answer.latest_evaluation.id}`}>
            Open evaluation
          </Link>
        ) : null}
      </div>

      <section className="panel">
        <div className="row-between">
          <h2>Generated answer</h2>
          <Badge tone="info">{answer.confidence_band}</Badge>
        </div>
        <pre className="text-block">{answer.answer_text}</pre>
      </section>

      <section className="panel">
        <h2>Citations</h2>
        <div className="card-list">
          {answer.citations.map((citation) => (
            <div className="list-card" key={citation.id}>
              <div className="row-between">
                <h3>{citation.document_title}</h3>
                <Badge tone="info">Rank {citation.relevance_rank}</Badge>
              </div>
              <p>{citation.excerpt_text}</p>
              <small>{citation.rationale}</small>
            </div>
          ))}
        </div>
      </section>

      <section className="panel">
        <h2>Submit review decision</h2>
        <form className="form-grid" onSubmit={handleSubmit}>
          <label>
            Decision
            <select
              value={decision}
              onChange={(e) =>
                setDecision(
                  e.target.value as "approved" | "changes_requested" | "rejected",
                )
              }
            >
              <option value="approved">approved</option>
              <option value="changes_requested">changes_requested</option>
              <option value="rejected">rejected</option>
            </select>
          </label>

          <label>
            Comment
            <textarea
              rows={4}
              value={comment}
              onChange={(e) => setComment(e.target.value)}
            />
          </label>

          <button className="button" type="submit" disabled={mutation.isPending}>
            {mutation.isPending ? "Saving decision..." : "Submit review decision"}
          </button>
        </form>
      </section>

      <div className="actions-row">
        <button className="button button--secondary" onClick={() => navigate(-1)}>
          Back
        </button>
      </div>
    </section>
  );
}
