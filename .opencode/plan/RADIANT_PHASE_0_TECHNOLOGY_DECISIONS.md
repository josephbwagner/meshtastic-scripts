# RADIANT - PHASE 0: TECHNOLOGY DECISIONS & BEST PRACTICES (FINAL)

## Overview

This document establishes all technology choices, dependency versions, tooling configurations, and best practices for the Radiant project. These decisions are based on proven patterns from the yendoria project and industry best practices.

**Status:** FINALIZED - All decisions confirmed and ready for implementation.

**Date:** January 2026

---

## FINALIZED DECISIONS

All questions have been resolved. Key decisions:

1. **Lock files:** Commit poetry.lock for both packages ✅
2. **Coverage:** Start at 55%, increase to 85% over time ✅
3. **CLI Python:** 3.9+ for maximum compatibility ✅
4. **Server Python:** 3.12+ (stable, mature, battle-tested) ✅
5. **Docker:** Multi-arch (AMD64 + ARM64 for Raspberry Pi) ✅
6. **Frontend State:** React Context + Zustand (hybrid approach) ✅
7. **Repo Structure:** Monorepo (cli/, server/, frontend/ in one repo) ✅

---

## 1. PYTHON VERSION STRATEGY

### CLI Package (radiant-cli)
- **Minimum:** Python 3.9
- **Tested:** Python 3.9, 3.10, 3.11, 3.12, 3.13
- **Rationale:** 
  - Python 3.9 available on Debian 11, Ubuntu 20.04 LTS, older Raspberry Pi OS
  - Maximum compatibility for diagnostic tools
  - Supports modern type hints with `from __future__ import annotations`
  - Pattern matching (3.10+) not critical for CLI tool
  - Broad reach more important than minor features

### Server Package (radiant-server)
- **Minimum:** Python 3.12
- **Tested:** Python 3.12, 3.13
- **Rationale:**
  - Python 3.12 mature and battle-tested (released Oct 2023, 15+ months old)
  - Excellent async/await performance
  - All dependencies fully support 3.12
  - Python 3.13 too new (4 months old) for production server
  - Docker isolation allows easy upgrade path later
  - 3.12 → 3.13 upgrade simple when ready (6-12 months)

### Type Hint Style
```python
# Modern syntax (Python 3.9+ with future import)
from __future__ import annotations

def get_nodes(port: str | None = None) -> list[Node]:
    pass

# Not: Optional[str], List[Node] (old style)
```

---

## 2. DEPENDENCY MANAGEMENT

### Tool: Poetry

**Why Poetry over pip/pip-tools/setuptools:**
- Deterministic dependency resolution
- Lock file for reproducible builds (poetry.lock)
- Modern pyproject.toml standard
- Built-in virtual environment management
- Single tool for packaging and publishing
- Better than pip-tools: integrated build system
- Better than setuptools: modern, user-friendly

### Installation
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### Configuration Strategy
- **Lock file committed:** YES - Both CLI and server are applications (need reproducibility)
- **Version pinning:** Caret (^) for semver compatibility
- **Dependency groups:** Separate dev/test/docs dependencies
- **Local virtual environments:** `.venv` in project directory for faster access

---

## 3. PROJECT STRUCTURE

### Src Layout Pattern (Confirmed)

