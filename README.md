# 🛰️ ReconPilot

```text
██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗██████╗ ██╗██╗      ██████╗ ████████╗
██╔══██╗██╔════╝██╔═══██╗██╔══██╗████╗  ██║██╔══██╗██║██║     ██╔═══██╗╚══██╔══╝
██████╔╝█████╗  ██║   ██║██████╔╝██╔██╗ ██║██████╔╝██║██║     ██║   ██║   ██║
██╔══██╗██╔══╝  ██║   ██║██╔══██╗██║╚██╗██║██╔═══╝ ██║██║     ██║   ██║   ██║
██║  ██║███████╗╚██████╔╝██║  ██║██║ ╚████║██║     ██║███████╗╚██████╔╝   ██║
╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝     ╚═╝╚══════╝ ╚═════╝    ╚═╝
```

> **AI-assisted reconnaissance and attack-surface intelligence for authorized security testing.**

[![Status](https://img.shields.io/badge/status-active%20development-orange)](#roadmap)
[![License](https://img.shields.io/badge/license-MIT-blue)](#license)
[![Python](https://img.shields.io/badge/Python-3.x-blue)](https://www.python.org/)
[![React](https://img.shields.io/badge/React-TypeScript-61DAFB)](https://react.dev/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Python-009688)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-4169E1)](https://www.postgresql.org/)
[![Ollama](https://img.shields.io/badge/AI-Ollama-black)](https://ollama.com/)

---

## 👨‍💻 Built By

**Abhishek Kumar**

Security Researcher | Bug Bounty Hunter | Offensive Security

ReconPilot is a personal security research project created to reduce repetitive reconnaissance work and provide a cleaner attack-surface map for manual security testing.

> Built with curiosity, security research, and a lot of terminal windows. 🚀

---

# 🎯 What is ReconPilot?

ReconPilot is a local-first reconnaissance orchestration platform designed to accelerate the reconnaissance phase of authorized web application and bug-bounty testing.

Instead of manually running multiple reconnaissance tools and then combining thousands of results, ReconPilot aims to provide a single workflow:

```text
Target
  ↓
Scope Validation
  ↓
Subdomain Discovery
  ↓
Live Host Detection
  ↓
Technology Detection
  ↓
Web Crawling
  ↓
JavaScript Discovery
  ↓
API / Endpoint Discovery
  ↓
Parameter Extraction
  ↓
Deduplication & Normalization
  ↓
AI Classification
  ↓
Attack Surface Map
  ↓
Manual Testing Queue
```

### The goal

ReconPilot is **not designed to replace the security researcher**.

Its goal is:

> **Spend less time collecting reconnaissance data and more time testing authentication, authorization, business logic, and application functionality.**

---

# ⚡ Why ReconPilot?

A typical bug-bounty reconnaissance workflow may involve:

```text
subfinder
httpx
katana
dnsx
naabu
JavaScript analysis
OpenAPI/Swagger discovery
URL collection
manual filtering
deduplication
endpoint classification
```

The problem isn't that these tools are bad.

The problem is that the researcher has to repeatedly:

```text
Run tools
   ↓
Collect output
   ↓
Clean output
   ↓
Remove duplicates
   ↓
Combine sources
   ↓
Understand endpoints
   ↓
Prioritize interesting targets
```

ReconPilot aims to automate this **data collection and organization layer**.

---

# 🧠 Core Philosophy

ReconPilot follows a simple principle:

```text
Automation discovers.
AI understands.
Researcher decides.
```

The system should help answer:

> "What should I manually test?"

rather than:

> "How can an AI autonomously attack the target?"

---

# 🏗️ Architecture

```text
                         ┌─────────────────────┐
                         │      React UI       │
                         │   TypeScript/Vite   │
                         └──────────┬──────────┘
                                    │
                                    │ HTTP/REST
                                    ▼
                         ┌─────────────────────┐
                         │       FastAPI       │
                         │      Backend        │
                         └──────────┬──────────┘
                                    │
                           Recon Orchestrator
                                    │
              ┌─────────────────────┼─────────────────────┐
              │                     │                     │
              ▼                     ▼                     ▼
        ┌───────────┐         ┌───────────┐        ┌───────────┐
        │ Subfinder │         │   HTTPX   │        │  Katana   │
        │           │         │           │        │           │
        │ Subdomain │         │Live Hosts │        │  Crawler  │
        └─────┬─────┘         └─────┬─────┘        └─────┬─────┘
              │                     │                     │
              └─────────────────────┼─────────────────────┘
                                    ▼
                           ┌──────────────────┐
                           │  Data Processing │
                           │ Normalize/Unique │
                           └────────┬─────────┘
                                    ▼
                           ┌──────────────────┐
                           │   PostgreSQL     │
                           │     Database     │
                           └────────┬─────────┘
                                    │
                                    ▼
                           ┌──────────────────┐
                           │      Ollama      │
                           │    Local LLM     │
                           └────────┬─────────┘
                                    ▼
                           ┌──────────────────┐
                           │ AI Classification│
                           │ & Prioritization │
                           └────────┬─────────┘
                                    ▼
                         ┌─────────────────────┐
                         │ Manual Testing Queue│
                         └─────────────────────┘
```

---

# 🛠️ Technology Stack

| Component               | Technology                 |
| ----------------------- | -------------------------- |
| Frontend                | React + TypeScript         |
| Frontend tooling        | Vite                       |
| Backend                 | Python + FastAPI           |
| Database                | PostgreSQL                 |
| ORM                     | SQLAlchemy                 |
| Migrations              | Alembic                    |
| AI Runtime              | Ollama                     |
| Subdomain discovery     | ProjectDiscovery Subfinder |
| HTTP probing            | ProjectDiscovery HTTPX     |
| Web crawling            | ProjectDiscovery Katana    |
| Port discovery          | ProjectDiscovery Naabu     |
| Vulnerability templates | ProjectDiscovery Nuclei    |
| Version control         | Git                        |
| OS                      | Windows / Linux            |

---

# ✨ Planned Features

## 🔎 Asset Discovery

* Subdomain enumeration
* DNS resolution
* IP discovery
* Live host detection
* HTTP/HTTPS probing
* Port discovery

## 🌐 Web Discovery

* URL crawling
* JavaScript file discovery
* JavaScript endpoint extraction
* API endpoint discovery
* Parameter discovery
* Redirect detection
* Content-type identification

## 🔌 API Intelligence

* REST endpoint discovery
* OpenAPI/Swagger detection
* GraphQL detection
* API version detection
* HTTP method identification
* Parameter normalization

## 🧹 Data Intelligence

* URL normalization
* Endpoint deduplication
* Source correlation
* Technology correlation
* Historical scan comparison

## 🤖 AI Intelligence

Local AI will be used for:

* Endpoint classification
* Technology interpretation
* Attack-surface summarization
* Interesting endpoint identification
* Manual-testing prioritization
* Business-function classification

## 🎯 Manual Testing Queue

ReconPilot will prioritize endpoints that may deserve manual investigation, such as:

```text
Authentication
Authorization
User management
Object references
Password reset
File uploads
Payments
Transactions
Admin functionality
API endpoints
GraphQL
Webhooks
Sensitive data
Business operations
```

The final decision remains with the researcher.

---

# 📁 Project Structure

```text
reconpilot/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── engines/
│   │   └── db/
│   │
│   ├── main.py
│   ├── pyproject.toml
│   └── uv.lock
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── hooks/
│   │   └── types/
│   │
│   ├── package.json
│   └── vite.config.ts
│
├── data/
│   ├── raw/
│   └── processed/
│
├── docs/
│
├── scripts/
│
├── .env.example
├── .gitignore
├── README.md
└── LICENSE
```

---

# 💻 Installation

## 1. Prerequisites

Install the following:

* Git
* Python 3.x
* Node.js LTS
* PostgreSQL
* Go
* Ollama

You also need:

* PowerShell on Windows
* Internet access
* Sufficient disk space for local AI models

---

# 2. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/reconpilot.git
cd reconpilot
```

Replace `YOUR_USERNAME` with your GitHub username.

---

# 3. Install ProjectDiscovery Tools

ReconPilot uses ProjectDiscovery tools as reconnaissance engines.

Install:

### Subfinder

```bash
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
```

### HTTPX

```bash
go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
```

### Katana

```bash
go install -v github.com/projectdiscovery/katana/cmd/katana@latest
```

### Naabu

```bash
go install -v github.com/projectdiscovery/naabu/v2/cmd/naabu@latest
```

### Nuclei

```bash
go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
```

Verify:

```bash
subfinder -h
httpx -h
katana -h
naabu -h
nuclei -h
```

> Some reconnaissance providers used by passive enumeration tools may require their own API keys. The tools themselves are open source, but third-party data providers can have separate limits or requirements.

---

# 4. Install Ollama

Install Ollama for your operating system.

Verify:

```bash
ollama --version
```

Then download a local model supported by your machine:

```bash
ollama pull <MODEL_NAME>
```

Test:

```bash
ollama run <MODEL_NAME>
```

ReconPilot is designed to use Ollama locally so AI analysis does not require a paid cloud API.

---

# 5. Create PostgreSQL Database

Open PostgreSQL / pgAdmin and create:

```text
Database:
reconpilot
```

Default development configuration:

```text
Host: localhost
Port: 5432
Database: reconpilot
User: postgres
Password: YOUR_PASSWORD
```

---

# 6. Configure Environment Variables

Create:

```text
.env
```

from:

```text
.env.example
```

Example:

```env
DATABASE_URL=postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5432/reconpilot

OLLAMA_BASE_URL=http://localhost:11434

OLLAMA_MODEL=<MODEL_NAME>

ENVIRONMENT=development
```

### ⚠️ Never commit `.env`

Make sure `.gitignore` contains:

```gitignore
.env
.env.*
!.env.example

__pycache__/
*.pyc

node_modules/
dist/

.venv/
.vscode/

data/raw/
data/processed/
```

---

# 7. Backend Setup

Open PowerShell:

```bash
cd backend
```

Create the Python environment:

```bash
uv sync
```

If the project does not yet contain a lockfile:

```bash
uv init
```

Then install dependencies:

```bash
uv add "fastapi[standard]"
uv add sqlalchemy
uv add psycopg
uv add alembic
uv add pydantic-settings
```

Run the backend:

```bash
uv run fastapi dev app/main.py
```

Backend:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

---

# 8. Frontend Setup

Open another terminal:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start development server:

```bash
npm run dev
```

Frontend:

```text
http://localhost:5173
```

---

# 🚀 Running ReconPilot

Start PostgreSQL.

Start Ollama.

Then start the backend:

```bash
cd backend
uv run fastapi dev app/main.py
```

Start the frontend in another terminal:

```bash
cd frontend
npm run dev
```

Open:

```text
http://localhost:5173
```

---

# 🔄 Recon Workflow

The intended workflow is:

```text
1. Create Project
        ↓
2. Define Target
        ↓
3. Define Scope
        ↓
4. Start Recon
        ↓
5. Asset Discovery
        ↓
6. Live Host Detection
        ↓
7. Technology Detection
        ↓
8. Crawling
        ↓
9. JavaScript Analysis
        ↓
10. API Discovery
        ↓
11. Endpoint Normalization
        ↓
12. Deduplication
        ↓
13. AI Classification
        ↓
14. Prioritization
        ↓
15. Manual Testing
```

---

# 📊 Example Output

Given:

```text
https://example.com
```

ReconPilot may eventually produce:

```text
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
              RECON SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Target
example.com

Assets
243

Live Hosts
87

Technologies
19

JavaScript Files
136

URLs
2,431

API Endpoints
421

Parameters
847
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Manual Testing Queue

```text
🔴 HIGH PRIORITY

GET /api/users/{id}
→ Authorization

POST /api/password/reset
→ Authentication

POST /api/transfer
→ Business Logic

POST /api/upload
→ File Upload

GET /admin/users
→ Access Control
```

---

# 🧠 AI Prioritization Example

Input:

```json
{
  "method": "GET",
  "path": "/api/orders/{id}",
  "authentication": "required",
  "source": [
    "crawler",
    "javascript",
    "openapi"
  ]
}
```

Possible AI output:

```json
{
  "category": "authorization",
  "priority": "high",
  "reason": "Object-level endpoint with an identifier.",
  "manual_review": [
    "Check object ownership",
    "Check cross-account access",
    "Check role boundaries"
  ]
}
```

The AI provides **analysis and prioritization**, not autonomous exploitation.

---

# 🛡️ Scope & Safety

ReconPilot is intended **only for authorized security testing**.

Examples include:

* Bug bounty programs
* Your own applications
* Local labs
* CTF environments
* Applications where you have explicit authorization
* Authorized penetration tests

Always respect:

```text
✓ Program scope
✓ Out-of-scope assets
✓ Rate limits
✓ Authentication requirements
✓ Terms and conditions
✓ Responsible disclosure rules
```

ReconPilot should enforce scope **before** reconnaissance jobs are executed.

---

# 🚧 Roadmap

## Phase 1 — Foundation

* [x] Project structure
* [ ] React frontend
* [ ] FastAPI backend
* [ ] PostgreSQL
* [ ] Configuration system

## Phase 2 — Recon Engine

* [ ] Subfinder integration
* [ ] HTTPX integration
* [ ] Katana integration
* [ ] Naabu integration
* [ ] Scan orchestration

## Phase 3 — Data Processing

* [ ] URL normalization
* [ ] Endpoint extraction
* [ ] JS analysis
* [ ] API discovery
* [ ] Deduplication
* [ ] Source correlation

## Phase 4 — AI

* [ ] Ollama integration
* [ ] Endpoint classification
* [ ] Technology analysis
* [ ] Attack-surface summarization
* [ ] Prioritization engine

## Phase 5 — Researcher Workflow

* [ ] Manual testing queue
* [ ] Scan history
* [ ] Difference between scans
* [ ] Burp import/export
* [ ] Evidence management
* [ ] Report generation

## Phase 6 — Advanced

* [ ] Authenticated crawling
* [ ] GraphQL intelligence
* [ ] WebSocket discovery
* [ ] Source-map analysis
* [ ] Advanced endpoint correlation
* [ ] Custom researcher rules

---

# 🗺️ Long-Term Vision

The long-term vision is:

```text
                ┌──────────────────────┐
                │       TARGET         │
                └──────────┬───────────┘
                           ↓
                ┌──────────────────────┐
                │     RECONPILOT       │
                └──────────┬───────────┘
                           ↓
              ┌─────────────────────────┐
              │ Complete Attack Surface │
              └───────────┬─────────────┘
                          ↓
                 ┌─────────────────┐
                 │ AI Prioritizer  │
                 └────────┬────────┘
                          ↓
                ┌────────────────────┐
                │ Researcher's Queue │
                └─────────┬──────────┘
                          ↓
                  MANUAL TESTING
                          ↓
             Authentication / Access
             Control / Business Logic
             API / Web / Functionality
```

The researcher remains in control.

---

# 🧪 Development Philosophy

ReconPilot follows these principles:

### 1. Deterministic tools first

Use specialized tools for discovery.

```text
Subfinder
HTTPX
Katana
Naabu
```

### 2. AI second

Use AI for:

```text
Classification
Correlation
Prioritization
Summarization
```

### 3. Researcher always in control

The system should make the researcher faster, not blindly attack targets.

### 4. Local-first

Whenever possible:

```text
Local tools
Local database
Local AI
```

This keeps the project inexpensive and gives the researcher control over sensitive reconnaissance data.

---

# 📚 Learning Resources

While developing ReconPilot, learn these concepts progressively:

```text
Python
 ↓
FastAPI
 ↓
REST APIs
 ↓
PostgreSQL
 ↓
SQLAlchemy
 ↓
React
 ↓
TypeScript
 ↓
Async Python
 ↓
Process orchestration
 ↓
Security automation
 ↓
LLM integration
```

Don't try to learn everything before starting.

Build the system one component at a time.

---

# 🤝 Contributing

This project is currently primarily a personal security-research project.

Contributions, ideas, bug reports and improvements may be considered as the project matures.

Before contributing, please read the security and scope requirements.

---

# ⚠️ Disclaimer

ReconPilot is a security research and automation tool.

The author does not encourage unauthorized scanning, enumeration, exploitation, or testing of systems you do not own or have explicit permission to assess.

You are responsible for complying with:

* Applicable laws
* Bug bounty program rules
* Target scope
* Terms of service
* Responsible disclosure requirements

**Only use ReconPilot against systems you are authorized to test.**

---

# 📄 License

This project is released under the MIT License.

See [`LICENSE`](LICENSE) for details.

---

# ⭐ Support the Project

If ReconPilot helps your security research:

```text
⭐ Star the repository
🐛 Report bugs
💡 Suggest features
🔧 Submit improvements
📖 Improve documentation
```

---

<div align="center">

### 🛰️ ReconPilot

**Discover faster. Understand better. Test deeper.**

Built with ❤️ for security research.

**Built by Abhishek Kumar**

</div>
