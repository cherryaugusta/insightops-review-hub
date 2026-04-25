import { api } from "../../lib/api";
import type { AuditEvent, PaginatedResponse } from "../../lib/types";

export async function fetchAuditEvents(workspaceId: string) {
  const response = await api.get<PaginatedResponse<AuditEvent>>(
    `/workspaces/${workspaceId}/audit-events/`,
  );
  return response.data;
}
