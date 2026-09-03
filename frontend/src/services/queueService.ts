import type { QueueItem } from "../types";
import { apiRequest } from "./api";

export async function getQueueItems(projectId?: string): Promise<QueueItem[]> {
  return apiRequest<QueueItem[]>(projectId ? `/projects/${projectId}/testing-queue` : "/testing-queue");
}