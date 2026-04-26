# PHASE 2A: Full Repo Architecture ($REPO_ARCHITECTURE_CME_FULL)

## Metadata
- **Phase**: 2A
- **Decision**: Full repo architecture with env variables, services, pipelines
- **Status**: DRAFT
- **Created**: 2026-04-26
- **Parent**: PHASE_2_ARCHITECTURE

## The Ask

Complete repository architecture including:
- Directory tree with services
- $ENV variables (all environment configs)
- Service definitions
- CI/CD pipelines
- Deployment scripts

## Architecture Overview

```
├── SERVICES (per-function microservices)
│   ├── api-gateway/          # Router, auth, rate limiting
│   ├── content-service/      # Content management, versioning
│   ├── lexicon-service/      # Persona lexicon engine
│   ├── storefront-service/   # Client-facing rendering
│   ├── corpus-service/       # Atomization, embedding
│   └── orchestration-service/ # Cross-service coordination
│
├── SHARED (common dependencies)
│   ├── lib/                 # Shared utilities
│   ├── types/               # TypeScript definitions
│   ├── schema/              # JSON schemas
│   └── config/               # Common config
│
├── INFRASTRUCTURE
│   ├── docker/              # Container definitions
│   ├── kubernetes/          # K8s manifests
│   ├── terraform/           # IaC definitions
│   └── ci-cd/               # GitHub Actions
│
└── OPERATIONS
    ├── scripts/              # Deploy, rollback, migrate
    ├── monitoring/          # Logs, metrics, alerts
    └── docs/                 # Architecture docs
```

## Environment Variables

| Variable | Service | Description | Default |
|---|---|---|---|
| `ENV` | All | Environment (dev/staging/prod) | development |
| `LOG_LEVEL` | All | Log verbosity | info |
| `DATABASE_URL` | All | Primary DB connection | - |
| `REDIS_URL` | All | Cache/queue connection | - |
| `API_KEY_SECRET` | api-gateway | Master encryption key | - |
| `JWT_SECRET` | api-gateway | Token signing key | - |
| `S3_BUCKET` | content-service | Media storage | - |
| `S3_REGION` | content-service | S3 region | us-east-1 |
| `LEXICON_PATH` | lexicon-service | Lexicon source path | ./data/lexicons |
| `CORPUS_PATH` | corpus-service | Corpus source path | ./data/corpus |
| `STOREFRONT_URL` | storefront-service | Client-facing URL | http://localhost:3000 |
| `WEBHOOK_SECRET` | orchestration-service | Outbound signing | - |
| `SLACK_WEBHOOK` | monitoring | Alert channel | - |
| `PAGERDUTY_KEY` | monitoring | On-call integration | - |
| `SENTRY_DSN` | All | Error tracking | - |

## Service Specifications

### api-gateway
- **Port**: 8080
- **Dependencies**: redis, database
- **Endpoints**: /health, /auth/*, /api/*
- **Auth**: JWT + API key
- **Rate**: 1000 req/min

### content-service
- **Port**: 8081
- **Dependencies**: s3, database
- **Storage**: Versioned content, drafts
- **Features**: Markdown rendering, media

### lexicon-service
- **Port**: 8082
- **Dependencies**: filesystem, corpus-service
- **Features**: Lexicon loading, persona lookup, embedding

### storefront-service
- **Port**: 8083
- **Dependencies**: lexicon-service, content-service
- **Features**: Client rendering, A/B testing
- **Static**: Next.js/Astro adapter

### corpus-service
- **Port**: 8084
- **Dependencies**: database, filesystem
- **Features**: Tokenization, embedding, similarity search

### orchestration-service
- **Port**: 8085
- **Dependencies**: All services
- **Features**: Job queue, workflow, cron

## CI/CD Pipeline

```yaml
# .github/workflows/ci-cd.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run tests
        run: make test
      - name: Lint
        run: make lint
      
  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build containers
        run: make docker-build
      
  deploy-staging:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/develop'
    steps:
      - name: Deploy to staging
        run: make deploy-staging
        
  deploy-prod:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Deploy to production
        run: make deploy-prod
```

## Deployment Scripts

| Script | Purpose |
|---|---|
| `scripts/deploy.sh` | Production deploy |
| `scripts/deploy-staging.sh` | Staging deploy |
| `scripts/rollback.sh` | Rollback to last version |
| `scripts/migrate.sh` | Database migrations |
| `scripts/seed.sh` | Seed data |
| `scripts/health-check.sh` | Post-deploy verification |

## Decision Log

| Decision | Choice | Rationale |
|---|---|---|
| Architecture | Microservices | Independent scaling |
| Container | Docker + K8s | Industry standard |
| Service mesh | None (overhead) | Keep lean |
| Config | ENV files | 12-factor |
| Deployment | GitHub Actions | Already in use |

## Generated Files

`phase2-2A-repo-architecture/directory-tree.md`
`phase2-2A-repo-architecture/env-spec.md`
`phase2-2A-repo-architecture/service-specs.md`
`phase2-2A-repo-architecture/ci-cd-pipeline.md`
`phase2-2A-repo-architecture/deployment-scripts.sh`