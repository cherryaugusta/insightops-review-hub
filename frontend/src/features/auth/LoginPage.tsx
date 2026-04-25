import type { FormEvent } from "react";
import { useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { useMutation } from "@tanstack/react-query";
import { fetchMe, login } from "./api";
import { useAuthStore } from "./store";

export function LoginPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const { setAuthTokens, setUser } = useAuthStore();

  const [username, setUsername] = useState("demoanalyst");
  const [password, setPassword] = useState("StrongPassword123!");
  const [errorMessage, setErrorMessage] = useState("");

  const mutation = useMutation({
    mutationFn: async () => {
      const tokens = await login(username, password);
      setAuthTokens(tokens.access, tokens.refresh);
      const user = await fetchMe();
      setUser(user);
      return user;
    },
    onSuccess: () => {
      const destination = (location.state as { from?: string } | null)?.from || "/dashboard";
      navigate(destination);
    },
    onError: () => {
      setErrorMessage("Login failed. Check the username and password.");
    },
  });

  function handleSubmit(event: FormEvent) {
    event.preventDefault();
    setErrorMessage("");
    mutation.mutate();
  }

  return (
    <div className="auth-page">
      <div className="auth-panel">
        <div className="eyebrow">Internal knowledge operations</div>
        <h1>InsightOps Review Hub</h1>
        <p>
          Sign in to manage workspaces, source material, reviewable answers,
          evaluations, and audit visibility.
        </p>

        <form className="form-grid" onSubmit={handleSubmit}>
          <label>
            Username
            <input
              value={username}
              onChange={(event) => setUsername(event.target.value)}
              placeholder="demoanalyst"
            />
          </label>

          <label>
            Password
            <input
              type="password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              placeholder="StrongPassword123!"
            />
          </label>

          {errorMessage ? <div className="form-error">{errorMessage}</div> : null}

          <button className="button" type="submit" disabled={mutation.isPending}>
            {mutation.isPending ? "Signing in..." : "Sign in"}
          </button>
        </form>

        <div className="auth-links">
          <span>Need an account?</span> <Link to="/register">Register</Link>
        </div>
      </div>
    </div>
  );
}