```
radiant/
├── cli/
│   ├── src/
│   │   └── radiant/              # ← Package inside src/
│   │       ├── __init__.py       # Version, exports
│   │       ├── __main__.py       # python -m radiant
│   │       ├── py.typed          # PEP 561 marker
│   │       ├── cli/              # CLI commands
│   │       ├── core/             # Core logic
│   │       ├── config/           # Configuration
│   │       └── output/           # Output formatting
│   ├── tests/                    # Test suite
│   └── pyproject.toml
├── server/
│   ├── src/
│   │   └── radiant_server/       # ← Separate package
│   │       ├── __init__.py
│   │       ├── api/
│   │       ├── database/
│   │       ├── monitoring/
│   │       └── alerts/
│   ├── tests/
│   └── pyproject.toml
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── hooks/
│   │   └── stores/              # ← Zustand stores
│   ├── package.json
│   └── tsconfig.json
├── docker/
│   ├── Dockerfile.cli
│   ├── Dockerfile.server
│   ├── Dockerfile.frontend
│   └── docker-compose.yml
├── docs/
│   ├── conf.py                   # Sphinx configuration
│   ├── index.rst
│   └── api/
├── .github/
│   ├── workflows/
│   │   ├── ci.yml
│   │   ├── security.yml
│   │   ├── release.yml
│   │   └── docs.yml
│   ├── dependabot.yml
│   └── ISSUE_TEMPLATE/
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

**Why src/ layout:**
- Prevents accidental imports from working directory
- Forces proper installation for testing
- Catches import errors early
- Industry standard for Python packages
- Required for editable installs to work correctly

**Key files:**
- `py.typed`: Declares package supports type hints (PEP 561)
- `__main__.py`: Enables `python -m radiant` execution
- `__init__.py`: Version string, public API exports
- `poetry.lock`: Committed for reproducible builds

---

## 4. CODE QUALITY TOOLS

### 4.1 Ruff (Linting + Formatting)

**Replaces:** black, isort, flake8, pyupgrade, autoflake, pycodestyle

**Why Ruff:**
- 10-100x faster than alternatives (written in Rust)
- Single tool replaces 6+ tools
- Auto-fixes most issues
- Modern Python support (3.9-3.13)
- Compatible with black formatting
- Built-in import sorting (replaces isort)

**Configuration:**
```toml
[tool.ruff]
line-length = 88
target-version = "py39"  # CLI package minimum

[tool.ruff.lint]
select = [
    "E",     # pycodestyle errors
    "F",     # Pyflakes
    "UP",    # pyupgrade (modernize Python)
    "I",     # isort (import sorting)
    "PL",    # pylint
    "B",     # flake8-bugbear
    "SIM",   # flake8-simplify
    "C4",    # flake8-comprehensions
    "RUF",   # Ruff-specific rules
]
fixable = ["ALL"]
unfixable = []

[tool.ruff.lint.per-file-ignores]
"tests/**/*" = ["PLR2004", "S101"]  # Allow magic values, asserts

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
```

### 4.2 MyPy (Type Checking)

**Why MyPy:**
- Industry standard type checker
- Excellent error messages
- Gradual typing support
- Plugin ecosystem
- IDE integration

**Configuration:**
```toml
[tool.mypy]
python_version = "3.9"  # CLI minimum
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
warn_redundant_casts = true
warn_unused_ignores = true
strict_optional = true
show_error_codes = true
mypy_path = "src"

[[tool.mypy.overrides]]
module = "meshtastic.*"
ignore_missing_imports = true
```

**Strictness Level:** Moderate (can increase gradually)

### 4.3 Pre-commit Hooks

**Configuration (.pre-commit-config.yaml):**
```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-merge-conflict
      - id: check-case-conflict
      - id: check-json
      - id: check-toml
      - id: check-yaml
      - id: debug-statements
      - id: check-executables-have-shebangs

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.11.13
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: local
    hooks:
      - id: mypy
        name: mypy
        entry: poetry run mypy src
        language: system
        types: [python]
        pass_filenames: false
```

---

## 5. TESTING FRAMEWORK

### 5.1 Pytest

**Configuration:**
```toml
[tool.pytest.ini_options]
minversion = "7.0"
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "--strict-markers",
    "--strict-config",
    "--cov=src/radiant",
    "--cov-report=term-missing",
    "--cov-report=html:htmlcov",
    "--cov-report=xml:coverage.xml",
    "--cov-fail-under=55",      # Start at 55%
    "--cov-branch",
]
markers = [
    "slow: marks tests as slow",
    "integration: marks tests as integration tests",
    "unit: marks tests as unit tests",
]
```

### 5.2 Coverage Strategy (FINALIZED)

**Configuration:**
```toml
[tool.coverage.run]
source = ["src"]
branch = true
omit = [
    "*/tests/*",
    "*/test_*",
    "*/__pycache__/*",
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
    "if TYPE_CHECKING:",
    "@(abc\\.)?abstractmethod",
]
show_missing = true
precision = 2

