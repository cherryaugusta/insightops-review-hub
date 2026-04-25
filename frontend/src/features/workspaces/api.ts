import { api } from "../../lib/api";
import type { PaginatedResponse, WorkspaceDetail, WorkspaceSummary } from "../../lib/types";

export interface WorkspacePayload {
  title: string;
  slug: string;
  description: string;
  status?: "active" | "archived";
}

export async function fetchWorkspaces(search?: string, status?: string) {
  const response = await api.get<PaginatedResponse<WorkspaceSummary>>("/workspaces/", {
    params: {
      search: search || undefined,
      status: status || undefined,
    },
  });
  return response.data;
}

export async function fetchWorkspaceDetail(workspaceId: string) {
  const response = await api.get<WorkspaceDetail>(`/workspaces/${workspaceId}/`);
  return response.data;
}

export async function createWorkspace(payload: WorkspacePayload) {
  const response = await api.post("/workspaces/", payload);
  return response.data;
}

export async function updateWorkspace(workspaceId: string, payload: Partial<WorkspacePayload>) {
  const response = await api.patch(`/workspaces/${workspaceId}/`, payload);
  return response.data;
}

export async function deleteWorkspace(workspaceId: string) {
  const response = await api.delete(`/workspaces/${workspaceId}/`);
  return response.data;
}
