# RADIANT - IMPLEMENTATION PLAN (FINAL)

## Project Identity

**Name:** Radiant

**Tagline:** Professional administration platform for Meshtastic radio networks

**License:** GPL v3

**Package Names:**
- PyPI CLI: `radiant-cli` (Python 3.9+)
- PyPI Server: `radiant-server` (Python 3.12+)
- Docker: `josephbwagner/radiant:latest`
- Command: `radiant` (all subcommands unified)

**Repository:** `github.com/josephbwagner/radiant`

**Tone:** Clean, succinct, professional. No emojis. Enterprise-grade quality.

---

## Project Status

**Current Phase:** Planning Complete - Ready for Phase 0 Execution

**All Technical Decisions Finalized:**
- ✅ Python versions (3.9 CLI, 3.12 Server)
- ✅ Dependency management (Poetry with lock files)
- ✅ Code quality tools (Ruff, MyPy, Pytest)
- ✅ Frontend stack (React + Context + Zustand)
- ✅ Docker (Multi-arch: AMD64 + ARM64)
- ✅ Coverage strategy (Start 55%, goal 85%)
- ✅ Repository structure (Monorepo)

---

## Implementation Timeline

**Total Duration:** 13 weeks to v1.0

- **Phase 0:** Technology Setup (Week 0 - 3-5 days)
- **Phase 1:** CLI Foundation + Diagnostics (Weeks 1-3)
- **Phase 2:** Server Backend + Database (Weeks 4-5)
- **Phase 3:** TypeScript Frontend (Weeks 6-8)
- **Phase 4:** Docker Deployment (Week 9)
- **Phase 5:** Testing & Quality (Weeks 10-11)
- **Phase 6:** Documentation & Release (Week 12-13)

---

## Phase 0: Technology Setup & Best Practices (3-5 Days)

### Objective
Establish complete technical foundation with all tools, configurations, and infrastructure before writing application code.

### Key Decisions (All Finalized)

**Python Strategy:**
- CLI: Python 3.9+ (broad compatibility)
- Server: Python 3.12+ (modern, stable)

**Dependency Management:**
- Poetry with committed lock files
- Dependabot weekly updates

**Code Quality:**
- Ruff (linting + formatting)
- MyPy (type checking)
- Pre-commit hooks
- 55% initial coverage, 85% goal, 90% for new code

**CI/CD:**
- GitHub Actions matrix builds
- Multi-OS (Ubuntu, macOS, Windows)
- Multi-Python (3.9-3.13 for CLI, 3.12-3.13 for server)
- Security scanning (Bandit, Safety)
- Semantic versioning (conventional commits)

**Frontend:**
- React 18 + TypeScript + Vite
- Hybrid state: Context (auth, theme) + Zustand (real-time data)
- shadcn/ui components
- TanStack Query for server state

**Docker:**
- Multi-arch builds (AMD64 + ARM64)
- Optimized multi-stage builds
- Docker Compose for full stack

### Timeline (5 Days)

**Day 1: Repository Creation**
- Create GitHub repository with GPL v3
- Setup branch protection
- Enable GitHub Pages
- Initialize README with badges

**Day 2: Structure Setup**
- Create monorepo structure (cli/, server/, frontend/, docker/, docs/)
- Initialize Poetry (CLI and server)
- Initialize npm/pnpm (frontend)
- Create src/ layouts
- Add py.typed markers

**Day 3: Tooling Configuration**
- Configure Ruff, MyPy, Pytest in pyproject.toml
- Setup pre-commit hooks
- Configure ESLint, TypeScript for frontend
- Install and test all tools

**Day 4: CI/CD Setup**
- Create GitHub Actions workflows (CI, security, release, docs)
- Configure Dependabot
- Setup Codecov integration
- Configure multi-arch Docker builds

**Day 5: Documentation & Verification**
- Setup Sphinx with Furo theme
- Create CONTRIBUTING.md
- Configure VS Code settings/tasks/extensions
- Run complete verification checklist
- Confirm all tooling works

