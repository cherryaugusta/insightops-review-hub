import { defineConfig } from "@playwright/test";

export default defineConfig({
  testDir: "./tests",
  timeout: 60000,
  expect: {
    timeout: 10000,
  },
  use: {
    baseURL: "http://127.0.0.1:5173",
    headless: true,
  },
  webServer: [
    {
      command: "..\\.venv\\Scripts\\python.exe ..\\backend\\manage.py runserver 127.0.0.1:8000",
      port: 8000,
      reuseExistingServer: true,
      timeout: 120000,
    },
    {
      command: "npm run dev -- --host 127.0.0.1 --port 5173",
      port: 5173,
      reuseExistingServer: true,
      timeout: 120000,
    },
  ],
});
