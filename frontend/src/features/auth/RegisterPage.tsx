import type { FormEvent } from "react";
import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useMutation } from "@tanstack/react-query";
import { registerUser } from "./api";

export function RegisterPage() {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    username: "",
    email: "",
    first_name: "",
    last_name: "",
    password: "",
  });
  const [errorMessage, setErrorMessage] = useState("");

  const mutation = useMutation({
    mutationFn: () => registerUser(form),
    onSuccess: () => navigate("/login"),
    onError: () => setErrorMessage("Registration failed. Review the form and try again."),
  });

  function handleSubmit(event: FormEvent) {
    event.preventDefault();
    setErrorMessage("");
    mutation.mutate();
  }

  return (
    <div className="auth-page">
      <div className="auth-panel">
        <div className="eyebrow">Account setup</div>
        <h1>Create an account</h1>

        <form className="form-grid" onSubmit={handleSubmit}>
          <label>
            Username
            <input
              value={form.username}
              onChange={(e) => setForm({ ...form, username: e.target.value })}
            />
          </label>

          <label>
            Email
            <input
              value={form.email}
              onChange={(e) => setForm({ ...form, email: e.target.value })}
            />
          </label>

          <label>
            First name
            <input
              value={form.first_name}
              onChange={(e) => setForm({ ...form, first_name: e.target.value })}
            />
          </label>

          <label>
            Last name
            <input
              value={form.last_name}
              onChange={(e) => setForm({ ...form, last_name: e.target.value })}
            />
          </label>

          <label>
            Password
            <input
              type="password"
              value={form.password}
              onChange={(e) => setForm({ ...form, password: e.target.value })}
            />
          </label>

          {errorMessage ? <div className="form-error">{errorMessage}</div> : null}

          <button className="button" type="submit" disabled={mutation.isPending}>
            {mutation.isPending ? "Creating account..." : "Create account"}
          </button>
        </form>

        <div className="auth-links">
          <span>Already registered?</span> <Link to="/login">Back to login</Link>
        </div>
      </div>
    </div>
  );
}