### Deliverables

- [ ] Complete repository structure
- [ ] All development tools configured
- [ ] CI/CD pipelines functional
- [ ] Pre-commit hooks working
- [ ] Documentation framework ready
- [ ] VS Code integration complete
- [ ] Verification checklist 100% complete

### Success Criteria

- Repository created and accessible
- `poetry install && poetry run pytest` works in both packages
- `npm run build` works in frontend
- All CI workflows trigger correctly
- Pre-commit hooks catch issues
- Documentation builds without errors

**Detailed documentation:** See `RADIANT_PHASE_0_TECHNOLOGY_DECISIONS_FINAL.md`

---

## Phase 1: CLI Foundation + Diagnostics (Weeks 1-3)

### Objective
Create professional, database-free CLI tool that solves radio connection diagnostics (your primary pain point).

### Key Components

**Core Library (`cli/src/radiant/core/`):**
- `meshtastic.py`: Unified CLI wrapper with JSON parsing, retry logic
- `diagnostics.py`: Comprehensive diagnostic engine
- `parser.py`: JSON parsing utilities
- `exceptions.py`: Rich exception hierarchy with actionable errors
- `models.py`: Data models (Node, Radio, DiagnosticReport)

**CLI Commands (`cli/src/radiant/cli/`):**
- `doctor`: Full system diagnostics with auto-fix suggestions
- `monitor`: Live monitoring with file output
- `backup`: Device backup operations
- `config`: Configuration management

**Configuration System:**
- YAML-based config at `~/.config/radiant/config.yaml`
- Pydantic validation
- Environment variable overrides
- No database required

**Output Formatting:**
- Table format (default, human-readable)
- JSON format (machine-readable)
- YAML format
- File output by default

### Diagnostic Features (Solving Your Pain Point)

**System Diagnostics:**
- Python version check
- Meshtastic CLI detection and version
- Configuration file validation
- Permission verification

**Device Diagnostics:**
- Auto-detect all USB devices
- Test connection and response time
- Check user permissions (dialout group)
- Firmware version detection
- Battery and signal quality
- Node ID and configuration

**Network Diagnostics:**
- Visible nodes count
- Channel configuration
- Network health assessment
- Gateway detection

**Auto-Fix Capabilities:**
- Suggest udev rules
- Recommend permission fixes
- Provide setup commands

**Example Output:**
```
RADIANT SYSTEM DIAGNOSTICS
==========================

ENVIRONMENT
[PASS] Python 3.12.3
[PASS] Meshtastic CLI v2.3.0 at /usr/local/bin/meshtastic
[PASS] Configuration loaded from ~/.config/radiant/config.yaml

USB DEVICES
[PASS] /dev/ttyACM0: Heltec v3 (firmware 2.3.2)
       Node ID: !6984a7c8
       Connection: 234ms response time
       Permissions: Read/Write
       Battery: 87%
       Signal: SNR 8.5 dB

[FAIL] /dev/ttyACM1: Permission denied
       FIX: sudo usermod -a -G dialout $USER
       Then logout and login again

MESH NETWORK
[PASS] 4 nodes visible
[PASS] Primary channel configured: LongFast
[WARN] No internet gateway detected

RECOMMENDATIONS
- Add user to dialout group for /dev/ttyACM1
- Consider enabling MQTT for cloud integration

Run with --verbose for detailed logs
Save report: radiant doctor --save diagnostic-report.json
```

### Tasks

#### 1.1 Core Library
- [ ] Implement MeshtasticCLI wrapper with JSON parsing
- [ ] Create exception hierarchy (DeviceNotFoundError, PermissionDeniedError, etc.)
- [ ] Define data models (Node, Radio, DiagnosticResult)
- [ ] Implement retry logic with exponential backoff
- [ ] Add structured logging

