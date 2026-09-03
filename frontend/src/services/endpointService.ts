import type { Endpoint } from "../types";
import { apiRequest } from "./api";

export async function getEndpoints(projectId?: string): Promise<Endpoint[]> {
  return apiRequest<Endpoint[]>(projectId ? `/projects/${projectId}/endpoints` : "/endpoints");
}