import { render, screen } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { EvaluationDetailPage } from "./EvaluationDetailPage";
import * as api from "./api";

vi.mock("./api");

describe("EvaluationDetailPage", () => {
  it("renders scores and verdict", async () => {
    vi.mocked(api.fetchEvaluation).mockResolvedValue({
      id: 1,
      answer_id: 10,
      evaluator_type: "heuristic",
      groundedness_score: "0.90",
      citation_coverage_score: "0.95",
      completeness_score: "0.85",
      overall_score: "0.90",
      verdict: "pass",
      notes: "Looks grounded",
      created_at: "",
    });

    render(
      <QueryClientProvider client={new QueryClient()}>
        <MemoryRouter initialEntries={["/evaluations/1"]}>
          <Routes>
            <Route path="/evaluations/:evaluationId" element={<EvaluationDetailPage />} />
          </Routes>
        </MemoryRouter>
      </QueryClientProvider>,
    );

    expect(await screen.findByText("Groundedness")).toBeInTheDocument();
    expect(await screen.findAllByText("pass")).toHaveLength(2);
  });
});