#### 1.2 Diagnostic Engine
- [ ] System environment checks
- [ ] USB device detection (cross-platform)
- [ ] Connection testing with latency measurement
- [ ] Permission verification
- [ ] Firmware detection
- [ ] Network health assessment
- [ ] Auto-fix recommendations

#### 1.3 CLI Commands
- [ ] `radiant doctor` with full diagnostics
- [ ] `radiant monitor` for live monitoring
- [ ] `radiant backup` for device backups
- [ ] `radiant config` for configuration management
- [ ] Unified `radiant` entry point with Click

#### 1.4 Configuration System
- [ ] Pydantic schemas for config validation
- [ ] YAML loader with env variable support
- [ ] Default config generation
- [ ] Config file management commands

#### 1.5 Output Formatting
- [ ] Table formatter (using Rich library)
- [ ] JSON formatter
- [ ] YAML formatter
- [ ] File output handling
- [ ] Colorized terminal output

#### 1.6 Testing
- [ ] Unit tests for core library (>55% coverage)
- [ ] Mock Meshtastic CLI responses
- [ ] Integration tests with sample data
- [ ] CLI command tests
- [ ] Cross-platform testing (via CI)

#### 1.7 Documentation
- [ ] README.md with installation and quick start
- [ ] CLI command reference (sphinx)
- [ ] Diagnostic troubleshooting guide
- [ ] Configuration guide

### Deliverables

- [ ] Working CLI: `pip install radiant-cli`
- [ ] `radiant doctor` solving connection issues
- [ ] `radiant monitor` for live monitoring
- [ ] `radiant backup` for device backups
- [ ] All output saved to files by default
- [ ] Multiple output formats supported
- [ ] >55% test coverage
- [ ] Complete documentation

### Success Criteria

- User can install with `pip install radiant-cli` on Python 3.9+
- `radiant doctor` accurately identifies connection problems
- Clear, actionable error messages with fix suggestions
- All operations work without database
- Professional output (no emojis)
- Tests passing with >55% coverage

---

## Phase 2: Server Backend + Database (Weeks 4-5)

### Objective
Build optional server component for users wanting historical data, API access, and web dashboard.

### Key Components

**FastAPI Backend:**
- REST API endpoints for nodes, messages, events
- WebSocket support for real-time updates
- OpenAPI documentation (auto-generated)
- CORS configuration for frontend

**PostgreSQL Database:**
- Schema: nodes, node_history, messages, events, radios, config_snapshots
- Alembic migrations
- SQLAlchemy 2.0 async ORM
- Repository pattern for data access
- Optimized indexes for time-series queries

**Monitoring Service:**
- Background polling of mesh network
- Database updates at configurable intervals
- Event detection (nodes joining/leaving, battery changes)
- WebSocket streaming to connected clients
- Graceful error handling and recovery

**Alert System:**
- Plugin architecture (console, email, Discord)
- Configurable rules engine
- Cooldown/deduplication logic
- Alert delivery via multiple channels

### Tasks

#### 2.1 Database Layer
- [ ] Design PostgreSQL schema
- [ ] Create Alembic migrations
- [ ] Implement SQLAlchemy async models
- [ ] Build repository pattern for data access
- [ ] Add indexes for performance
- [ ] Write database tests

#### 2.2 FastAPI Application
- [ ] Create FastAPI app with versioned API (v1)
- [ ] Implement REST endpoints (nodes, messages, events, alerts)
- [ ] Add WebSocket endpoint for real-time updates
- [ ] Configure CORS for frontend
- [ ] Generate OpenAPI documentation
- [ ] Add health check endpoints

#### 2.3 Monitoring Service
- [ ] Background service using asyncio
- [ ] Poll mesh at configurable intervals (default 30s)
- [ ] Update database with node status
- [ ] Detect and log events
- [ ] Stream updates via WebSocket
- [ ] Handle errors gracefully

