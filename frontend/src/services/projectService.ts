import type { Project } from "../types";
import { apiRequest } from "./api";

export async function getProjects(): Promise<Project[]> {
  return apiRequest<Project[]>("/projects");
}

export async function getProject(id: string): Promise<Project | undefined> {
  return apiRequest<Project>(`/projects/${id}`);
}

export async function createProject(payload: {
  name: string;
  rootDomain: string;
  description?: string;
}): Promise<Project> {
  return apiRequest<Project>("/projects", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function deleteProject(id: string): Promise<Project> {
  return apiRequest<Project>(`/projects/${id}`, {
    method: "DELETE",
  });
}