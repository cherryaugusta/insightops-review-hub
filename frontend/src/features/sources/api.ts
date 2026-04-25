import { api } from "../../lib/api";
import type {
  PaginatedResponse,
  SourceDocumentDetail,
  SourceDocumentSummary,
  SourceExcerpt,
} from "../../lib/types";

export interface SourcePayload {
  title: string;
  source_type: string;
  filename: string;
  source_url: string;
  raw_text: string;
  status?: "draft" | "ready" | "archived";
  metadata?: Record<string, unknown>;
}

export async function fetchSources(workspaceId: string) {
  const response = await api.get<PaginatedResponse<SourceDocumentSummary>>(
    `/workspaces/${workspaceId}/sources/`,
  );
  return response.data;
}

export async function fetchSourceDetail(workspaceId: string, sourceId: string) {
  const response = await api.get<SourceDocumentDetail>(
    `/workspaces/${workspaceId}/sources/${sourceId}/`,
  );
  return response.data;
}

export async function createSource(workspaceId: string, payload: SourcePayload) {
  const response = await api.post(`/workspaces/${workspaceId}/sources/`, payload);
  return response.data;
}

export async function updateSource(
  workspaceId: string,
  sourceId: string,
  payload: Partial<SourcePayload>,
) {
  const response = await api.patch(`/workspaces/${workspaceId}/sources/${sourceId}/`, payload);
  return response.data;
}

export async function deleteSource(workspaceId: string, sourceId: string) {
  const response = await api.delete(`/workspaces/${workspaceId}/sources/${sourceId}/`);
  return response.data;
}

export async function generateExcerpts(sourceId: string) {
  const response = await api.post(`/sources/${sourceId}/generate-excerpts/`);
  return response.data as {
    source_document_id: number;
    created_excerpt_count: number;
    status: string;
  };
}

export async function fetchExcerpts(sourceId: string) {
  const response = await api.get<PaginatedResponse<SourceExcerpt>>(`/sources/${sourceId}/excerpts/`);
  return response.data;
}