#### 2.4 Alert System
- [ ] Plugin base class
- [ ] Console alert plugin
- [ ] Email alert plugin (SMTP)
- [ ] Discord webhook plugin
- [ ] Rules engine (YAML configuration)
- [ ] Alert cooldown logic

#### 2.5 CLI Integration
- [ ] Add `radiant server start` command
- [ ] Add `radiant server stop` command
- [ ] Add `radiant server status` command
- [ ] Database configuration in config.yaml
- [ ] Optional database mode for CLI

#### 2.6 Testing
- [ ] Unit tests for database layer
- [ ] API endpoint integration tests
- [ ] WebSocket connection tests
- [ ] Monitoring service tests
- [ ] Alert delivery tests
- [ ] >55% test coverage

#### 2.7 Documentation
- [ ] Server installation guide
- [ ] Database setup instructions
- [ ] API reference (auto-generated from OpenAPI)
- [ ] Configuration reference
- [ ] Alert system guide

### Deliverables

- [ ] `radiant-server` package on PyPI
- [ ] PostgreSQL schema with migrations
- [ ] FastAPI backend with REST + WebSocket
- [ ] Background monitoring service
- [ ] Alert system (console, email plugins)
- [ ] CLI server management commands
- [ ] >55% test coverage
- [ ] Complete API documentation

### Success Criteria

- Server runs reliably for 24+ hours without issues
- API responds in <100ms for typical queries
- WebSocket streams updates with <1s latency
- Database queries optimized with proper indexes
- Monitoring service handles network issues gracefully
- Alerts deliver successfully via configured channels

---

## Phase 3: TypeScript Frontend (Weeks 6-8)

### Objective
Create professional web dashboard accessible to both technical and non-technical users.

### Key Components

**React Application:**
- React 18 + TypeScript
- Vite for fast builds
- React Router for navigation
- shadcn/ui component library (Tailwind-based)

**State Management (Hybrid):**
- React Context: Auth, theme, configuration (infrequent updates)
- Zustand: Node data, messages, alerts (frequent updates, performance-critical)
- TanStack Query: Server state, caching, refetching

**Core Features:**
- Real-time node monitoring
- Historical data visualization (charts)
- Message feed with filtering
- Alert management
- Diagnostic dashboard
- System configuration

### Tasks

#### 3.1 Project Setup
- [ ] Initialize Vite + React + TypeScript
- [ ] Configure shadcn/ui with Tailwind
- [ ] Setup React Router
- [ ] Install TanStack Query
- [ ] Install Zustand
- [ ] Configure ESLint + Prettier

#### 3.2 State Management
- [ ] Create Auth Context (authentication state)
- [ ] Create Theme Context (light/dark mode)
- [ ] Create Config Context (user preferences)
- [ ] Create Node Store (Zustand - real-time node data)
- [ ] Create Message Store (Zustand - message feed)
- [ ] Create Alert Store (Zustand - notifications)
- [ ] Create WebSocket Store (Zustand - connection state)

#### 3.3 API Integration
- [ ] Generate TypeScript types from OpenAPI spec
- [ ] Setup TanStack Query hooks
- [ ] Implement WebSocket service
- [ ] Add automatic reconnection logic
- [ ] Handle authentication

#### 3.4 Core Components
- [ ] Layout (sidebar, header, responsive)
- [ ] Node list/grid view
- [ ] Node detail view with charts (Recharts)
- [ ] Message feed with filtering
- [ ] Alert panel with severity indicators
- [ ] Diagnostic dashboard (radio status)
- [ ] Settings page

#### 3.5 Pages
- [ ] Dashboard (overview, key metrics)
- [ ] Nodes (list, details, history)
- [ ] Messages (feed, search, export)
- [ ] Diagnostics (radio status, health checks)
- [ ] Alerts (history, configuration)
- [ ] Settings (system configuration)

#### 3.6 Real-time Features
- [ ] WebSocket connection management
- [ ] Optimistic UI updates
- [ ] Toast notifications for events
- [ ] Live data refresh indicators

