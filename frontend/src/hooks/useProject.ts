import { useParams } from "react-router-dom";
import { getProject } from "../services/projectService";
import { useAsync } from "./useAsync";

export function useProject() {
  const { projectId } = useParams();
  const result = useAsync(
    () => (projectId ? getProject(projectId) : Promise.resolve(undefined)),
    [projectId],
  );

  return { projectId, ...result };
}