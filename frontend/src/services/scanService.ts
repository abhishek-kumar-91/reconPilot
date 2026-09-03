import type { Scan } from "../types";
import { apiRequest } from "./api";

export async function getScans(projectId?: string): Promise<Scan[]> {
  return apiRequest<Scan[]>(projectId ? `/projects/${projectId}/scans` : "/scans");
}

export async function getScan(id: string): Promise<Scan | undefined> {
  return apiRequest<Scan>(`/scans/${id}`);
}

export async function createScan(projectId: string): Promise<Scan> {
  return apiRequest<Scan>(`/projects/${projectId}/scans`, { method: "POST" });
}