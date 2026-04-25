import { useParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { fetchEvaluation } from "./api";
import { LoadingState } from "../../components/ui/LoadingState";
import { ScorePill } from "../../components/ui/ScorePill";

export function EvaluationDetailPage() {
  const { evaluationId = "" } = useParams();

  const query = useQuery({
    queryKey: ["evaluation", evaluationId],
    queryFn: () => fetchEvaluation(evaluationId),
  });

  if (query.isLoading) {
    return <LoadingState label="Loading evaluation..." />;
  }

  const evaluation = query.data;
  if (!evaluation) {
    return <div>Evaluation not found.</div>;
  }

  return (
    <section className="page-section">
      <h1>Evaluation detail</h1>

      <div className="stats-grid">
        <ScorePill label="Groundedness" score={evaluation.groundedness_score} />
        <ScorePill label="Citation coverage" score={evaluation.citation_coverage_score} />
        <ScorePill label="Completeness" score={evaluation.completeness_score} />
        <ScorePill
          label="Overall"
          score={evaluation.overall_score}
          verdict={evaluation.verdict}
        />
      </div>

      <section className="panel">
        <h2>Evaluation metadata</h2>
        <p><strong>Verdict:</strong> {evaluation.verdict}</p>
        <p><strong>Evaluator type:</strong> {evaluation.evaluator_type}</p>
        <p><strong>Notes:</strong> {evaluation.notes}</p>
      </section>
    </section>
  );
}
