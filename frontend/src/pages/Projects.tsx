import { Plus } from "lucide-react";
import { useEffect, useState } from "react";
import { PageHeader } from "../components/ui/PageHeader";
import { ProjectCard } from "../components/projects/ProjectCard";
import { Modal } from "../components/ui/Modal";
import { NewScanForm } from "../components/forms/NewScanForm";
import { createProject, deleteProject, getProjects } from "../services/projectService";
import type { Project } from "../types";

export function Projects() {
  const [modalOpen, setModalOpen] = useState(false);
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    void loadProjects();
  }, []);

  async function loadProjects() {
    try {
      const data = await getProjects();
      setProjects(data);
    } finally {
      setLoading(false);
    }
  }

  async function handleSubmit(target: string) {
    const normalizedTarget = target.trim();
    const rootDomain = normalizedTarget
      .replace(/^https?:\/\//i, "")
      .replace(/\/$/, "")
      .split("/")[0];

    await createProject({
      name: normalizedTarget || rootDomain || "New project",
      rootDomain,
      description: "Created from recon workflow",
    });
    setModalOpen(false);
    await loadProjects();
  }

  async function handleDelete(project: Project) {
    if (!window.confirm(`Delete project "${project.name}"? This cannot be undone.`)) {
      return;
    }

    await deleteProject(project.id);
    setProjects((currentProjects) => currentProjects.filter(({ id }) => id !== project.id));
  }

  return (
    <>
      <PageHeader
        title="Projects"
        description="Manage authorized reconnaissance workspaces."
        actions={
          <button className="button primary" onClick={() => setModalOpen(true)}>
            <Plus size={16} /> New project
          </button>
        }
      />

      {loading ? <div className="empty-state"><p>Loading projects…</p></div> : (
        <div className="projects-grid">
          {projects.map((project) => <ProjectCard key={project.id} project={project} onDelete={handleDelete} />)}
        </div>
      )}

      <Modal open={modalOpen} title="Create project" onClose={() => setModalOpen(false)}>
        <NewScanForm onSubmit={(target) => {
          void handleSubmit(target);
        }} />
      </Modal>
    </>
  );
}