[tool.coverage.html]
directory = "htmlcov"
```

**Coverage Requirements:**
- **Project Coverage (Overall):** 55% minimum initially
- **New Code (PR Patch):** 90% minimum (enforced via Codecov)
- **Goal:** Increase to 85% over time
- **Branch Coverage:** Required

**Codecov Configuration (codecov.yml):**
```yaml
coverage:
  status:
    project:
      default:
        target: 55%       # Start here
        threshold: 2%     # Allow 2% decrease
    patch:
      default:
        target: 90%       # New code must be well-tested

comment:
  layout: "header, diff, files"
  behavior: default
  require_changes: false
```

---

## 6. DOCUMENTATION

### 6.1 Sphinx + Furo Theme

**Configuration (docs/conf.py):**
```python
project = "Radiant"
copyright = "2025, Joseph Wagner"
author = "Joseph Wagner"
version = "1.0"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx",
    "sphinx.ext.githubpages",
    "sphinx_autodoc_typehints",
]

html_theme = "furo"
html_theme_options = {
    "source_repository": "https://github.com/josephbwagner/radiant/",
    "source_branch": "main",
}

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "fastapi": ("https://fastapi.tiangolo.com", None),
}

autodoc_typehints = "description"
```

### 6.2 Docstring Convention: Google Style

**Example:**
```python
def diagnose_device(device_path: str, timeout: int = 30) -> DiagnosticReport:
    """Run diagnostic checks on a Meshtastic device.
    
    Performs comprehensive health checks including connection test,
    firmware version detection, and permission verification.
    
    Args:
        device_path: Path to the device (e.g., /dev/ttyACM0)
        timeout: Maximum time to wait for device response in seconds
    
    Returns:
        DiagnosticReport containing all check results and recommendations
    
    Raises:
        DeviceNotFoundError: If device path does not exist
        PermissionDeniedError: If user lacks access to device
        TimeoutError: If device does not respond within timeout
    
    Example:
        >>> report = diagnose_device("/dev/ttyACM0")
        >>> print(report.status)
        DiagnosticStatus.PASS
    """
```

---

## 7. CI/CD INFRASTRUCTURE

### 7.1 GitHub Actions

**Test Matrix:**
- **Operating Systems:** Ubuntu, macOS, Windows
- **Python Versions (CLI):** 3.9, 3.10, 3.11, 3.12, 3.13
- **Python Versions (Server):** 3.12, 3.13

**Checks Per Build:**
1. Ruff linting
2. Ruff formatting check
3. MyPy type checking
4. Pytest with coverage (55% threshold)
5. Coverage upload to Codecov

**Optimizations:**
- Poetry cache (speeds up 5-10x)
- Fail-fast: false (see all failures)
- Platform-specific handling

### 7.2 Security Scanning

**Tools:**
- **Bandit:** Static security analysis
- **Safety:** Dependency vulnerability scanning
- **pip-audit:** Additional CVE checks

**Schedule:** Weekly (Monday 10 AM UTC)

### 7.3 Release Automation

**Tool:** Python Semantic Release

**Versioning Strategy:**
- `feat:` → minor version (0.X.0)
- `fix:` → patch version (0.0.X)
- `BREAKING CHANGE:` → major version (X.0.0)
- Automatic CHANGELOG.md generation

### 7.4 Dependabot

**Configuration:**
```yaml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/cli"
    schedule:
      interval: "weekly"
      day: "monday"
      time: "09:00"
    open-pull-requests-limit: 5
    groups:
      patch-updates:
        patterns: ["*"]
        update-types: ["patch"]
  
  - package-ecosystem: "pip"
    directory: "/server"
    schedule:
      interval: "weekly"
    groups:
      patch-updates:
        patterns: ["*"]
        update-types: ["patch"]
  
  - package-ecosystem: "npm"
    directory: "/frontend"
    schedule:
      interval: "weekly"
    groups:
      patch-updates:
        patterns: ["*"]
        update-types: ["patch"]
  
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
```

---

## 8. FRONTEND TECHNOLOGY STACK

### 8.1 Core Framework

- **React 18** with TypeScript
- **Vite** for build tooling (fast, modern)
- **React Router v6** for navigation

### 8.2 State Management (HYBRID APPROACH - FINALIZED)

**Strategy:** Use both React Context and Zustand for different use cases.

#### React Context Usage

**Purpose:** Infrequent, simple state that rarely changes.

**Use Cases:**
- User authentication/session
- Theme (light/dark mode)
- Language preferences
- System configuration

**Example:**
```typescript
// contexts/AuthContext.tsx
import { createContext, useContext, useState } from 'react';

