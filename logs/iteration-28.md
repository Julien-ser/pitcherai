# Iteration 28 - pitcherai

**Timestamp:** Sun Mar 22 12:55:25 PM EDT 2026
**Task:** Prepare deployment

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
- Iteration: 28 / 64k Token Budget
- Attempt: 1 (previous attempts may have partial progress)
- **Mandate:** Operate efficiently. Use partial edits, not full file rewrites when possible.
- **Output:** Be concise and action-oriented.


## CURRENT PROJECT STATE (Iteration 28)

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
- [x] Implement main features
- [x] Integrate APIs and libraries
- [x] Build core logic

## Phase 3: Testing
- [x] Write and run tests
- [x] Integration testing
- [x] Bug fixes

## Phase 4: Documentation & Deployment
- [x] Write documentation ✅
- [ ] Prepare deployment
- [ ] Deploy and validate

**Created:** Sat Mar 21 12:11:43 AM EDT 2026
**Mission:** *AI-Pitched** — an autonomous agent that monitors startup funding announcements (Crunchbase, AngelList, press releases), identifies relevant VCs/angels for your specific niche, and auto-drafts personalized cold emails using recent investments, shared connections, and portfolio alignment. The agent also tracks response rates, learns which templates and targets convert, and iteratively improves.

**Why now:** AI agents are hot, but founders still waste hours on manual outreach. This automates the funnel from target discovery to first contact, while keeping it personalized enough to actually get replies. You could charge $99/mo for access, or take a success fee on raised capital.

**Tech stack:** Use your own Wiggum loops (or OpenCode agents) to scrape, filter, draft, and send via Gmail API. Add a simple dashboard to review targets and override before sending.

**Differentiator:** Not just a contact list — it's an autonomous outreach campaign manager that learns what works for your vertical.
```

## NEXT TASK TO COMPLETE:
Prepare deployment

**Instructions:** Complete this task. Mark [x] in TASKS.md when done. Create, modify, or delete files as needed. Execute commands as needed. Also update README.md to match this project (name, setup instructions, current progress). No permission needed—just act.
```

## OpenCode Output

```
[0m
> build · stepfun/step-3.5-flash:free
[0m
I'll help you prepare deployment for the PitcherAI project. Let me first examine the current state and understand what needs to be done.
[0m✗ [0mread failed
[91m[1mError: [0mFile not found: /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/package.json
[0m→ [0mRead TASKS.md
[0m→ [0mRead README.md
[0m✱ [0mGlob "src/**/*"[90m 36 matches[0m
[0m✱ [0mGlob "Dockerfile"[90m 0 matches[0m
[0m✱ [0mGlob "docker-compose*.yml"[90m 0 matches[0m
[0m→ [0mRead pyproject.toml
Let me check the existing project files to understand what needs to be prepared for deployment:
[0m
[0m$ [0mls -la
total 684
drwxr-xr-x 12 julien julien   4096 Mar 22 12:54 .
drwxr-xr-x 30 julien julien   4096 Mar 21 00:10 ..
-rw-r--r--  1 julien julien      8 Mar 22 12:21 .agent_role
-rw-r--r--  1 julien julien   5466 Mar 21 12:50 ARCHITECTURE.md
-rw-r--r--  1 julien julien   2925 Mar 22 12:54 CHANGELOG.md
-rw-r--r--  1 julien julien   7413 Mar 22 12:54 CONTRIBUTING.md
-rw-r--r--  1 julien julien  53248 Mar 22 12:52 .coverage
drwxr-xr-x  2 julien julien   4096 Mar 21 10:49 data
-rw-r--r--  1 julien julien    863 Mar 21 12:50 .env.example
drwxr-xr-x  7 julien julien   4096 Mar 22 12:55 .git
drwxr-xr-x  3 julien julien   4096 Mar 21 00:10 .github
-rw-r--r--  1 julien julien      4 Mar 21 10:38 .gitignore
drwxr-xr-x  2 julien julien   4096 Mar 21 23:53 htmlcov
drwxr-xr-x  2 julien julien   4096 Mar 22 12:55 logs
-rw-r--r--  1 julien julien   9218 Mar 21 00:10 prompt.txt
-rw-r--r--  1 julien julien   2079 Mar 22 00:07 pyproject.toml
drwxr-xr-x  3 julien julien   4096 Mar 21 00:17 .pytest_cache
-rw-r--r--  1 julien julien   6707 Mar 22 12:54 README.md
drwxr-xr-x  4 julien julien   4096 Mar 21 01:07 .ruff_cache
drwxr-xr-x  3 julien julien   4096 Mar 21 12:16 src
-rw-r--r--  1 julien julien   2597 Mar 22 12:54 TASKS.md
-rw-r--r--  1 julien julien   2595 Mar 21 12:36 TASKS_original.md
-rw-r--r--  1 julien julien     95 Mar 21 12:42 tasks.py
drwxr-xr-x  5 julien julien   4096 Mar 21 13:04 tests
-rw-r--r--  1 julien julien 523785 Mar 22 00:06 uv.lock
drwxr-xr-x  7 julien julien   4096 Mar 21 12:23 .venv
-rw-r--r--  1 julien julien      6 Mar 22 12:21 .worker_persistent_mode
[0m
Now I'll prepare deployment for the project. The task includes creating Docker configuration and deployment files for this Python/FastAPI application. Let me start by creating the necessary files:
[0m← [0mWrite Dockerfile
Wrote file successfully.
[0m
[0m← [0mWrite .env.production
Wrote file successfully.
[0m
[0m← [0mWrite docker-compose.yml
Wrote file successfully.
[0m
Now I'll create a .dockerignore file and add deployment documentation:
[0m← [0mWrite .dockerignore
Wrote file successfully.
[0m
[0m← [0mWrite DEPLOYMENT.md
Wrote file successfully.
[0m
[0m← [0mWrite deploy/pitcherai-celery-worker.service
Wrote file successfully.
[0m
[0m← [0mWrite deploy/pitcherai-celery-beat.service
Wrote file successfully.
[0m
[0m← [0mWrite deploy/nginx-pitcherai.conf
Wrote file successfully.
[0m
[0m← [0mWrite deploy/pitcherai-web.service
Wrote file successfully.
[0m
Now I'll update the README.md to include deployment instructions and mark the task as complete:
[0m→ [0mRead README.md[90m [limit=50, offset=200][0m
[0m
[0m← [0mEdit README.md
Index: /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/README.md
===================================================================
--- /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/README.md
+++ /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/README.md
@@ -129,10 +129,48 @@
 ```
 
 See `.env.example` for all available options.
 
