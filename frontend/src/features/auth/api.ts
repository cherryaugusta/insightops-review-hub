import { api } from "../../lib/api";
import type { AuthUser } from "../../lib/types";

export interface RegisterPayload {
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  password: string;
}

export async function login(username: string, password: string) {
  const response = await api.post("/token/", { username, password });
  return response.data as { access: string; refresh: string };
}

export async function registerUser(payload: RegisterPayload) {
  const response = await api.post("/auth/register/", payload);
  return response.data;
}

export async function fetchMe() {
  const response = await api.get<AuthUser>("/auth/me/");
  return response.data;
}
