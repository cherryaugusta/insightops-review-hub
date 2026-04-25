import { render, screen } from "@testing-library/react";
import { MemoryRouter, Routes, Route } from "react-router-dom";
import { ProtectedRoute } from "./ProtectedRoute";

describe("ProtectedRoute", () => {
  it("redirects without token", () => {
    localStorage.removeItem("access_token");

    render(
      <MemoryRouter initialEntries={["/dashboard"]}>
        <Routes>
          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <div>Protected</div>
              </ProtectedRoute>
            }
          />
          <Route path="/login" element={<div>Login screen</div>} />
        </Routes>
      </MemoryRouter>,
    );

    expect(screen.getByText("Login screen")).toBeInTheDocument();
  });
});