#### 3.7 Testing
- [ ] Component tests (React Testing Library)
- [ ] E2E tests for critical workflows (Playwright)
- [ ] Accessibility testing
- [ ] Performance testing

#### 3.8 Documentation
- [ ] User guide for dashboard
- [ ] Feature overview
- [ ] Screenshots

### Deliverables

- [ ] Professional React dashboard
- [ ] Real-time node monitoring interface
- [ ] Historical data visualization
- [ ] Message feed and search
- [ ] Alert management UI
- [ ] Diagnostic interface
- [ ] Mobile-responsive design
- [ ] >80% component test coverage
- [ ] User documentation

### Success Criteria

- Dashboard loads in <2 seconds
- Real-time updates appear within 1 second
- Works on mobile browsers (responsive)
- Accessible (keyboard navigation, screen readers)
- Professional, clean design
- No runtime errors in console

---

## Phase 4: Docker Deployment (Week 9)

### Objective
Enable single-command deployment of full platform with multi-architecture support.

### Key Components

**Multi-Architecture Support:**
- AMD64 (x86_64) for standard servers
- ARM64 (aarch64) for Raspberry Pi and ARM servers
- Single image tag works on both platforms

**Docker Compose Stack:**
- PostgreSQL 16
- Backend API + Monitoring service
- Frontend (Nginx)
- Volume persistence
- USB device passthrough for radios

### Tasks

#### 4.1 Dockerfiles
- [ ] Create Dockerfile.server (Python 3.12, multi-stage)
- [ ] Create Dockerfile.frontend (Node build + Nginx)
- [ ] Optimize layer caching
- [ ] Add health checks
- [ ] Configure for multi-arch builds

#### 4.2 Docker Compose
- [ ] Setup PostgreSQL service
- [ ] Setup backend service with device passthrough
- [ ] Setup frontend service
- [ ] Configure networking
- [ ] Add volume mounts for persistence
- [ ] Environment variable configuration
- [ ] Health check dependencies

#### 4.3 GitHub Actions
- [ ] Add Docker build workflow
- [ ] Configure buildx for multi-arch
- [ ] Push to Docker Hub
- [ ] Tag versioning (latest, semver)

#### 4.4 Production Configuration
- [ ] Environment variable documentation
- [ ] Secrets management guide
- [ ] Reverse proxy examples (Caddy, Nginx)
- [ ] SSL/TLS configuration
- [ ] Backup/restore procedures

#### 4.5 Documentation
- [ ] Docker deployment guide
- [ ] docker-compose reference
- [ ] Environment variables reference
- [ ] Troubleshooting guide
- [ ] Upgrade procedures

### Deliverables

- [ ] Multi-arch Docker images (AMD64 + ARM64)
- [ ] docker-compose.yml for full stack
- [ ] Automated builds in CI/CD
- [ ] USB device access working in containers
- [ ] Persistent data volumes
- [ ] Complete deployment documentation

### Success Criteria

- `docker-compose up` works on fresh install
- USB devices accessible in server container
- Data persists across container restarts
- Multi-arch images build successfully
- Images published to Docker Hub
- Easy upgrade path (pull new image)

---

## Phase 5: Testing & Quality (Weeks 10-11)

### Objective
Achieve production-grade code quality and comprehensive test coverage.

### Tasks

#### 5.1 Test Suite Completion
- [ ] Complete unit tests (CLI package >55%)
- [ ] Complete unit tests (Server package >55%)
- [ ] Integration tests for all API endpoints
- [ ] E2E tests for critical user workflows
- [ ] Frontend component tests (>80%)
- [ ] Frontend E2E tests (Playwright)

#### 5.2 Coverage Improvement
- [ ] Identify untested code paths
- [ ] Add tests to reach coverage goals
- [ ] Review Codecov reports
- [ ] Ensure new code has 90%+ coverage

