export type ScanStatus = "queued" | "running" | "completed" | "failed";
export type Priority = "critical" | "high" | "medium" | "low" | "info";
export type EndpointCategory =
  | "authentication"
  | "authorization"
  | "business-logic"
  | "file-upload"
  | "admin"
  | "api"
  | "graphql"
  | "webhook"
  | "general";

export interface Project {
  id: string;
  name: string;
  rootDomain: string;
  description?: string;
  status: "active" | "paused";
  assetCount: number;
  endpointCount: number;
  lastScanAt?: string;
  createdAt: string;
}

export interface Scan {
  id: string;
  projectId: string;
  target: string;
  status: ScanStatus;
  startedAt: string;
  completedAt?: string;
  assetsFound: number;
  liveHosts: number;
  urlsFound: number;
  jsFiles: number;
  apiEndpoints: number;
  technologies: number;
  progress: number;
}

export interface Asset {
  id: string;
  projectId: string;
  hostname: string;
  url: string;
  type: "domain" | "subdomain" | "ip";
  statusCode?: number;
  alive: boolean;
  title?: string;
  technologies: string[];
  ips: string[];
  ports: number[];
  source: string[];
  discoveredAt: string;
}

export interface Endpoint {
  id: string;
  projectId: string;
  host: string;
  method: "GET" | "POST" | "PUT" | "PATCH" | "DELETE" | "OPTIONS";
  path: string;
  url: string;
  category: EndpointCategory;
  priority: Priority;
  authRequired: boolean;
  parameterCount: number;
  parameters: string[];
  statusCode?: number;
  contentType?: string;
  sources: string[];
  notes?: string;
  lastSeenAt: string;
}

export interface JavaScriptFile {
  id: string;
  projectId: string;
  host: string;
  url: string;
  filename: string;
  size: number;
  endpointsFound: number;
  secretsFound: number;
  source: string;
  statusCode: number;
  lastSeenAt: string;
}

export interface ApiSpec {
  id: string;
  projectId: string;
  host: string;
  type: "OpenAPI" | "Swagger" | "GraphQL" | "REST";
  url: string;
  version?: string;
  endpointCount: number;
  discoveredAt: string;
  statusCode: number;
}

export interface Technology {
  id: string;
  projectId: string;
  name: string;
  category: "frontend" | "backend" | "server" | "cdn" | "analytics" | "database" | "other";
  version?: string;
  assets: number;
  confidence: number;
  sources: string[];
}

export interface QueueItem {
  id: string;
  endpointId: string;
  endpoint: Endpoint;
  reason: string;
  priority: Priority;
  aiScore: number;
  status: "new" | "testing" | "done" | "dismissed";
  createdAt: string;
}

export interface DashboardStats {
  projects: number;
  assets: number;
  liveHosts: number;
  endpoints: number;
  jsFiles: number;
  apiSpecs: number;
  technologies: number;
  queueItems: number;
}