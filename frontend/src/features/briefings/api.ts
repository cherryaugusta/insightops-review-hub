import { api } from "../../lib/api";
import type { BriefingDetail, BriefingSummary, PaginatedResponse } from "../../lib/types";

export interface BriefingPayload {
  title: string;
  question: string;
  audience: string;
  goal: string;
  status?: "draft" | "processing" | "ready" | "needs_review";
}

export async function fetchBriefings(workspaceId: string) {
  const response = await api.get<PaginatedResponse<BriefingSummary>>(
    `/workspaces/${workspaceId}/briefings/`,
  );
  return response.data;
}

export async function fetchBriefingDetail(workspaceId: string, briefingId: string) {
  const response = await api.get<BriefingDetail>(
    `/workspaces/${workspaceId}/briefings/${briefingId}/`,
  );
  return response.data;
}

export async function createBriefing(workspaceId: string, payload: BriefingPayload) {
  const response = await api.post(`/workspaces/${workspaceId}/briefings/`, payload);
  return response.data;
}

export async function updateBriefing(
  workspaceId: string,
  briefingId: string,
  payload: Partial<BriefingPayload>,
) {
  const response = await api.patch(
    `/workspaces/${workspaceId}/briefings/${briefingId}/`,
    payload,
  );
  return response.data;
}

export async function deleteBriefing(workspaceId: string, briefingId: string) {
  const response = await api.delete(`/workspaces/${workspaceId}/briefings/${briefingId}/`);
  return response.data;
}

export async function generateAnswer(briefingId: string) {
  const response = await api.post(`/briefings/${briefingId}/generate-answer/`);
  return response.data as {
    briefing_request_id: number;
    answer_id: number;
    evaluation_run_id: number;
    status: string;
  };
}

export async function submitReviewDecision(
  answerId: string,
  payload: {
    decision: "approved" | "changes_requested" | "rejected";
    comment: string;
  },
) {
  const response = await api.post(`/answers/${answerId}/review-decisions/`, payload);
  return response.data;
}
