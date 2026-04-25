import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { WorkspaceListPage } from "./WorkspaceListPage";
import * as api from "./api";

vi.mock("./api");

describe("WorkspaceListPage", () => {
  it("renders workspace list", async () => {
    vi.mocked(api.fetchWorkspaces).mockResolvedValue({
      count: 1,
      next: null,
      previous: null,
      results: [
        {
          id: 1,
          title: "Market Intelligence Workspace",
          slug: "market-intelligence-workspace",
          description: "Workspace for source-backed market briefings.",
          status: "active",
          source_document_count: 5,
          briefing_request_count: 4,
          last_activity_at: null,
          created_at: "",
          updated_at: "",
        },
      ],
    });

    render(
      <QueryClientProvider client={new QueryClient()}>
        <MemoryRouter>
          <WorkspaceListPage />
        </MemoryRouter>
      </QueryClientProvider>,
    );

    expect(await screen.findByText("Market Intelligence Workspace")).toBeInTheDocument();
  });
});
