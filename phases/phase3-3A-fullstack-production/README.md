# PHASE 3A: Full-Stack Production ($MODE = full-stack)

## Metadata
- **Phase**: 3A
- **Decision**: Full-stack system (multi-service, production-grade)
- **Status**: DRAFT
- **Created**: 2026-04-26
- **Parent**: PHASE_3_EXECUTION

## The Ask

Build production-grade full-stack system with:
- Multi-service architecture
- Complete CI/CD
- Monitoring, alerting
- Security hardening
- Performance optimization

## Service Topology

```
                          ┌─────────────────┐
                          │   CDN (Cloudflare)│
                          └────────┬────────┘
                                   ▼
                    ┌─────────────────────────┐
                    │    API Gateway (Kong)   │
                    │  (rate limit, auth)     │
                    └────────┬────────┬──────┘
                             │        │
              ┌──────────────┼────────┼──────────────┐
              ▼              ▼        ▼              ▼
       ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
       │  Content    │ │   Lexicon    │ │  Storefront  │ │   Corpus    │
       │  Service    │ │   Service    │ │   Service    │ │   Service    │
       │  (v1)      │ │   (v1)      │ │   (v1)      │ │   (v1)      │
       └─────┬──────┘ └─────┬──────┘ └─────┬──────┘ └─────┬──────┘
             │             │             │             │
             └─────────────┴─────────────┴─────────────┘
                           ▼
              ┌─────────────────────────────┐
              │    Orchestration Service    │
              │    (workflow, job queue)     │
              └─────────────┬──────────────┘
                           │
         ┌─────────────────┼─────────────────┐
         ▼                 ▼                 ▼
  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
  │  Database   │  │    Redis     │  │     S3      │
  │ (PostgreSQL) │  │  (cache/q)  │  │   (media)   │
  └──────────────┘  └──────────────┘  └──────────────┘
```

## Infrastructure Specs

| Component | Technology | Spec |
|---|---|---|
| Container | Docker + K8s | Multi-node cluster |
| Database | PostgreSQL 15 | Primary + replica |
| Cache | Redis 7 | Cluster mode |
| Queue | BullMQ | Redis-backed |
| Storage | S3 | Cross-region |
| CDN | Cloudflare | Global |
| Gateway | Kong | Rate limiting |
| Monitoring | Datadog | APM + logs |
| Alerting | PagerDuty | Escalation |
| Secrets | Vault | Rotation |

## Security Hardening

| Layer | Implementation |
|---|---|
| Network | VPC, private subnets, security groups |
| App | JWT + API keys, CSRF protection |
| Data | Encryption at rest (AES-256), TLS 1.3 |
| Secrets | HashiCorp Vault, automatic rotation |
| DDoS | Cloudflare rate limiting |
| Compliance | SOC2-ready audit logs |

## Performance Targets

| Metric | Target |
|---|---|
| P99 Latency | < 200ms |
| Uptime | 99.9% ( SLA) |
| Throughput | 10K req/s |
| Cold start | < 3s |
| Database | < 50ms p95 |
| Cache hit | > 95% |

## CI/CD Pipeline

```yaml
name: Production CI/CD

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - Run unit tests (80% coverage required)
      - Run integration tests
      - Run e2e tests
      
  security:
    runs-on: ubuntu-latest
    steps:
      - Dependency audit (npm audit)
      - SAST scanning (Semgrep)
      - Secret scanning (TruffleHog)
      
  build:
    needs: [test, security]
    runs-on: ubuntu-latest
    steps:
      - Build all Docker images
      - Push to ECR
      
  deploy-staging:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - Deploy to staging
      - Run canary analysis
      
  deploy-prod:
    needs: deploy-staging
    runs-on: ubuntu-latest
    steps:
      - Deploy to production (blue/green)
      - Smoke tests
      - Alert on failure
```

## Observability Stack

| Tool | Purpose |
|---|---|
| Datadog APM | Distributed tracing |
| Datadog Logs | Structured logging |
| Prometheus | Metrics |
| Grafana | Dashboards |
| PagerDuty | Incidents |
| Sentry | Error tracking |

## Decision Log

| Decision | Choice | Rationale |
|---|---|---|
| Scale | Horizontal | Growth ready |
| Database | PostgreSQL | ACID compliance |
| Cache | Redis cluster | HA |
| Deployment | Blue/green | Zero downtime |
| Secrets | Vault | Rotation |
| Monitoring | Datadog | Full stack |

## Next Phase

From 3A → goes to:
- **4B**: Dissertation-grade depth (full documentation)

---

## Generated Files

`phase3-3A-fullstack-production/infrastructure.md`
`phase3-3A-fullstack-production/security.md`
`phase3-3A-fullstack-production/ci-cd.md`
`phase3-3A-fullstack-production/observability.md`