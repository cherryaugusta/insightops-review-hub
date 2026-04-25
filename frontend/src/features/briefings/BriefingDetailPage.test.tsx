import { render, screen } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BriefingDetailPage } from "./BriefingDetailPage";
import * as api from "./api";

vi.mock("./api");

describe("BriefingDetailPage", () => {
  it("renders generate answer control", async () => {
    vi.mocked(api.fetchBriefingDetail).mockResolvedValue({
      id: 1,
      title: "Summarise the main customer risks",
      question: "What are the main customer risks?",
      audience: "Operations Lead",
      goal: "Prepare an executive summary.",
      status: "draft",
      answers: [],
      created_at: "",
      updated_at: "",
    });

    render(
      <QueryClientProvider client={new QueryClient()}>
        <MemoryRouter initialEntries={["/workspaces/1/briefings/1"]}>
          <Routes>
            <Route path="/workspaces/:workspaceId/briefings/:briefingId" element={<BriefingDetailPage />} />
          </Routes>
        </MemoryRouter>
      </QueryClientProvider>,
    );

    expect(await screen.findByRole("button", { name: /generate answer/i })).toBeInTheDocument();
  });
});
