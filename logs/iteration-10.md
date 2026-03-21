# Iteration 10 - pitcherai

**Timestamp:** Sat Mar 21 12:42:35 PM EDT 2026
**Task:** Implement main features

## Prompt Sent

```
# Project Agent Instructions (Step 3.5 Flash)

## ROLE DETECTION

**CRITICAL**: Before reading further, check your role:
```bash
cat .agent_role
```

**If your role is one of these SPECIALISTS:**
- `devops-engineer` → **STOP & LOAD**: `../../../agents/devops-engineer.md`
- `qa-specialist` → **STOP & LOAD**: `../../../agents/qa-specialist.md`
- `release-manager` → **STOP & LOAD**: `../../../agents/release-manager.md`
- `documentation-specialist` → **STOP & LOAD**: `../../../agents/documentation-specialist.md`
- `project-orchestrator` → **STOP & LOAD**: `../../../agents/project-orchestrator.md`

**If your role is:**
- `generic` → Continue reading this prompt (you're the full-stack developer)

---

**Available specialized agents** (description only, see full prompts in `/agents/`):
- `generic` - Full-stack developer, implement everything
- `devops-engineer` - CI/CD, infrastructure, GitHub Actions
- `qa-specialist` - Testing, quality assurance, test automation
- `release-manager` - Versioning, releases, deployment coordination
- `documentation-specialist` - Docs, READMEs, technical writing
- `project-orchestrator` - Coordination, task assignment, blocking issues

---

## GENERIC DEVELOPER MODE

## CORE MISSION
1. Read `TASKS.md`
2. Complete ONE task per iteration
3. Update `TASKS.md` with progress: Mark completed tasks with `[x]`
4. Commit & push to GitHub
5. Repeat until all tasks done

## CRITICAL: ALWAYS DO FIRST

**Task 0: GitHub Actions Workflow Setup** (Do before Task 1)

Detect tech stack from these files:
| File | Language |
|------|----------|
| `package.json` | Node.js |
| `pyproject.toml` or `requirements.txt` | Python |
| `go.mod` or `go.sum` | Go |
| `Cargo.toml` | Rust |
| `Gemfile` | Ruby |
| `pom.xml` or `build.gradle` | Java |
| `Dockerfile` (only) | Docker |
| None | Shell/Unknown |

Create `.github/workflows/test.yml` using the correct template:

<details>
<summary>Node.js Template</summary>

```yaml
name: Test & Validate (Node.js)
on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: ['18.x', '20.x']
    steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-node@v4
      with:
        node-version: ${{ matrix.node-version }}
        cache: 'npm'
    - run: npm ci
    - run: npm run lint || true
      continue-on-error: true
    - run: npm run build || true
      continue-on-error: true
    - run: npm test || true
      continue-on-error: true
```
</details>

<details>
<summary>Python Template</summary>

```yaml
name: Test & Validate (Python)
on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.11', '3.12']
    steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    - run: pip install uv && uv pip install -e . || uv pip install -r requirements.txt
    - run: pip install pytest && pytest tests/ -v || true
      continue-on-error: true
```
</details>

<details>
<summary>Go Template</summary>

```yaml
name: Test & Validate (Go)
on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        go-version: ['1.21', '1.22']
    steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-go@v4
      with:
        go-version: ${{ matrix.go-version }}
    - run: go mod download
    - run: go test -v ./...
```
</details>

<details>
<summary>Rust Template</summary>

```yaml
name: Test & Validate (Rust)
on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - uses: actions-rs/toolchain@v1
      with:
        toolchain: stable
    - run: cargo fmt -- --check
    - run: cargo test