interface AuthContextType {
  user: User | null;
  login: (credentials: Credentials) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | null>(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState<User | null>(null);
  
  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth must be used within AuthProvider');
  return context;
};
```

#### Zustand Usage

**Purpose:** Complex, frequently-updating state with performance requirements.

**Bundle Size:** 1.2 KB (minimal impact)

**Use Cases:**
- Real-time node data (updates every 30 seconds)
- Message feed (constantly changing)
- Dashboard filters and view preferences
- WebSocket connection state
- Alert notifications

**Features:**
- No re-render issues (only changed subscriptions update)
- Built-in devtools for debugging
- LocalStorage persistence
- Better TypeScript support
- Cleaner syntax than Context

**Example:**
```typescript
// stores/nodeStore.ts
import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';

interface NodeStore {
  nodes: Node[];
  lastUpdate: number;
  setNodes: (nodes: Node[]) => void;
  updateNode: (nodeId: string, updates: Partial<Node>) => void;
  clearNodes: () => void;
}

export const useNodeStore = create<NodeStore>()(
  devtools(
    persist(
      (set) => ({
        nodes: [],
        lastUpdate: 0,
        setNodes: (nodes) => set({ nodes, lastUpdate: Date.now() }),
        updateNode: (nodeId, updates) =>
          set((state) => ({
            nodes: state.nodes.map((n) =>
              n.id === nodeId ? { ...n, ...updates } : n
            ),
            lastUpdate: Date.now(),
          })),
        clearNodes: () => set({ nodes: [], lastUpdate: 0 }),
      }),
      { name: 'node-storage' }
    )
  )
);

// Usage in component
function NodeList() {
  // Only re-renders when nodes change
  const nodes = useNodeStore((state) => state.nodes);
  const updateNode = useNodeStore((state) => state.updateNode);
  
  return (
    <div>
      {nodes.map(node => (
        <NodeCard key={node.id} node={node} onUpdate={updateNode} />
      ))}
    </div>
  );
}
```

**Directory Structure:**
```
frontend/src/
├── contexts/           # React Context providers
│   ├── AuthContext.tsx
│   ├── ThemeContext.tsx
│   └── ConfigContext.tsx
├── stores/            # Zustand stores
│   ├── nodeStore.ts
│   ├── messageStore.ts
│   ├── alertStore.ts
│   └── websocketStore.ts
├── components/
├── pages/
└── hooks/
```

### 8.3 UI Components

- **shadcn/ui** (Tailwind-based, customizable)
- **Recharts** for data visualization
- **TanStack Query** (React Query) for server state

### 8.4 Real-time Communication

- **Native WebSocket API** for real-time updates
- **TanStack Query** for REST API calls
- **Zustand** for WebSocket state management

---

## 9. DOCKER CONFIGURATION (MULTI-ARCH)

### 9.1 Multi-Architecture Support (FINALIZED)

**Platforms:**
- **AMD64** (x86_64) - Standard servers, desktops
- **ARM64** (aarch64) - Raspberry Pi 4/5, Apple Silicon, ARM servers

**Why Multi-arch:**
- Raspberry Pi is common in mesh networks
- ARM servers increasingly popular
- Docker BuildKit makes it easy
- Single image tag works on both platforms

### 9.2 Build Configuration

**Dockerfile.server:**
```dockerfile
# Multi-stage build for efficiency
FROM --platform=$BUILDPLATFORM python:3.12-slim as base

ARG TARGETPLATFORM
ARG BUILDPLATFORM

RUN echo "Building for $TARGETPLATFORM on $BUILDPLATFORM"

# Install poetry
RUN pip install poetry

WORKDIR /app

# Copy dependency files
COPY server/pyproject.toml server/poetry.lock ./

# Install dependencies
RUN poetry config virtualenvs.create false && \
    poetry install --no-dev --no-root

# Runtime stage
FROM python:3.12-slim as runtime

WORKDIR /app

# Copy installed packages from base
COPY --from=base /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=base /usr/local/bin /usr/local/bin

# Copy application code
COPY server/src ./src

EXPOSE 8000

CMD ["uvicorn", "radiant_server.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Docker Compose:**
```yaml
version: '3.8'

services:
  postgres:
    image: postgres:16-alpine
    platform: linux/amd64  # PostgreSQL official image
    environment:
      POSTGRES_DB: radiant
      POSTGRES_USER: radiant
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U radiant"]
      interval: 10s
      timeout: 5s
      retries: 5
  
  server:
    build:
      context: .
      dockerfile: docker/Dockerfile.server
      platforms:
        - linux/amd64
        - linux/arm64
    depends_on:
      postgres:
        condition: service_healthy
    environment:
      DATABASE_URL: postgresql://radiant:${DB_PASSWORD}@postgres:5432/radiant
    ports:
      - "8000:8000"
    devices:
      - /dev/ttyACM0:/dev/ttyACM0
    volumes:
      - ./config:/app/config:ro
  
  frontend:
    build:
      context: ./frontend
      dockerfile: ../docker/Dockerfile.frontend
      platforms:
        - linux/amd64
        - linux/arm64
    ports:
      - "3000:80"
    depends_on:
      - server

volumes:
  postgres_data:
```

**GitHub Actions Build:**
```yaml
- name: Set up Docker Buildx
  uses: docker/setup-buildx-action@v3

- name: Build and push multi-arch
  uses: docker/build-push-action@v5
  with:
    context: .
    file: ./docker/Dockerfile.server
    platforms: linux/amd64,linux/arm64
    push: true
    tags: josephbwagner/radiant:latest
```

---

## 10. VERSION CONTROL

### 10.1 Git Configuration

**.gitignore:**
```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv/
*.egg-info/
dist/
build/
*.egg

# Testing
.pytest_cache/
.coverage
htmlcov/
*.cover

# Type checking
.mypy_cache/
.dmypy.json

# IDEs
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Documentation
docs/_build/

# Ruff
.ruff_cache/

# Poetry lock files (COMMITTED)
# poetry.lock files ARE tracked for applications
```

### 10.2 Commit Convention: Conventional Commits

**Format:**
```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

**Types:**
- `feat:` New feature (minor bump)
- `fix:` Bug fix (patch bump)
- `docs:` Documentation
- `style:` Formatting
- `refactor:` Code restructuring
- `perf:` Performance (patch bump)
- `test:` Tests
- `build:` Build system
- `ci:` CI configuration
- `chore:` Maintenance

**Tools:**
- **Commitizen:** Interactive commit helper
- **Semantic Release:** Automated versioning

---

## 11. DEPENDENCY VERSIONS

### 11.1 CLI Package (radiant-cli)

**pyproject.toml:**
```toml
[tool.poetry]
name = "radiant-cli"
version = "0.1.0"
description = "Professional CLI tools for Meshtastic radio administration"
authors = ["Joseph Wagner <j.wagner1024@gmail.com>"]
license = "GPL-3.0-or-later"
readme = "README.md"
homepage = "https://github.com/josephbwagner/radiant"
repository = "https://github.com/josephbwagner/radiant"
packages = [{include = "radiant", from = "src"}]

[tool.poetry.dependencies]
python = "^3.9"
click = "^8.1.7"
pydantic = "^2.9"
pyyaml = "^6.0.1"
rich = "^13.7.0"

[tool.poetry.group.dev.dependencies]
pytest = "^8.0"
pytest-cov = "^6.0"
pytest-mock = "^3.14"
ruff = "^0.11.13"
mypy = "^1.16"
pre-commit = "^4.2"
sphinx = "^7.0"
furo = "^2024.8"
sphinx-autodoc-typehints = "^2.3"
bandit = {extras = ["toml"], version = "^1.8"}
python-semantic-release = "^10.1"
commitizen = "^4.1"

[tool.poetry.scripts]
radiant = "radiant.cli.main:cli"

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"
```

### 11.2 Server Package (radiant-server)

**pyproject.toml:**
```toml
[tool.poetry]
name = "radiant-server"
version = "0.1.0"
description = "Backend server for Radiant Meshtastic administration platform"
authors = ["Joseph Wagner <j.wagner1024@gmail.com>"]
license = "GPL-3.0-or-later"
readme = "README.md"
packages = [{include = "radiant_server", from = "src"}]

[tool.poetry.dependencies]
python = "^3.12"
radiant-cli = "^1.0.0"
fastapi = "^0.115"
uvicorn = {extras = ["standard"], version = "^0.32"}
sqlalchemy = {extras = ["asyncio"], version = "^2.0"}
asyncpg = "^0.29"
alembic = "^1.14"
pydantic = "^2.9"
pydantic-settings = "^2.6"
python-multipart = "^0.0.12"
websockets = "^14.1"

[tool.poetry.group.dev.dependencies]
pytest = "^8.0"
pytest-cov = "^6.0"
pytest-asyncio = "^0.24"
httpx = "^0.27"
ruff = "^0.11.13"
mypy = "^1.16"
pre-commit = "^4.2"

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"
```

### 11.3 Frontend Package

**package.json:**
```json
{
  "name": "radiant-frontend",
  "version": "0.1.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "lint": "eslint . --ext ts,tsx",
    "type-check": "tsc --noEmit"
  },
  "dependencies": {
    "react": "^18.3.1",
    "react-dom": "^18.3.1",
    "react-router-dom": "^6.28.0",
    "zustand": "^5.0.2",
    "@tanstack/react-query": "^5.62.0",
    "recharts": "^2.13.3"
  },
  "devDependencies": {
    "@types/react": "^18.3.12",
    "@types/react-dom": "^18.3.1",
    "@vitejs/plugin-react": "^4.3.4",
    "typescript": "^5.7.2",
    "vite": "^6.0.3",
    "eslint": "^9.17.0",
    "@typescript-eslint/eslint-plugin": "^8.18.2",
    "@typescript-eslint/parser": "^8.18.2"
  }
}
```

---

## 12. VS CODE CONFIGURATION

### 12.1 Settings (.vscode/settings.json)

```json
{
    "python.defaultInterpreterPath": "./cli/.venv/bin/python",
    "python.terminal.activateEnvironment": true,
    
    "[python]": {
        "editor.formatOnSave": true,
        "editor.codeActionsOnSave": {
            "source.fixAll.ruff": "explicit",
            "source.organizeImports.ruff": "explicit"
        },
        "editor.defaultFormatter": "charliermarsh.ruff"
    },
    
    "[typescript]": {
        "editor.formatOnSave": true,
        "editor.defaultFormatter": "esbenp.prettier-vscode"
    },
    
    "[typescriptreact]": {
        "editor.formatOnSave": true,
        "editor.defaultFormatter": "esbenp.prettier-vscode"
    },
    
    "python.linting.mypyEnabled": true,
    "python.testing.pytestEnabled": true,
    "python.testing.pytestArgs": ["tests"],
    
    "editor.rulers": [88],
    "files.trimTrailingWhitespace": true,
    "files.insertFinalNewline": true,
    
    "files.watcherExclude": {
        "**/__pycache__/**": true,
        "**/.pytest_cache/**": true,
        "**/.mypy_cache/**": true,
        "**/.ruff_cache/**": true,
        "**/htmlcov/**": true,
        "**/node_modules/**": true
    }
}
```

### 12.2 Extensions (.vscode/extensions.json)

```json
{
    "recommendations": [
        "ms-python.python",
        "ms-python.vscode-pylance",
        "charliermarsh.ruff",
        "ms-python.mypy-type-checker",
        "dbaeumer.vscode-eslint",
        "esbenp.prettier-vscode",
        "GitHub.copilot",
        "GitHub.copilot-chat",
        "tamasfe.even-better-toml",
        "redhat.vscode-yaml",
        "ms-azuretools.vscode-docker"
    ]
}
```

---

## 13. TIMELINE FOR PHASE 0

### Week 0: Repository Setup (3-5 days)

**Day 1: Repository Creation**
- [ ] Create GitHub repository: `radiant`
- [ ] Initialize with GPL v3 license
- [ ] Create initial README.md with project badges
- [ ] Setup branch protection rules (require PR, passing tests)
- [ ] Enable GitHub Pages for documentation

**Day 2: Structure Setup**
- [ ] Create directory structure (cli/, server/, frontend/, docker/, docs/, .github/)
- [ ] Initialize Poetry in cli/ (Python 3.9+)
- [ ] Initialize Poetry in server/ (Python 3.12+)
- [ ] Initialize npm/pnpm in frontend/
- [ ] Create src/ layouts for both Python packages
- [ ] Add py.typed markers
- [ ] Create __init__.py with version, __main__.py files

**Day 3: Tooling Configuration**
- [ ] Configure Ruff in pyproject.toml (both packages)
- [ ] Configure MyPy in pyproject.toml (both packages)
- [ ] Configure Pytest with 55% coverage threshold
- [ ] Configure Coverage excludes
- [ ] Setup pre-commit hooks (.pre-commit-config.yaml)
- [ ] Install and test all tools locally

**Day 4: CI/CD Setup**
- [ ] Create .github/workflows/ci.yml (matrix: 3 OS, 5 Python versions for CLI, 2 for server)
- [ ] Create .github/workflows/security.yml (Bandit, Safety, pip-audit)
- [ ] Create .github/workflows/release.yml (semantic-release)
- [ ] Create .github/workflows/docs.yml (Sphinx → GitHub Pages)
- [ ] Configure Dependabot (.github/dependabot.yml)
- [ ] Setup Codecov integration (55% project, 90% patch)
- [ ] Add GitHub Actions for multi-arch Docker builds

**Day 5: Documentation & Polish**
- [ ] Setup Sphinx in docs/ (conf.py with Furo theme)
- [ ] Create docs/index.rst, docs/api/
- [ ] Write CONTRIBUTING.md (setup, workflow, tools)
- [ ] Create initial CHANGELOG.md (empty, for semantic-release)
- [ ] Configure VS Code (.vscode/settings.json, tasks.json, extensions.json)
- [ ] Write verification script (test_setup.sh)
- [ ] Run verification checklist
- [ ] Create .gitignore (comprehensive)
- [ ] Commit all configuration files

---

## 14. VERIFICATION CHECKLIST

After Phase 0 completion, verify:

**Repository Structure:**
- [ ] Monorepo created with cli/, server/, frontend/, docker/, docs/, .github/
- [ ] Src layout implemented (src/radiant/, src/radiant_server/)
- [ ] All __init__.py files have version and exports
- [ ] py.typed markers present in both Python packages
- [ ] poetry.lock files committed (both CLI and server)

**Tooling:**
- [ ] Poetry install works in cli/ and server/
- [ ] Pre-commit hooks installed and passing
- [ ] `poetry run ruff check .` passes
- [ ] `poetry run ruff format .` passes
- [ ] `poetry run mypy src` passes (no errors)
- [ ] `poetry run pytest` discovers tests
- [ ] Coverage reports generated (HTML, XML)
- [ ] Frontend build works (`npm run build`)

**CI/CD:**
- [ ] CI workflow triggers on push/PR
- [ ] Matrix builds execute (Ubuntu/macOS/Windows × Python versions)
- [ ] Security workflow scheduled (weekly)
- [ ] Codecov integration active (comments on PRs)
- [ ] Dependabot creating PRs
- [ ] Multi-arch Docker builds configured

**Documentation:**
- [ ] Sphinx builds successfully (`sphinx-build -b html`)
- [ ] API docs auto-generate from docstrings
- [ ] README.md complete with badges (CI, Coverage, Python, License)
- [ ] CONTRIBUTING.md comprehensive

**VS Code:**
- [ ] Settings load correctly
- [ ] Tasks accessible (Cmd+Shift+P → Tasks)
- [ ] Extensions recommended automatically
- [ ] Format on save works (Python and TypeScript)
- [ ] Type checking active (MyPy, TypeScript)

**Git:**
- [ ] .gitignore comprehensive
- [ ] Conventional commits enforced (via commitizen)
- [ ] Branch protection active (main branch)
- [ ] All configuration files committed

**Frontend:**
- [ ] Vite dev server runs (`npm run dev`)
- [ ] TypeScript compiles (`npm run type-check`)
- [ ] ESLint passes (`npm run lint`)
- [ ] Zustand store examples created

---

## 15. COMMAND REFERENCE

### Setup Commands
```bash
# Initial setup - CLI
cd cli
poetry install
poetry run pre-commit install

# Initial setup - Server
cd server
poetry install

# Initial setup - Frontend
cd frontend
npm install

# Verify installation
cd cli && poetry run python -c "import radiant; print(radiant.__version__)"
```

### Development Commands
```bash
# Python: Code quality
poetry run ruff check .
poetry run ruff format .
poetry run mypy src

# Python: Testing
poetry run pytest
poetry run pytest --cov=src/radiant --cov-report=html

# Python: Security
poetry run bandit -r src/
poetry run safety scan

# Python: Full CI validation
poetry run ruff check . && \
poetry run ruff format --check . && \
poetry run mypy src && \
poetry run pytest --cov=src/radiant --cov-fail-under=55

# Frontend: Development
npm run dev          # Start Vite dev server
npm run build        # Production build
npm run type-check   # TypeScript check
npm run lint         # ESLint

# Documentation
cd docs && poetry run sphinx-build -b html . _build/html
```

### Release Commands
```bash
# Conventional commit
poetry run cz commit

# Preview next version
poetry run semantic-release version --print

# Manual version bump (if needed)
poetry version patch|minor|major
```

### Docker Commands
```bash
# Build multi-arch images
docker buildx build --platform linux/amd64,linux/arm64 -t radiant-server:latest -f docker/Dockerfile.server .

# Run full stack
docker-compose up

# Build specific service
docker-compose build server
```

---

## 16. SUCCESS CRITERIA

Phase 0 is complete when:

1. ✅ Repository created with full monorepo structure
2. ✅ All tooling configured and passing (Ruff, MyPy, Pytest)
3. ✅ CI/CD pipelines functional (multi-platform, multi-Python-version)
4. ✅ Pre-commit hooks working
5. ✅ Documentation building successfully (Sphinx)
6. ✅ VS Code configuration tested
7. ✅ Multi-arch Docker builds configured
8. ✅ Frontend build pipeline working
9. ✅ Verification checklist 100% complete
10. ✅ Team can run `poetry install && poetry run pytest` successfully in both packages

**Estimated Time:** 3-5 days

**Next Step:** Phase 1 (CLI Foundation + Diagnostics)

---

## 17. SUMMARY OF FINALIZED DECISIONS

### Python
- **CLI:** Python 3.9+ (maximum compatibility)
- **Server:** Python 3.12+ (mature, stable, battle-tested)
- **Type Hints:** Modern syntax with `from __future__ import annotations`

### Dependencies
- **Management:** Poetry with committed lock files
- **CLI Deps:** Click, Pydantic, Rich, PyYAML
- **Server Deps:** FastAPI, SQLAlchemy 2.0, Asyncpg, Alembic

### Testing
- **Framework:** Pytest
- **Coverage:** Start at 55%, goal 85%, new code 90%
- **Strategy:** Unit + Integration tests

### Frontend
- **Framework:** React 18 + TypeScript + Vite
- **State:** React Context (auth, theme) + Zustand (real-time data)
- **UI:** shadcn/ui + Recharts
- **Server State:** TanStack Query

### Infrastructure
- **CI/CD:** GitHub Actions (matrix builds)
- **Docker:** Multi-arch (AMD64 + ARM64)
- **Docs:** Sphinx + Furo theme
- **Security:** Bandit, Safety, pip-audit (weekly)

### Quality
- **Linting:** Ruff (replaces 6+ tools)
- **Type Checking:** MyPy
- **Pre-commit:** Automated checks before commit
- **Versioning:** Semantic Release (conventional commits)

### Repository
- **Structure:** Monorepo (cli/, server/, frontend/)
- **Layout:** Src layout pattern for Python packages
- **VCS:** Conventional commits, branch protection

---

## NEXT ACTIONS

1. ✅ Review this finalized document
2. ✅ Confirm all decisions are acceptable
3. Execute Phase 0 timeline (Days 1-5)
4. Run verification checklist
5. Proceed to Phase 1: CLI Foundation + Diagnostics

**Ready to begin implementation!**
