import { render, screen } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { AnswerDetailPage } from "./AnswerDetailPage";
import * as workspaceApi from "../workspaces/api";
import * as briefingApi from "./api";

vi.mock("../workspaces/api");
vi.mock("./api");

describe("AnswerDetailPage", () => {
  it("renders citations", async () => {
    vi.mocked(workspaceApi.fetchWorkspaces).mockResolvedValue({
      count: 1,
      next: null,
      previous: null,
      results: [
        {
          id: 1,
          title: "Workspace",
          slug: "workspace",
          description: "Desc",
          status: "active",
          source_document_count: 1,
          briefing_request_count: 1,
          last_activity_at: null,
          created_at: "",
          updated_at: "",
        },
      ],
    });

    vi.mocked(briefingApi.fetchBriefings).mockResolvedValue({
      count: 1,
      next: null,
      previous: null,
      results: [
        {
          id: 9,
          title: "Briefing",
          question: "Question",
          audience: "Audience",
          goal: "Goal",
          status: "ready",
          latest_answer_id: 5,
          latest_evaluation_verdict: "pass",
          created_at: "",
          updated_at: "",
        },
      ],
    });

    vi.mocked(briefingApi.fetchBriefingDetail).mockResolvedValue({
      id: 9,
      title: "Briefing",
      question: "Question",
      audience: "Audience",
      goal: "Goal",
      status: "ready",
      created_at: "",
      updated_at: "",
      answers: [
        {
          id: 5,
          provider: "stub",
          model_name: "keyword-overlap-v1",
          answer_text: "Answer text",
          confidence_band: "medium",
          status: "generated",
          generation_notes: "",
          created_at: "",
          latest_evaluation: {
            id: 3,
            groundedness_score: "0.90",
            citation_coverage_score: "0.95",
            completeness_score: "0.85",
            overall_score: "0.90",
            verdict: "pass",
            notes: "Good",
          },
          latest_review_decision: null,
          citations: [
            {
              id: 1,
              excerpt_id: 12,
              relevance_rank: 1,
              rationale: "Most direct evidence",
              excerpt_text: "Excerpt evidence text",
              document_title: "Q2 Market Themes Report",
            },
          ],
        },
      ],
    });

    render(
      <QueryClientProvider client={new QueryClient()}>
        <MemoryRouter initialEntries={["/answers/5"]}>
          <Routes>
            <Route path="/answers/:answerId" element={<AnswerDetailPage />} />
          </Routes>
        </MemoryRouter>
      </QueryClientProvider>,
    );

    expect(await screen.findByText("Citations")).toBeInTheDocument();
    expect(await screen.findByText("Q2 Market Themes Report")).toBeInTheDocument();
  });
});
