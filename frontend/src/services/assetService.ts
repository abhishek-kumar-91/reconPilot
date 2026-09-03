import type { Asset } from "../types";
import { apiRequest } from "./api";

export async function getAssets(projectId?: string): Promise<Asset[]> {
  return apiRequest<Asset[]>(projectId ? `/projects/${projectId}/assets` : "/assets");
}