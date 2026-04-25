import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { LoginPage } from "./LoginPage";

describe("LoginPage", () => {
  it("renders fields and submit button", () => {
    render(
      <QueryClientProvider client={new QueryClient()}>
        <MemoryRouter>
          <LoginPage />
        </MemoryRouter>
      </QueryClientProvider>,
    );

    expect(screen.getByText("InsightOps Review Hub")).toBeInTheDocument();
    expect(screen.getByPlaceholderText("demoanalyst")).toBeInTheDocument();
    expect(screen.getByPlaceholderText("StrongPassword123!")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /sign in/i })).toBeInTheDocument();
  });
});
