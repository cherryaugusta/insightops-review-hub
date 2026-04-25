import { create } from "zustand";
import type { AuthUser } from "../../lib/types";
import { clearTokens, getAccessToken, getRefreshToken, setTokens } from "../../lib/auth";

interface AuthState {
  user: AuthUser | null;
  isAuthenticated: boolean;
  setUser: (user: AuthUser | null) => void;
  setAuthTokens: (access: string, refresh: string) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  isAuthenticated: Boolean(getAccessToken() && getRefreshToken()),
  setUser: (user) => set({ user }),
  setAuthTokens: (access, refresh) => {
    setTokens(access, refresh);
    set({ isAuthenticated: true });
  },
  logout: () => {
    clearTokens();
    set({ user: null, isAuthenticated: false });
  },
}));
