export const API_BASE =
  window.location.origin && window.location.origin !== "null"
    ? window.location.origin
    : "http://127.0.0.1:8765";

export class ApiError extends Error {
  status: number;
  payload: unknown;

  constructor(message: string, status: number, payload: unknown) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.payload = payload;
  }
}

export function apiUrl(path: string): URL {
  return new URL(path, API_BASE);
}

export async function readJson<T>(response: Response): Promise<T> {
  return (await response.json().catch(() => ({}))) as T;
}

export async function apiJson<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(apiUrl(path), {
    cache: "no-store",
    ...init
  });

  if (handleAuthFailure(response)) {
    throw new ApiError("auth redirect", response.status, {});
  }

  const payload = await readJson<Record<string, unknown>>(response);
  if (!response.ok) {
    const message =
      typeof payload.message === "string"
        ? payload.message
        : typeof payload.error === "string"
          ? payload.error
          : `HTTP ${response.status}`;
    throw new ApiError(message, response.status, payload);
  }

  return payload as T;
}

export function handleAuthFailure(response: Response): boolean {
  if (response.status === 401) {
    window.location.href = `/login.html?next=${encodeURIComponent(window.location.pathname + window.location.search)}`;
    return true;
  }

  if (response.status === 403) {
    response
      .clone()
      .json()
      .then((data: { error?: string }) => {
        window.location.href = data.error === "expired" ? "/expired.html" : "/login.html";
      })
      .catch(() => {
        window.location.href = "/login.html";
      });
    return true;
  }

  return false;
}
