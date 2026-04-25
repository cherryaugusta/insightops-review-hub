import { render, screen } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { SourceDetailPage } from "./SourceDetailPage";
import * as api from "./api";

vi.mock("./api");

describe("SourceDetailPage", () => {
  it("renders excerpt section", async () => {
    vi.mocked(api.fetchSourceDetail).mockResolvedValue({
      id: 10,
      title: "Q2 Market Themes Report",
      source_type: "report",
      filename: "q2-market-themes.pdf",
      source_url: "",
      status: "ready",
      excerpt_count: 1,
      created_at: "",
      updated_at: "",
      raw_text: "Full source text",
      metadata: {},
      excerpts: [],
    });

    vi.mocked(api.fetchExcerpts).mockResolvedValue({
      count: 1,
      next: null,
      previous: null,
      results: [
        {
          id: 1,
          document_id: 10,
          order_index: 1,
          text: "Excerpt text",
          token_count: 10,
          char_start: 0,
          char_end: 50,
        },
      ],
    });

    render(
      <QueryClientProvider client={new QueryClient()}>
        <MemoryRouter initialEntries={["/workspaces/1/sources/10"]}>
          <Routes>
            <Route path="/workspaces/:workspaceId/sources/:sourceId" element={<SourceDetailPage />} />
          </Routes>
        </MemoryRouter>
      </QueryClientProvider>,
    );

    expect(await screen.findByText("Excerpts")).toBeInTheDocument();
    expect(await screen.findByText("Excerpt #1")).toBeInTheDocument();
  });
});