#### 5.3 Performance Testing
- [ ] API endpoint benchmarks
- [ ] Database query optimization
- [ ] Frontend load time testing
- [ ] WebSocket performance testing
- [ ] Memory leak detection

#### 5.4 Security Audit
- [ ] Review Bandit scan results
- [ ] Review Safety scan results
- [ ] Address all HIGH and CRITICAL vulnerabilities
- [ ] Update dependencies
- [ ] Review OWASP Top 10

#### 5.5 Accessibility Testing
- [ ] WCAG 2.1 AA compliance
- [ ] Keyboard navigation testing
- [ ] Screen reader testing
- [ ] Color contrast verification

#### 5.6 Code Quality Review
- [ ] Review all Ruff warnings
- [ ] Review all MyPy errors
- [ ] Ensure consistent code style
- [ ] Remove dead code
- [ ] Optimize imports

### Deliverables

- [ ] Test coverage >55% (CLI and Server)
- [ ] Frontend test coverage >80%
- [ ] All critical paths tested
- [ ] Performance benchmarks established
- [ ] Security vulnerabilities addressed
- [ ] Accessibility compliance achieved
- [ ] Code quality metrics green

### Success Criteria

- All tests passing in CI
- Coverage thresholds met
- No critical security issues
- Performance meets requirements
- Accessibility standards met
- Code quality tools report no issues

---

## Phase 6: Documentation & Release (Weeks 12-13)

### Objective
Complete documentation and release v1.0.

### Tasks

#### 6.1 User Documentation
- [ ] Getting started guide
- [ ] Installation instructions (pip, Docker)
- [ ] Quick start tutorial
- [ ] CLI command reference
- [ ] Web dashboard user guide
- [ ] Configuration guide
- [ ] Troubleshooting guide

#### 6.2 Technical Documentation
- [ ] Architecture documentation
- [ ] API reference (auto-generated)
- [ ] Database schema documentation
- [ ] WebSocket protocol documentation
- [ ] Alert system guide

#### 6.3 Developer Documentation
- [ ] Contributing guide (already exists, review/update)
- [ ] Development setup instructions
- [ ] Code style guide
- [ ] Testing guide
- [ ] Release process documentation

#### 6.4 Migration Guide
- [ ] Migration from meshtastic-scripts
- [ ] Feature comparison table
- [ ] Configuration conversion examples
- [ ] Data import guide (if applicable)

#### 6.5 Release Preparation
- [ ] Final code review
- [ ] Update CHANGELOG.md
- [ ] Version bump to 1.0.0
- [ ] Create release notes
- [ ] Tag release in git

#### 6.6 Publication
- [ ] Publish radiant-cli to PyPI
- [ ] Publish radiant-server to PyPI
- [ ] Publish Docker images to Docker Hub
- [ ] Create GitHub release
- [ ] Update documentation website

#### 6.7 Announcement
- [ ] Write blog post/announcement
- [ ] Post to relevant communities (Meshtastic forum, Reddit, etc.)
- [ ] Update README with release information

### Deliverables

- [ ] Complete user documentation
- [ ] Complete technical documentation
- [ ] Complete developer documentation
- [ ] Migration guide
- [ ] v1.0 release published
- [ ] Announcement materials

### Success Criteria

- Documentation comprehensive and easy to follow
- Clear migration path from legacy scripts
- v1.0 published to PyPI and Docker Hub
- GitHub release created with assets
- Community announcement posted

---

## Post-1.0 Roadmap

### v1.1 (3-6 months after v1.0)
- Discord alert plugin
- Slack/Teams webhook support
- Network topology visualization
- Predictive battery alerts
- Enhanced diagnostic capabilities
- Python 3.13 support for server

### v1.2 (6-9 months after v1.0)
- Additional alert channels (Pushover, SMS/Twilio)
- Plugin system for community extensions
- Advanced analytics and reporting
- Coverage increase to 85%