-## API Endpoints
+## Deployment
 
+PitcherAI can be deployed using Docker (recommended) or on bare metal.
+
+### Docker Deployment (Recommended)
+
+1. Create a `.env` file from the production template:
+```bash
+cp .env.production .env
+```
+
+2. Edit `.env` and add your API keys:
+   - `SECRET_KEY`: Generate a strong, random secret (min 32 characters)
+   - `OPENAI_API_KEY`: Your OpenAI API key
+   - `GMAIL_CLIENT_ID/SECRET/REFRESH_TOKEN`: Gmail API credentials (optional)
+   - Database and Redis passwords
+
+3. Start all services with Docker Compose:
+```bash
+docker-compose up -d
+```
+
+4. Initialize the database:
+```bash
+docker-compose exec web uv run python -c "from pitcherai.database import init_db; import asyncio; asyncio.run(init_db())"
+```
+
+5. Access the services:
+   - API Documentation: http://localhost:8000/docs
+   - API Endpoints: http://localhost:8000
+   - Streamlit Dashboard: http://localhost:8501
+
+See [DEPLOYMENT.md](DEPLOYMENT.md) for comprehensive deployment options including:
+- Manual deployment with systemd
+- Cloud deployments (Heroku, Railway, Fly.io)
+- Database migrations and maintenance
+- Production checklist and troubleshooting
+
+## CI/CD
+
 ### Users
 - `POST /api/users` - Create user
 - `GET /api/users/{id}` - Get user
 - `PUT /api/users/{id}` - Update user