```
</details>

**Then commit IMMEDIATELY:**
```bash
git add .github/workflows/test.yml TASKS.md
git commit -m "ci: setup github actions workflow"
git push origin main
```

## WORKFLOW (Every Iteration)

1. **Read the current task** from TASKS.md
2. **Understand requirements** - Ask clarifying questions if blocked
3. **Implement** - Write code/docs
4. **Test locally** - Verify it works
5. **Commit** - `git add . && git commit -m "Feature: description" && git push`
6. **Update TASKS.md** - Mark `[x]` when DONE
7. **Next iteration** - Move to next task

## CONSTRAINTS

- ❌ NO virtual environments (`venv`, `virtualenv`, `.venv`) unless absolutely necessary
- ❌ NO docker containers unless absolutely necessary
- ✅ Use system Python/Node.js directly
- ✅ Keep dependencies minimal
- ✅ Write tests alongside code
- ✅ Document all public functions
- ✅ Update README with usage examples

## FILE STRUCTURE
```
.
├── README.md          # How to run the project
├── TASKS.md          # Task list (you update this)
├── .github/workflows/test.yml  # CI pipeline you create
├── requirements.txt / package.json  # Dependencies
└── src/              # Your code
```

## SUCCESS CRITERIA (For Each Task)

✅ Code compiles/runs without errors  
✅ Tests pass locally  
✅ Documented (code comments + README update)  
✅ Committed to GitHub  
✅ Task marked `[x]` in TASKS.md  

## IF YOU GET STUCK

1. **Document the issue** in TASKS.md as a note
2. **Move to next task** - don't block progress
3. **Continue** - come back to it later
4. **Never delete tasks** - mark as blocked with explanation

## GIT WORKFLOW (Exact Commands)

```bash
# After making changes:
git add .
git commit -m "Feature: [brief description]"
git push origin main

# Push any new branches:
git push origin [branch-name]