### v2.0 (12+ months after v1.0)
- Mobile app (React Native)
- Multi-mesh support (manage multiple networks)
- Cloud sync (optional remote access)
- Advanced automation rules
- Machine learning for anomaly detection

---

## Success Metrics

### Phase Completion Metrics
- All deliverables completed
- All success criteria met
- Tests passing with required coverage
- Documentation complete
- Code review approved

### v1.0 Release Metrics
- Install success rate >95%
- Docker deployment works on fresh systems
- User satisfaction (GitHub stars, feedback)
- Issue resolution time <48 hours
- Active usage (PyPI downloads, Docker pulls)

---

## Risk Mitigation

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| USB device access in Docker | High | Medium | Extensive testing, fallback to native install |
| Meshtastic CLI breaking changes | High | Low | Use JSON output exclusively, version checking |
| Timeline slippage | Medium | Medium | Each phase ships independently, can extend if needed |
| Scope creep | Medium | High | Strict adherence to phase deliverables, defer to v1.1+ |
| Testing coverage not achieved | Medium | Low | Automated coverage tracking in CI, block merge if below threshold |
| Multi-arch Docker complexity | Low | Low | Well-documented pattern, GitHub Actions support |
| Frontend state management issues | Low | Low | Hybrid approach provides flexibility, can adjust |

---

## Open Questions (All Resolved)

All questions have been answered. Ready for implementation.

---

## Next Actions

1. ✅ Review and confirm this implementation plan
2. ✅ Review Phase 0 technology decisions document
3. **Execute Phase 0** (3-5 days)
4. Begin Phase 1 (CLI Foundation + Diagnostics)

---

## Repository Structure (Final)

```
radiant/
├── cli/                          # CLI package (Python 3.9+)
│   ├── src/radiant/
│   │   ├── __init__.py
│   │   ├── __main__.py
│   │   ├── py.typed
│   │   ├── cli/                  # CLI commands
│   │   ├── core/                 # Core logic
│   │   ├── config/               # Configuration
│   │   └── output/               # Output formatting
│   ├── tests/
│   ├── pyproject.toml
│   └── poetry.lock               # Committed
├── server/                       # Server package (Python 3.12+)
│   ├── src/radiant_server/
│   │   ├── __init__.py
│   │   ├── api/                  # FastAPI
│   │   ├── database/             # SQLAlchemy + Alembic
│   │   ├── monitoring/           # Background service
│   │   └── alerts/               # Alert system
│   ├── tests/
│   ├── pyproject.toml
│   └── poetry.lock               # Committed
├── frontend/                     # React + TypeScript
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── contexts/             # React Context
│   │   ├── stores/               # Zustand stores
│   │   ├── services/             # API clients
│   │   └── hooks/
│   ├── package.json
│   └── tsconfig.json
├── docker/
│   ├── Dockerfile.server
│   ├── Dockerfile.frontend
│   └── docker-compose.yml
├── docs/                         # Sphinx documentation
│   ├── conf.py
│   ├── index.rst
│   └── api/
├── .github/
│   ├── workflows/
│   │   ├── ci.yml
│   │   ├── security.yml
│   │   ├── release.yml
│   │   └── docs.yml
│   └── dependabot.yml
├── .vscode/
│   ├── settings.json
│   ├── tasks.json
│   └── extensions.json
├── README.md
├── CONTRIBUTING.md
├── CHANGELOG.md
├── LICENSE                       # GPL v3
└── .gitignore
```

---

## Conclusion

This implementation plan represents a complete roadmap from initial setup through v1.0 release. All technical decisions have been finalized based on:

1. Best practices from yendoria project
2. Your specific requirements (diagnostics, mission-critical, professional)
3. Modern tooling and frameworks
4. Industry standards and proven patterns

The plan is comprehensive yet executable, with clear phases, deliverables, and success criteria. Each phase builds on the previous, allowing for iterative progress and early value delivery.

**We are ready to begin Phase 0 implementation.**
