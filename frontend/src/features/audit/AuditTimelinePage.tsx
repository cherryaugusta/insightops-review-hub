import { useParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { fetchAuditEvents } from "./api";
import { LoadingState } from "../../components/ui/LoadingState";
import { formatDateTime } from "../../lib/utils";

export function AuditTimelinePage() {
  const { workspaceId = "" } = useParams();

  const query = useQuery({
    queryKey: ["audit-events", workspaceId],
    queryFn: () => fetchAuditEvents(workspaceId),
  });

  if (query.isLoading) {
    return <LoadingState label="Loading audit timeline..." />;
  }

  const events = query.data?.results ?? [];

  return (
    <section className="page-section">
      <h1>Audit timeline</h1>

      <div className="timeline">
        {events.map((event) => (
          <div className="timeline-item" key={event.id}>
            <div className="timeline-item__meta">
              <strong>{event.action}</strong>
              <span>{formatDateTime(event.created_at)}</span>
            </div>
            <p>
              Actor: {event.actor_display_name || "System"} · Entity: {event.entity_type} #
              {event.entity_id}
            </p>
            <pre className="text-block text-block--small">
              {JSON.stringify(event.metadata, null, 2)}
            </pre>
          </div>
        ))}
      </div>
    </section>
  );
}
