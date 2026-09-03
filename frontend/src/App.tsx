import { Routes, Route, Navigate } from "react-router-dom";
import { AppShell } from "./components/layout/AppShell";
import { Dashboard } from "./pages/Dashboard";
import { Projects } from "./pages/Projects";
import { ProjectOverview } from "./pages/ProjectOverview";
import { ScanDetail } from "./pages/ScanDetail";
import { Assets } from "./pages/Assets";
import { Endpoints } from "./pages/Endpoints";
import { JavaScriptFiles } from "./pages/JavaScriptFiles";
import { APIs } from "./pages/APIs";
import { Technologies } from "./pages/Technologies";
import { TestingQueue } from "./pages/TestingQueue";
import { Settings } from "./pages/Settings";
import { NotFound } from "./pages/NotFound";

export default function App() {
  return (
    <AppShell>
      <Routes>
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/projects" element={<Projects />} />
        <Route path="/projects/:projectId" element={<ProjectOverview />} />
        <Route path="/scans/:scanId" element={<ScanDetail />} />
        <Route path="/assets" element={<Assets />} />
        <Route path="/endpoints" element={<Endpoints />} />
        <Route path="/javascript" element={<JavaScriptFiles />} />
        <Route path="/apis" element={<APIs />} />
        <Route path="/technologies" element={<Technologies />} />
        <Route path="/testing-queue" element={<TestingQueue />} />
        <Route path="/settings" element={<Settings />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </AppShell>
  );
}