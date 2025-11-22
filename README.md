
# POWERHOUSE

**Enterprise-Grade Multi-Agent Platform**

Powerhouse is the enterprise B2B platform for deploying, managing, and governing AI agents at scale. It provides:
- 🏢 **Enterprise Runtime**: Pro runtime with advanced policies and governance
- 🔐 **SSO & Auth**: SAML, OAuth, enterprise directory integration
- 📊 **Observability**: Real-time monitoring, audit logs, incident management
- 🛡️ **Governance**: Tenant policies, approval workflows, compliance
- 🎯 **Certification**: Bronze/Silver/Gold certification levels
- 📦 **Private Catalogs**: Organization-specific agent libraries

## Key Features

### Runtime-Pro
- **CPU**: Up to 32 cores (tenant-configurable)
- **Memory**: Up to 64 GB (tenant-configurable)
- **Duration**: Up to 1 hour (tenant-configurable)
- **Network**: Configurable egress allowlist per tenant
- **Permissions**: More permissive (including filesystem.write, database access)

### Enterprise Governance
- Tenant-specific policies
- Approval workflows for sensitive permissions
- Audit logs with 365-day retention
- Compliance reporting (SOC 2, GDPR, HIPAA)
- Incident management system

### Certification Levels
- **Bronze**: Static checks, manifest validation (auto-awarded)
- **Silver**: Dynamic testing, security scans (requires review)
- **Gold**: Enterprise audit, compliance, SLA (requires audit)

### Organization Management
- Multi-tenant architecture
- SSO integration (SAML, OAuth)
- Role-based access control (RBAC)
- Team management
- Usage analytics per org

## Environment Variables

All Powerhouse environment variables use the `PH_*` prefix:

```bash
# Database
PH_DB_URL=postgresql://user:password@localhost:5432/powerhouse

# JWT & Auth
PH_JWT_SECRET=your_jwt_secret_here_min_32_chars
PH_JWT_ISSUER=powerhouse.enterprise

# SSO
PH_ENABLE_SSO=true
PH_SAML_ENTITY_ID=powerhouse

# Runtime
PH_RUNTIME_MODE=pro
PH_DEFAULT_CPU_LIMIT=4
PH_DEFAULT_MEM_MB=8192

# Governance
PH_ENABLE_AUDIT_LOGS=true
PH_AUDIT_LOG_RETENTION_DAYS=365
```

## Installation

### Prerequisites
- Python 3.10+
- Node.js 18+
- PostgreSQL 14+
- Redis 6+ (for Celery task queue)

### Backend Setup

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your credentials

# Run database migrations
# (Add migration commands here)

# Start backend
python app.py
```

### Frontend Setup

```bash
cd frontend/app

# Install dependencies
yarn install

# Configure environment
cp .env.example .env.local
# Edit .env.local

# Start development server
yarn dev
```

## Architecture

```
POWERHOUSE/
├── backend/
│   ├── runtime_pro.py         # Pro runtime with governance
│   ├── policies.py            # Tenant-specific policies
│   ├── audit.py               # Audit logging
│   ├── certification.py       # Certification system
│   └── requirements.txt
├── frontend/
│   ├── app/                   # Next.js app directory
│   │   ├── dashboard/         # Admin dashboard
│   │   ├── agents/            # Agent management
│   │   ├── workflows/         # Workflow orchestration
│   │   └── settings/          # Org settings
│   └── package.json
└── README.md
```

## API Endpoints

### Agent Management
- `GET /api/agents` - List deployed agents
- `POST /api/agents/deploy` - Deploy agent from private catalog
- `GET /api/agents/:id/executions` - Get execution history

### Runtime
- `POST /api/runtime/execute` - Execute agent with Pro runtime
- `GET /api/runtime/executions/:id` - Get execution details

### Governance
- `GET /api/policies` - Get tenant policies
- `PUT /api/policies` - Update tenant policies
- `GET /api/audit-logs` - Query audit logs

### Certification
- `POST /api/certification/request` - Request certification
- `GET /api/certification/status/:id` - Check certification status

### Organization
- `GET /api/org/users` - List organization users
- `POST /api/org/users` - Invite user
- `GET /api/org/analytics` - Organization usage analytics

## Usage

### For Administrators
1. Set up organization
2. Configure SSO
3. Define tenant policies
4. Invite team members

### For Developers
1. Deploy agents from private catalog
2. Configure execution policies
3. Monitor runtime executions
4. Review audit logs

### For Compliance Officers
1. Review audit logs
2. Generate compliance reports
3. Manage certifications
4. Configure retention policies

## Security

- Enterprise SSO integration
- Role-based access control (RBAC)
- Audit logs for all actions
- Encrypted secrets management
- Network isolation per tenant

## Telemetry Events

Powerhouse emits events for:
- Agent deployments
- Runtime executions
- Policy violations
- Certification awards
- Audit log entries

## Integration with DRACANUS (Optional)

Powerhouse can optionally integrate with DRACANUS to deploy agents from the public marketplace:

```bash
PH_ENABLE_DRACANUS_DEPLOY=true
PH_DRACANUS_API_URL=https://api.dracanus.app
PH_DRACANUS_API_KEY=your_api_key
```

## Support

For enterprise support: enterprise@powerhouse.io

## License

Proprietary - Enterprise license required
