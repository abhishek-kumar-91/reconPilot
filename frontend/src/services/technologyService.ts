import type { Technology } from "../types";
import { apiRequest } from "./api";

export async function getTechnologies(projectId?: string): Promise<Technology[]> {
  return apiRequest<Technology[]>(projectId ? `/projects/${projectId}/technologies` : "/technologies");
}