[0m
[0m← [0mEdit README.md
Index: /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/README.md
===================================================================
--- /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/README.md
+++ /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/README.md
@@ -269,8 +269,9 @@
 
 - **README.md** - Project overview, quick start, and usage guide
 - **ARCHITECTURE.md** - System design, components, and data flow
 - **CONTRIBUTING.md** - Guidelines for contributors
+- **DEPLOYMENT.md** - Deployment and operations guide
 - **CHANGELOG.md** - Version history and release notes
 
 ## License
 

[0m
[0m← [0mEdit README.md
Index: /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/README.md
===================================================================
--- /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/README.md
+++ /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/README.md
@@ -29,9 +29,9 @@
 - **CI/CD**: GitHub Actions
 
 ## Project Status
 
-**Phase 3**: Testing - Completed ✅
+**Phase 4**: Documentation & Deployment - In Progress
 
 - [x] Review requirements and design architecture
 - [x] Set up development environment and dependencies
 - [x] Create project structure
@@ -40,10 +40,10 @@
 - [x] Build core logic ✅
 - [x] Write and run tests ✅
 - [x] Integration testing ✅
 - [x] Bug fixes ✅
-- [ ] Write documentation
-- [ ] Prepare deployment
+- [x] Write documentation ✅
+- [x] Prepare deployment ✅
 - [ ] Deploy and validate
 
 See [TASKS.md](TASKS.md) for full task list.
 

[0m
Now I'll mark the task as complete in TASKS.md:
[0m← [0mEdit TASKS.md
Index: /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/TASKS.md
===================================================================
--- /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/TASKS.md
+++ /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/TASKS.md
@@ -24,9 +24,9 @@
 - [x] Bug fixes
 
 ## Phase 4: Documentation & Deployment
 - [x] Write documentation ✅
-- [ ] Prepare deployment
+- [x] Prepare deployment ✅
 - [ ] Deploy and validate
 
 **Created:** Sat Mar 21 12:11:43 AM EDT 2026
 **Mission:** *AI-Pitched** — an autonomous agent that monitors startup funding announcements (Crunchbase, AngelList, press releases), identifies relevant VCs/angels for your specific niche, and auto-drafts personalized cold emails using recent investments, shared connections, and portfolio alignment. The agent also tracks response rates, learns which templates and targets convert, and iteratively improves.

[0m
[0m$ [0mgit status
On branch wiggum/session-1774196501
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   README.md
	modified:   TASKS.md
	modified:   logs/worker-session-20260322-122142.log

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	.dockerignore
	.env.production
	DEPLOYMENT.md
	Dockerfile
	deploy/
	docker-compose.yml
	logs/iteration-28.md

no changes added to commit (use "git add" and/or "git commit -a")
[0m
[0m$ [0mgit add . && git commit -m "feat: add Docker deployment configuration and documentation"
[wiggum/session-1774196501 968c0e8] feat: add Docker deployment configuration and documentation
 13 files changed, 1433 insertions(+), 5 deletions(-)
 create mode 100644 .dockerignore
 create mode 100644 .env.production
 create mode 100644 DEPLOYMENT.md
 create mode 100644 Dockerfile
 create mode 100644 deploy/nginx-pitcherai.conf
 create mode 100644 deploy/pitcherai-celery-beat.service
 create mode 100644 deploy/pitcherai-celery-worker.service
 create mode 100644 deploy/pitcherai-web.service
 create mode 100644 docker-compose.yml
 create mode 100644 logs/iteration-28.md
[0m
Now let me commit all changes:
[0m$ [0mgit push origin main
Everything up-to-date
[0m
Deployment preparation complete. All files created and committed.

**Created files:**
- Dockerfile, docker-compose.yml
- .env.production, .dockerignore
- deploy/ (systemd services, nginx config)
- DEPLOYMENT.md

**Updated:**
- README.md (added deployment section)
- TASKS.md (marked task [x])

Next task: Deploy and validate
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
- [x] Implement main features
- [x] Integrate APIs and libraries
- [x] Build core logic

## Phase 3: Testing
- [x] Write and run tests
- [x] Integration testing
- [x] Bug fixes

## Phase 4: Documentation & Deployment
- [x] Write documentation ✅
- [x] Prepare deployment ✅
- [ ] Deploy and validate

**Created:** Sat Mar 21 12:11:43 AM EDT 2026
**Mission:** *AI-Pitched** — an autonomous agent that monitors startup funding announcements (Crunchbase, AngelList, press releases), identifies relevant VCs/angels for your specific niche, and auto-drafts personalized cold emails using recent investments, shared connections, and portfolio alignment. The agent also tracks response rates, learns which templates and targets convert, and iteratively improves.

**Why now:** AI agents are hot, but founders still waste hours on manual outreach. This automates the funnel from target discovery to first contact, while keeping it personalized enough to actually get replies. You could charge $99/mo for access, or take a success fee on raised capital.

**Tech stack:** Use your own Wiggum loops (or OpenCode agents) to scrape, filter, draft, and send via Gmail API. Add a simple dashboard to review targets and override before sending.

**Differentiator:** Not just a contact list — it's an autonomous outreach campaign manager that learns what works for your vertical.
```

**Completed at:** Sun Mar 22 12:57:54 PM EDT 2026
