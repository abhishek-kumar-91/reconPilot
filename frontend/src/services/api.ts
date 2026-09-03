const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000/api/v1";

export async function apiRequest<T>(
  path: string,
  options: RequestInit = {},
): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(options.headers ?? {}),
    },
  });

  if (!response.ok) {
    throw new Error(`API request failed: ${response.status}`);
  }

  return response.json() as Promise<T>;
}

// Backend integration examples:
// export const projectApi = {
//   list: () => apiRequest<Project[]>("/projects"),
//   get: (id: string) => apiRequest<Project>(`/projects/${id}`),
//   create: (body: CreateProjectRequest) =>
//     apiRequest<Project>("/projects", { method: "POST", body: JSON.stringify(body) }),
// };
//
// export const scanApi = {
//   create: (body: CreateScanRequest) =>
//     apiRequest<Scan>("/scans", { method: "POST", body: JSON.stringify(body) }),
//   get: (id: string) => apiRequest<Scan>(`/scans/${id}`),
// };