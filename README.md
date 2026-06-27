# Python Security Engineering

A 52-week Python learning plan built around security engineering.
One Saturday session per week. One concept, one mini project, one commit.

**Track:** Python Security Engineering Plan · Jun 2026 – May 2027
**Goal:** AppSec / Security Engineer roles in the remote market

---

## Structure

```
python-security/
  pyproject.toml          ← tool config (ruff, mypy, pytest)
  .gitignore
  README.md
  week03-login-log-parser/
    main.py
    test_main.py
  week04-security-config/
    main.py
    test_main.py
  ...
```

Each week is a self-contained folder. `main.py` is the project. `test_main.py` is the test suite.

---

## Setup

```bash
git clone <repo-url>
cd python-security
python -m venv .venv
source .venv/bin/activate
pip install ruff mypy bandit pytest pytest-cov
```

---

## Quality Gate

Run from the repo root at the end of every session before committing:

```bash
ruff check . && mypy . && bandit -r . && pytest --cov
```

| Tool | Checks |
|------|--------|
| `ruff` | Style, unused imports, common bugs |
| `mypy` | Type annotation correctness |
| `bandit` | Security-specific patterns |
| `pytest --cov` | Tests pass + coverage ≥ 80% |

Nothing gets committed unless all four pass.

---

## Projects

| Week | Project | Concept |
|------|---------|---------|
| 03 | Login log parser | Data structures |
| 04 | Security config object | References & mutability |
| 05 | User model with validation | Classes & methods |
| 06 | Auth interface system | Inheritance & ABCs |
| 07 | Modular security CLI | Modules & environments |
| 08 | Password validation test suite | Testing |
| 09 | *(exploration week — no project)* | Memory & Python runtime |
| 10 | Structured JSON logger | Error design & logging |
| 11 | *(quality week — no project)* | Code quality pass |
| 12 | `secure-cli` | Capstone — Months 1–3 |
| 13 | Thread-safe log analyser | Threading & the GIL |
| 14 | Concurrent log analyser | Multiprocessing |
| 15 | Async HTTP health checker | asyncio |
| 16 | Port scanner + health checker | Concurrency capstone |
| 17 | TCP client/server | Sockets |
| 18 | TLS certificate checker | HTTP & requests |
| 19 | Permission auditor | OS interaction |
| 20 | Port scanner + TLS checker + auditor | Networking capstone |
| 21 | Hashing + MAC tool | Cryptography |
| 22 | Password hashing system | Argon2 / key derivation |
| 23 | Vulnerable + patched code pairs | Injection & deserialisation |
| 24 | Static analysis pipeline | Bandit + fuzzing |
| 25 | Flask security hardening | Flask |
| 26 | JWT authentication API | FastAPI |
| 27 | Parameterised query layer | Database security |
| 28 | Auth API (registration + login + JWT + rate limiting) | Secure API capstone |
| 29–32 | Logging, config, CI/CD, code review | Professional practices |
| 33–52 | Security monitoring agent | Final capstone |

---

## Final Capstone Requirements

- `asyncio` concurrency
- Networking (sockets or HTTP)
- Cryptography and auth
- `pytest` coverage ≥ 80%
- Structured logging
- `bandit` + `mypy` passing clean
- Deployed and public on GitHub