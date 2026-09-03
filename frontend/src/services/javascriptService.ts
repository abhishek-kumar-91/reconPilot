import type { JavaScriptFile } from "../types";
import { apiRequest } from "./api";

export async function getJavaScriptFiles(
  projectId?: string,
): Promise<JavaScriptFile[]> {
  return apiRequest<JavaScriptFile[]>(projectId ? `/projects/${projectId}/javascript` : "/javascript");
}