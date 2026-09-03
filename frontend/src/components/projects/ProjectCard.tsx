import { ArrowUpRight, Globe2, Network, Trash2 } from "lucide-react";
import { Link } from "react-router-dom";
import type { Project } from "../../types";
import { StatusBadge } from "../ui/StatusBadge";

export function ProjectCard({ project, onDelete }: { project: Project; onDelete: (project: Project) => void }) {
  return (
    <Link className="project-card" to={`/projects/${project.id}`}>
      <div className="project-card-top">
        <div className="project-logo"><Globe2 size={20} /></div>
        <div className="project-card-actions">
          <button
            className="icon-button danger-icon"
            type="button"
            title={`Delete ${project.name}`}
            aria-label={`Delete ${project.name}`}
            onClick={(event) => {
              event.preventDefault();
              event.stopPropagation();
              onDelete(project);
            }}
          >
            <Trash2 size={15} />
          </button>
          <ArrowUpRight size={17} className="muted-icon" />
        </div>
      </div>
      <div className="project-card-title">{project.name}</div>
      <div className="project-domain">{project.rootDomain}</div>
      <div className="project-card-description">{project.description}</div>
      <div className="project-card-footer">
        <StatusBadge status={project.status} variant="success" />
        <span><Network size={14} /> {project.endpointCount} endpoints</span>
      </div>
    </Link>
  );
}