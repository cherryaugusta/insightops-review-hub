import { render, screen } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { AuditTimelinePage } from "./AuditTimelinePage";
import * as api from "./api";

vi.mock("./api");

describe("AuditTimelinePage", () => {
  it("renders event list", async () => {
    vi.mocked(api.fetchAuditEvents).mockResolvedValue({
      count: 1,
      next: null,
      previous: null,
      results: [
        {
          id: 1,
          actor_display_name: "Demo Analyst",
          entity_type: "briefing_answer",
          entity_id: 10,
          action: "briefing_answer.generated",
          metadata: { provider: "stub" },
          created_at: "2026-04-20T10:12:00Z",
        },
      ],
    });

    render(
      <QueryClientProvider client={new QueryClient()}>
        <MemoryRouter initialEntries={["/workspaces/1/audit"]}>
          <Routes>
            <Route path="/workspaces/:workspaceId/audit" element={<AuditTimelinePage />} />
          </Routes>
        </MemoryRouter>
      </QueryClientProvider>,
    );

    expect(await screen.findByText("briefing_answer.generated")).toBeInTheDocument();
  });
});
