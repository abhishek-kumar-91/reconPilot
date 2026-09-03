import type { ApiSpec } from "../types";
import { apiRequest } from "./api";

export async function getApiSpecs(projectId?: string): Promise<ApiSpec[]> {
  return apiRequest<ApiSpec[]>(projectId ? `/projects/${projectId}/apis` : "/apis");
}