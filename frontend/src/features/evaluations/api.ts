import { api } from "../../lib/api";
import type { EvaluationDetail } from "../../lib/types";

export async function fetchEvaluation(evaluationId: string) {
  const response = await api.get<EvaluationDetail>(`/evaluations/${evaluationId}/`);
  return response.data;
}
