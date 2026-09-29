/**
 * RUNIX API Client.
 *
 * Implements typed requests to the RUNIX Control Plane (/api/v1).
 * Handles authentication tokens, standard error envelopes, and request IDs.
 */

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export interface ApiError {
  code: string;
  message: string;
  details?: Array<{ field: string; message: string }>;
}

export interface ApiResponse<T> {
  data: T | null;
  error: ApiError | null;
  request_id: string;
}

export class RunixApiError extends Error {
  code: string;
  status: number;
  details?: Array<{ field: string; message: string }>;

  constructor(status: number, error: ApiError) {
    super(error.message);
    this.name = "RunixApiError";
    this.code = error.code;
    this.status = status;
    this.details = error.details;
  }
}

function getStoredToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem("runix_token");
}

export function setStoredToken(token: string | null): void {
  if (typeof window === "undefined") return;
  if (token) {
    localStorage.setItem("runix_token", token);
  } else {
    localStorage.removeItem("runix_token");
  }
}

async function request<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const token = getStoredToken();
  const headers = new Headers(options.headers);

  headers.set("Content-Type", "application/json");
  if (token) {
    headers.set("Authorization", `Bearer ${token}`);
  }

  const response = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers,
  });

  if (response.status === 204) {
    return {} as T;
  }

  const json: ApiResponse<T> = await response.json();

  if (!response.ok || json.error) {
    const error = json.error || {
      code: "UNKNOWN_ERROR",
      message: `HTTP error ${response.status}`,
    };
    throw new RunixApiError(response.status, error);
  }

  return json.data as T;
}

export const api = {
  // Auth
  register: (body: { email: string; password: string; display_name: string }) =>
    request<{ user: any }>("/auth/register", {
      method: "POST",
      body: JSON.stringify(body),
    }),

  login: (body: { email: string; password: string }) =>
    request<{ access_token: string; user: any }>("/auth/login", {
      method: "POST",
      body: JSON.stringify(body),
    }),

  logout: () =>
    request<void>("/auth/logout", {
      method: "POST",
    }),

  getMe: () =>
    request<any>("/auth/me", {
      method: "GET",
    }),

  // Projects
  listProjects: (params?: { page?: number; page_size?: number; search?: string }) => {
    const query = new URLSearchParams();
    if (params?.page) query.set("page", params.page.toString());
    if (params?.page_size) query.set("page_size", params.page_size.toString());
    if (params?.search) query.set("search", params.search);
    const qs = query.toString() ? `?${query.toString()}` : "";
    return request<{ items: any[]; page: number; page_size: number; total: number }>(
      `/projects${qs}`,
      { method: "GET" }
    );
  },

  createProject: (body: {
    name: string;
    description?: string;
    template: string;
    visibility?: "private" | "public";
  }) =>
    request<any>("/projects", {
      method: "POST",
      body: JSON.stringify(body),
    }),

  getProject: (projectId: string) =>
    request<any>(`/projects/${projectId}`, {
      method: "GET",
    }),

  deleteProject: (projectId: string) =>
    request<void>(`/projects/${projectId}`, {
      method: "DELETE",
    }),

  // Templates
  listTemplates: () =>
    request<{ items: any[] }>("/templates", {
      method: "GET",
    }),

  // Files
  listFiles: (projectId: string) =>
    request<{ items: any[] }>(`/projects/${projectId}/files`, {
      method: "GET",
    }),

  readFile: (projectId: string, path: string) =>
    request<{ path: string; content: string; encoding: string; size_bytes: number }>(
      `/projects/${projectId}/files/content?path=${encodeURIComponent(path)}`,
      { method: "GET" }
    ),

  writeFile: (projectId: string, path: string, content: string) =>
    request<{ path: string; saved: boolean; size_bytes: number }>(
      `/projects/${projectId}/files/content`,
      {
        method: "PUT",
        body: JSON.stringify({ path, content }),
      }
    ),

  // Commands & Terminal
  executeCommand: (projectId: string, command: string, timeout_seconds = 30) =>
    request<{
      id: string;
      project_id: string;
      command: string;
      status: string;
      exit_code: number;
      stdout: string;
      stderr: string;
      started_at: string;
      finished_at: string;
    }>(`/projects/${projectId}/commands`, {
      method: "POST",
      body: JSON.stringify({ command, timeout_seconds }),
    }),
};