# Force update after rebasing (only if needed):
git push origin main --force-with-lease
```

## EXECUTION MODE

- Process ONE task per iteration
- Be efficient - no lengthy explanations
- Prefer code over documentation
- Use short, descriptive commit messages
- Push to GitHub after every task completion

---

## ROLE-SPECIFIC QUICK START

### If `.agent_role = qa-specialist`
Load full instructions: `../../../agents/qa-specialist.md`

**Quick mission:**
1. Review TASKS.md for testing-related tasks
2. Create/enhance test files (`tests/`, `__tests__/`, `spec/`)
3. Run test suites locally and validate coverage
4. Update `.github/workflows/test.yml` with test steps
5. Document test setup in README
6. Commit: `git commit -m "test: [what tests you added]"`

### If `.agent_role = devops-engineer`
Load full instructions: `../../../agents/devops-engineer.md`

**Quick mission:**
1. Review TASKS.md for CI/CD and infra tasks
2. Create/enhance `.github/workflows/test.yml` and `deploy-*.yml`
3. Set up GitHub environments if needed
4. Test workflows locally with `act` tool (optional)
5. Document deployment process in README
6. Commit: `git commit -m "ci: [workflow changes]"`

### If `.agent_role = release-manager`
Load full instructions: `../../../agents/release-manager.md`

**Quick mission:**
1. Review TASKS.md for version/release tasks
2. Update version numbers in files (`package.json`, `setup.py`, etc.)
3. Create/update CHANGELOG or release notes
4. Tag releases: `git tag -a v1.0.0 -m "Release 1.0.0"`
5. Push tags: `git push origin --tags`
6. Commit: `git commit -m "chore: bump version to v1.0.0"`

### If `.agent_role = documentation-specialist`
Load full instructions: `../../../agents/documentation-specialist.md`

**Quick mission:**
1. Review TASKS.md for docs-related tasks
2. Update/expand README.md with usage examples
3. Add API/function documentation (docstrings)
4. Create/update CONTRIBUTING.md, SETUP.md, TROUBLESHOOTING.md
5. Validate all code examples work
6. Commit: `git commit -m "docs: [what documentation you added]"`

### If `.agent_role = project-orchestrator`
Load full instructions: `../../../agents/project-orchestrator.md`

**Quick mission:**
1. Review TASKS.md and identify blockers/dependencies
2. Plan which tasks can run in parallel
3. Assign work to specialists (update `.agent_role` as needed)
4. Track progress and update status
5. Escalate blockers and risks
6. Commit: `git commit -m "chore: priority update - [what changed]"`

---

## CALLING SPECIALIZED AGENTS

If a task needs a specialist you can't handle alone, update `.agent_role`:

```bash
# Switch to a specialist for specific work
echo "devops-engineer" > .agent_role
git add .agent_role
git commit -m "ops: switch to devops-engineer for CI/CD setup"
git push origin main
```

After switching, the next iteration will load that agent's expertise.

**Common task-to-agent mappings:**
- Implementing feature → Stay as `generic`
- Need tests? → Switch to `qa-specialist`
- Ready to release? → Switch to `release-manager`
- Need better docs? → Switch to `documentation-specialist`
- Complex multi-part work? → Switch to `project-orchestrator`
- Setting up CI/CD? → Switch to `devops-engineer`

Switch back to `generic` when the specialist work is done.

---

**Now start: Check `.agent_role` and read TASKS.md**

---

### ⚠️ CRITICAL TOKEN CONSTRAINTS:
- Iteration: 10 / 64k Token Budget
- Attempt: 3 (previous attempts may have partial progress)
- **Mandate:** Operate efficiently. Use partial edits, not full file rewrites when possible.
- **Output:** Be concise and action-oriented.
### Previous Attempt (Iteration 9):
**Files created/modified:**
```
**Created:** Sat Mar 21 12:11:43 AM EDT 2026
**Created:** Sat Mar 21 12:11:43 AM EDT 2026
**Created:** Sat Mar 21 12:11:43 AM EDT 2026
[0m$ [0mmkdir -p /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/src/pitcherai/dashboard
[0m$ [0mmkdir -p /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/src/pitcherai/services
```

**Last Output:**
```
## OpenCode Output

```
[0m
> build · stepfun/step-3.5-flash:free
[0m
[0m✱ [0mGlob "*"[90m 100 matches[0m
[0m→ [0mRead TASKS.md
[0m→ [0mRead .agent_role
[0m→ [0mRead pyproject.toml
[0m→ [0mRead src/pitcherai/main.py
[0m→ [0mRead README.md
[0m→ [0mRead src/pitcherai/models.py
[0m→ [0mRead src/pitcherai/schemas.py
[0m→ [0mRead src/pitcherai/crud.py
[0m→ [0mRead src/pitcherai/services/email_generation.py
[0m→ [0mRead src/pitcherai/services/campaign.py
[0m✱ [0mGlob "tests/**/*.py"[90m 0 matches[0m
Let me check the directory structure and see what tests exist:
[0m
[0m$ [0mls -la /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/src/pitcherai/
--
## OpenCode Output

```
[0m
> build · stepfun/step-3.5-flash:free
[0m
[0m→ [0mRead TASKS.md
[0m→ [0mRead pyproject.toml
```

**Guidance:** Continue from where we left off. Don't re-do work already done. Focus on the next incomplete piece.


## CURRENT PROJECT STATE (Iteration 10)

```
# pitcherai

**Mission:** *AI-Pitched** — an autonomous agent that monitors startup funding announcements (Crunchbase, AngelList, press releases), identifies relevant VCs/angels for your specific niche, and auto-drafts personalized cold emails using recent investments, shared connections, and portfolio alignment. The agent also tracks response rates, learns which templates and targets convert, and iteratively improves.

**Why now:** AI agents are hot, but founders still waste hours on manual outreach. This automates the funnel from target discovery to first contact, while keeping it personalized enough to actually get replies. You could charge $99/mo for access, or take a success fee on raised capital.

**Tech stack:** Use your own Wiggum loops (or OpenCode agents) to scrape, filter, draft, and send via Gmail API. Add a simple dashboard to review targets and override before sending.

**Differentiator:** Not just a contact list — it's an autonomous outreach campaign manager that learns what works for your vertical.

## Phase 1: Setup & Planning
- [x] Review requirements and design architecture
- [x] Set up development environment and dependencies
- [x] Create project structure

## Phase 2: Core Implementation  
- [ ] Implement main features
- [ ] Integrate APIs and libraries
- [ ] Build core logic

## Phase 3: Testing
- [ ] Write and run tests
- [ ] Integration testing
- [ ] Bug fixes

## Phase 4: Documentation & Deployment
- [ ] Write documentation
- [ ] Prepare deployment
- [ ] Deploy and validate

**Created:** Sat Mar 21 12:11:43 AM EDT 2026
**Mission:** *AI-Pitched** — an autonomous agent that monitors startup funding announcements (Crunchbase, AngelList, press releases), identifies relevant VCs/angels for your specific niche, and auto-drafts personalized cold emails using recent investments, shared connections, and portfolio alignment. The agent also tracks response rates, learns which templates and targets convert, and iteratively improves.

**Why now:** AI agents are hot, but founders still waste hours on manual outreach. This automates the funnel from target discovery to first contact, while keeping it personalized enough to actually get replies. You could charge $99/mo for access, or take a success fee on raised capital.

**Tech stack:** Use your own Wiggum loops (or OpenCode agents) to scrape, filter, draft, and send via Gmail API. Add a simple dashboard to review targets and override before sending.

**Differentiator:** Not just a contact list — it's an autonomous outreach campaign manager that learns what works for your vertical.
```

## NEXT TASK TO COMPLETE:
Implement main features

**Instructions:** Complete this task. Mark [x] in TASKS.md when done. Create, modify, or delete files as needed. Execute commands as needed. Also update README.md to match this project (name, setup instructions, current progress). No permission needed—just act.
```

## OpenCode Output

```
[0m
> build · stepfun/step-3.5-flash:free
[0m
I'll continue implementing the main features for pitcherai. Let me first check the current state and understand what we've built so far.
[0m→ [0mRead pyproject.toml
[0m→ [0mRead .agent_role
[0m→ [0mRead TASKS.md
[0m→ [0mRead README.md
Now let me check what's already been implemented in the source files:
[0m→ [0mRead src/pitcherai/main.py
[0m→ [0mRead src/pitcherai/models.py
[0m→ [0mRead src/pitcherai/schemas.py
[0m→ [0mRead src/pitcherai/crud.py
[0m→ [0mRead src/pitcherai/services/email_generation.py
[0m→ [0mRead src/pitcherai/services/campaign.py
[0m✱ [0mGlob "src/pitcherai/**/*.py"[90m 13 matches[0m
Let me check the remaining important files:
[0m→ [0mRead src/pitcherai/database.py
[0m→ [0mRead src/pitcherai/config.py
[0m→ [0mRead src/pitcherai/services/gmail.py
[0m→ [0mRead src/pitcherai/services/prospecting.py
[0m→ [0mRead src/pitcherai/dashboard/app.py
[0m→ [0mRead src/pitcherai/tasks/__init__.py
[0m→ [0mRead src/pitcherai/__init__.py
[0m✱ [0mGlob "tests/**/*.py"[90m 0 matches[0m
[0m
[0m$ [0mls -la /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/
total 676
drwxr-xr-x 12 julien julien   4096 Mar 21 12:42 .
drwxr-xr-x 30 julien julien   4096 Mar 21 00:10 ..
-rw-r--r--  1 julien julien      8 Mar 21 12:36 .agent_role
-rw-r--r--  1 julien julien  10447 Mar 21 12:16 ARCHITECTURE.md
-rw-r--r--  1 julien julien  53248 Mar 21 12:23 .coverage
drwxr-xr-x  2 julien julien   4096 Mar 21 10:49 data
-rw-r--r--  1 julien julien    768 Mar 21 12:40 .env.example
drwxr-xr-x  7 julien julien   4096 Mar 21 12:42 .git
drwxr-xr-x  3 julien julien   4096 Mar 21 00:10 .github
-rw-r--r--  1 julien julien      4 Mar 21 10:38 .gitignore
drwxr-xr-x  2 julien julien   4096 Mar 21 12:23 htmlcov
drwxr-xr-x  2 julien julien   4096 Mar 21 12:42 logs
-rw-r--r--  1 julien julien   9218 Mar 21 00:10 prompt.txt
-rw-r--r--  1 julien julien   2002 Mar 21 12:16 pyproject.toml
drwxr-xr-x  3 julien julien   4096 Mar 21 00:17 .pytest_cache
-rw-r--r--  1 julien julien   6396 Mar 21 12:19 README.md
drwxr-xr-x  4 julien julien   4096 Mar 21 01:07 .ruff_cache
drwxr-xr-x  3 julien julien   4096 Mar 21 12:16 src
-rw-r--r--  1 julien julien   2595 Mar 21 12:25 TASKS.md
-rw-r--r--  1 julien julien   2595 Mar 21 12:36 TASKS_original.md
-rw-r--r--  1 julien julien     95 Mar 21 12:42 tasks.py
drwxr-xr-x  4 julien julien   4096 Mar 21 12:14 tests
-rw-r--r--  1 julien julien 521433 Mar 21 12:22 uv.lock
drwxr-xr-x  7 julien julien   4096 Mar 21 12:23 .venv
-rw-r--r--  1 julien julien      6 Mar 21 12:36 .worker_persistent_mode
[0m
Let me also check if there are any existing tests and look for what needs to be done:
[0m→ [0mRead .env.example
[0m→ [0mRead ARCHITECTURE.md
[0m
[0m$ [0mls -la /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/tests/
total 16
drwxr-xr-x  4 julien julien 4096 Mar 21 12:14 .
drwxr-xr-x 12 julien julien 4096 Mar 21 12:42 ..
drwxr-xr-x  2 julien julien 4096 Mar 21 10:49 integration
drwxr-xr-x  2 julien julien 4096 Mar 21 10:49 unit
[0m
[0m$ [0mls -la /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/tests/unit/ /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/tests/integration/
/home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/tests/integration/:
total 8
drwxr-xr-x 2 julien julien 4096 Mar 21 10:49 .
drwxr-xr-x 4 julien julien 4096 Mar 21 12:14 ..

/home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/tests/unit/:
total 8
drwxr-xr-x 2 julien julien 4096 Mar 21 10:49 .
drwxr-xr-x 4 julien julien 4096 Mar 21 12:14 ..
[0m
Let me check what's in that tasks.py file at the root and examine any potential issues:
[0m→ [0mRead tasks.py
[0m
[0m$ [0mpython3 -c "import sys; sys.path.insert(0, 'src'); from pitcherai import main; print('Import successful')" 2>&1
Traceback (most recent call last):
  File "<string>", line 1, in <module>
    import sys; sys.path.insert(0, 'src'); from pitcherai import main; print('Import successful')
                                           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/src/pitcherai/main.py", line 12, in <module>
    from . import crud
  File "/home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/src/pitcherai/crud.py", line 9, in <module>
    from .models import (
    ...<9 lines>...
    )
  File "/home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/src/pitcherai/models.py", line 104, in <module>
    class SharedConnection(Base, TimestampMixin):
    ...<16 lines>...
        )
  File "/home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/src/pitcherai/models.py", line 119, in SharedConnection
    investor: Mapped["Investor"] = relationship(
                                   ~~~~~~~~~~~~^
        "Investor", back_populates="shared_connections"
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
TypeError: 'MappedColumn' object is not callable
[0m
There's a critical error in models.py. Let me examine it more carefully:
[0m→ [0mRead src/pitcherai/models.py[90m [limit=30, offset=100][0m
[0m
[0m# [0mTodos
[ ] Fix models.py - rename 'relationship' field to avoid shadowing
[ ] Add missing CLI entry point (cli.py)
[ ] Fix SQLAlchemy 2.0 async query syntax in campaign.py (replace query() with select())
[ ] Add prospecting API endpoints to main.py
[ ] Write unit tests for core components
[ ] Write integration tests
[ ] Fix any import/runtime issues
[ ] Run linting and type checking
[ ] Update TASKS.md to mark task complete
[0m
I found the bug! In models.py, line 116 defines a column named `relationship` which shadows the `relationship` function from SQLAlchemy. This breaks the relationship definition on line 119.

Let me create a todo list to track the work needed:
Now let me fix the critical bug first. I'll rename the `relationship` field to `relationship_type` to avoid shadowing:
[0m← [0mEdit src/pitcherai/models.py
Index: /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/src/pitcherai/models.py
===================================================================
--- /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/src/pitcherai/models.py
+++ /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/src/pitcherai/models.py
@@ -112,9 +112,9 @@
     ForeignKey("investors.id"), nullable=False
 )
 connection_name: Mapped[str] = mapped_column(String(255), nullable=False)
 connection_email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
-relationship: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
+relationship_type: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
 
 # Relationships
 investor: Mapped["Investor"] = relationship(
     "Investor", back_populates="shared_connections"

[0m
[0m$ [0mpython3 -c "import sys; sys.path.insert(0, 'src'); from pitcherai import main; print('Import successful')" 2>&1
Traceback (most recent call last):
  File "<string>", line 1, in <module>
    import sys; sys.path.insert(0, 'src'); from pitcherai import main; print('Import successful')
                                           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/src/pitcherai/main.py", line 14, in <module>
    from .services.email_generation import email_generator
  File "/home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/src/pitcherai/services/email_generation.py", line 6, in <module>
    from .config import settings
ModuleNotFoundError: No module named 'pitcherai.services.config'
[0m
There are import errors. The services modules are trying to import config incorrectly. They're in the `services` subdirectory so they need `from ..config import settings` not `from .config import settings`.

Let me fix the import in email_generation.py:
[0m← [0mEdit src/pitcherai/services/email_generation.py
Index: /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/src/pitcherai/services/email_generation.py
===================================================================
--- /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/src/pitcherai/services/email_generation.py
+++ /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/src/pitcherai/services/email_generation.py
@@ -2,9 +2,9 @@
 
 import os
 from typing import Optional, Dict, Any
 from openai import AsyncOpenAI
-from .config import settings
+from ..config import settings
 
 
 class EmailGenerationService:
     """Service for generating personalized emails using AI."""

[0m
Let me check the other service files for similar import issues and fix them all at once:
[0m✱ [0mGrep "from \.config import"[90m in src/pitcherai/services · 0 matches[0m
[0m
[0m$ [0mgrep -n "from .config import settings" src/pitcherai/services/*.py src/pitcherai/tasks/__init__.py 2>&1
Let me read the current state of email_generation.py:
[0m→ [0mRead src/pitcherai/services/email_generation.py[90m [limit=20][0m
[0m
[0m$ [0mpython3 -c "import sys; sys.path.insert(0, 'src'); from pitcherai import main; print('Import successful')" 2>&1
Traceback (most recent call last):
  File "<string>", line 1, in <module>
    import sys; sys.path.insert(0, 'src'); from pitcherai import main; print('Import successful')
                                           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/src/pitcherai/main.py", line 14, in <module>
    from .services.email_generation import email_generator
  File "/home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/src/pitcherai/services/email_generation.py", line 190, in <module>
    email_generator = EmailGenerationService()
  File "/home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/src/pitcherai/services/email_generation.py", line 13, in __init__
    self.client = AsyncOpenAI(api_key=settings.openai_api_key)
                  ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/julien/Desktop/Free-Wiggum-opencode/venv/lib/python3.14/site-packages/openai/_client.py", line 514, in __init__
    raise OpenAIError(
        "The api_key client option must be set either by passing api_key to the client or by setting the OPENAI_API_KEY environment variable"
    )
openai.OpenAIError: The api_key client option must be set either by passing api_key to the client or by setting the OPENAI_API_KEY environment variable
[0m
The OpenAI client is being instantiated at module import time. I need to make it lazy so the module can be imported without an API key. Let me refactor the email_generation.py:
[0m← [0mEdit src/pitcherai/services/email_generation.py
Index: /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/src/pitcherai/services/email_generation.py
===================================================================
--- /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/src/pitcherai/services/email_generation.py
+++ /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/src/pitcherai/services/email_generation.py
@@ -9,11 +9,18 @@
 class EmailGenerationService:
     """Service for generating personalized emails using AI."""
 
     def __init__(self):
-        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
+        self._client = None
         self.model = settings.openai_model
 
+    @property
+    def client(self):
+        """Lazy initialization of OpenAI client."""
+        if self._client is None and settings.openai_api_key:
+            self._client = AsyncOpenAI(api_key=settings.openai_api_key)
+        return self._client
+
     async def generate_email(
         self,
         investor_name: str,
         investor_firm: Optional[str],

[0m
```

## TASKS.md After Iteration

```markdown
# pitcherai

**Mission:** *AI-Pitched** — an autonomous agent that monitors startup funding announcements (Crunchbase, AngelList, press releases), identifies relevant VCs/angels for your specific niche, and auto-drafts personalized cold emails using recent investments, shared connections, and portfolio alignment. The agent also tracks response rates, learns which templates and targets convert, and iteratively improves.

**Why now:** AI agents are hot, but founders still waste hours on manual outreach. This automates the funnel from target discovery to first contact, while keeping it personalized enough to actually get replies. You could charge $99/mo for access, or take a success fee on raised capital.

**Tech stack:** Use your own Wiggum loops (or OpenCode agents) to scrape, filter, draft, and send via Gmail API. Add a simple dashboard to review targets and override before sending.

**Differentiator:** Not just a contact list — it's an autonomous outreach campaign manager that learns what works for your vertical.

## Phase 1: Setup & Planning
- [x] Review requirements and design architecture
- [x] Set up development environment and dependencies
- [x] Create project structure

## Phase 2: Core Implementation  
- [ ] Implement main features
- [ ] Integrate APIs and libraries
- [ ] Build core logic

## Phase 3: Testing
- [ ] Write and run tests
- [ ] Integration testing
- [ ] Bug fixes

## Phase 4: Documentation & Deployment
- [ ] Write documentation
- [ ] Prepare deployment
- [ ] Deploy and validate

**Created:** Sat Mar 21 12:11:43 AM EDT 2026
**Mission:** *AI-Pitched** — an autonomous agent that monitors startup funding announcements (Crunchbase, AngelList, press releases), identifies relevant VCs/angels for your specific niche, and auto-drafts personalized cold emails using recent investments, shared connections, and portfolio alignment. The agent also tracks response rates, learns which templates and targets convert, and iteratively improves.

**Why now:** AI agents are hot, but founders still waste hours on manual outreach. This automates the funnel from target discovery to first contact, while keeping it personalized enough to actually get replies. You could charge $99/mo for access, or take a success fee on raised capital.

**Tech stack:** Use your own Wiggum loops (or OpenCode agents) to scrape, filter, draft, and send via Gmail API. Add a simple dashboard to review targets and override before sending.

**Differentiator:** Not just a contact list — it's an autonomous outreach campaign manager that learns what works for your vertical.
```

**Completed at:** Sat Mar 21 12:46:10 PM EDT 2026
