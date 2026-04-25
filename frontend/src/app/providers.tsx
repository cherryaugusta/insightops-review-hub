import type { PropsWithChildren } from "react";
import { QueryClientProvider } from "@tanstack/react-query";
import { RouterProvider } from "react-router-dom";
import { queryClient } from "./queryClient";
import { router } from "./router";

export function AppProviders({ children }: PropsWithChildren) {
  return (
    <QueryClientProvider client={queryClient}>
      {children}
      <RouterProvider router={router} />
    </QueryClientProvider>
  );
}
