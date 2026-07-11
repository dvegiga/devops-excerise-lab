# DevOps Sprint Lab

A self-built, end-to-end DevOps pipeline covering containerization, orchestration, CI/CD, configuration management, infrastructure as code, and monitoring — built entirely on a MacBook (Apple Silicon) with no cloud infrastructure spend.

## Pipeline Overview
## Stack

| Layer | Tool |
|---|---|
| Containerization | Docker (via OrbStack) |
| Orchestration | Kubernetes (via `kind`) |
| CI/CD | GitHub Actions (cloud + self-hosted runner) |
| Configuration Management | Ansible |
| Infrastructure as Code | Terraform (`kreuzwerker/docker` provider) |
| Monitoring | Prometheus + Grafana + cAdvisor |

## Repo Structure
## What Each Piece Does

- **`app/`** — a minimal Flask API, containerized with a hand-written Dockerfile.
- **`k8s/`** — raw Kubernetes manifests (no Helm) defining a 2-replica Deployment and a NodePort Service, applied to a local `kind` cluster.
- **`.github/workflows/ci.yml`** — on every push to `main`: builds the Docker image, pushes it to GitHub Container Registry, then hands off to a self-hosted runner to deploy the updated image to the local Kubernetes cluster.
- **`ansible/`** — an idempotent playbook demonstrating configuration management fundamentals.
- **`terraform/`** — infrastructure as code managing a Docker image/container as tracked resources, with a full `init → plan → apply → destroy` lifecycle.
- **`monitoring/`** — a Prometheus + Grafana + cAdvisor stack (via Docker Compose) providing live container metrics, with a custom Grafana dashboard built from verified PromQL queries.

## Notable Problems Solved Along the Way

- Diagnosed and resolved a Docker context conflict from running two container runtimes simultaneously.
- Tracked down a `curl` failure to macOS's AirPlay Receiver silently occupying port 5000.
- Fixed a GitHub Actions permissions error (`GITHUB_TOKEN` defaults to read-only) to enable registry pushes.
- Stood up a self-hosted GitHub Actions runner to bridge cloud-based CI to a local deployment target — the same pattern used for on-prem/air-gapped CI/CD environments.
- Debugged a Terraform `destroy` failure caused by a stale container still referencing the target image.
- Isolated a broken monitoring dashboard to stale metric names in a third-party Grafana dashboard by testing each layer of the pipeline independently, then built a working dashboard from scratch.

## Running It Locally

```bash
# 1. Build and run the app
cd app && docker build -t devops-lab-app:v1 .

# 2. Stand up the cluster and deploy
kind create cluster --name devops-lab
kind load docker-image devops-lab-app:v1 --name devops-lab
kubectl apply -f k8s/

# 3. Bring up monitoring
cd monitoring && docker compose up -d
```

See the CI workflow for the fully automated version of steps 1–2.
