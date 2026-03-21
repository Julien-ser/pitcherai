# Iteration 6 - pitcherai

**Timestamp:** Sat Mar 21 12:27:29 PM EDT 2026
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
- Iteration: 6 / 64k Token Budget
- Attempt: 3 (previous attempts may have partial progress)
- **Mandate:** Operate efficiently. Use partial edits, not full file rewrites when possible.
- **Output:** Be concise and action-oriented.
### Previous Attempt (Iteration 5):
**Files created/modified:**
```
**Created:** Sat Mar 21 12:11:43 AM EDT 2026
**Created:** Sat Mar 21 12:11:43 AM EDT 2026
**Created:** Sat Mar 21 12:11:43 AM EDT 2026
**Created:** Sat Mar 21 12:11:43 AM EDT 2026
```

**Last Output:**
```
## OpenCode Output

```
[0m
> build · stepfun/step-3.5-flash:free
[0m
[0m✗ [0mread failed
[91m[1mError: [0mFile not found: /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/.agent_role
[0m→ [0mRead TASKS.md
Since there's no `.agent_role` file, I'm operating as the generic developer. I need to complete "Implement main features" task. Let me first understand the current project structure.
[0m
[0m$ [0mfind /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai -type f -name "*.py" -o -name "*.js" -o -name "*.ts" -o -name "*.json" -o -name "*.toml" 2>/dev/null | head -20
/home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/.venv/share/jupyter/nbextensions/pydeck/index.js
/home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/.venv/share/jupyter/nbextensions/pydeck/extensionRequires.js
/home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/.venv/lib/python3.12/site-packages/cffi/setuptools_ext.py
/home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/.venv/lib/python3.12/site-packages/cffi/pkgconfig.py
/home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/.venv/lib/python3.12/site-packages/cffi/__init__.py
/home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/.venv/lib/python3.12/site-packages/cffi/cffi_opcode.py
/home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/.venv/lib/python3.12/site-packages/cffi/commontypes.py
/home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/.venv/lib/python3.12/site-packages/cffi/vengine_cpy.py
/home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/.venv/lib/python3.12/site-packages/cffi/model.py
--
## OpenCode Output

```
[0m
> build · stepfun/step-3.5-flash:free
[0m
I'll start by reading the current TASKS.md and exploring the project structure to understand what needs to be implemented.
[0m→ [0mRead TASKS.md
```

**Guidance:** Continue from where we left off. Don't re-do work already done. Focus on the next incomplete piece.


## CURRENT PROJECT STATE (Iteration 6)

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
I'll continue from the previous iteration. As the generic developer, I need to implement the main features for the pitcherai project. Let me first explore the project structure to understand what exists.
[0m→ [0mRead TASKS.md
[0m✱ [0mGlob "**/*.json"[90m 1 match[0m
[0m✱ [0mGlob "**/*.py"[90m 7 matches[0m
[0m
[0m$ [0mls -la /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai
total 660
drwxr-xr-x 12 julien julien   4096 Mar 21 12:23 .
drwxr-xr-x 30 julien julien   4096 Mar 21 00:10 ..
-rw-r--r--  1 julien julien  10447 Mar 21 12:16 ARCHITECTURE.md
-rw-r--r--  1 julien julien  53248 Mar 21 12:23 .coverage
drwxr-xr-x  2 julien julien   4096 Mar 21 10:49 data
-rw-r--r--  1 julien julien    737 Mar 21 12:19 .env.example
drwxr-xr-x  7 julien julien   4096 Mar 21 12:27 .git
drwxr-xr-x  3 julien julien   4096 Mar 21 00:10 .github
-rw-r--r--  1 julien julien      4 Mar 21 10:38 .gitignore
drwxr-xr-x  2 julien julien   4096 Mar 21 12:23 htmlcov
drwxr-xr-x  2 julien julien   4096 Mar 21 12:27 logs
-rw-r--r--  1 julien julien   9218 Mar 21 00:10 prompt.txt
-rw-r--r--  1 julien julien   2002 Mar 21 12:16 pyproject.toml
drwxr-xr-x  3 julien julien   4096 Mar 21 00:17 .pytest_cache
-rw-r--r--  1 julien julien   6396 Mar 21 12:19 README.md
drwxr-xr-x  4 julien julien   4096 Mar 21 01:07 .ruff_cache
drwxr-xr-x  3 julien julien   4096 Mar 21 12:16 src
-rw-r--r--  1 julien julien   2595 Mar 21 12:25 TASKS.md
drwxr-xr-x  4 julien julien   4096 Mar 21 12:14 tests
-rw-r--r--  1 julien julien 521433 Mar 21 12:22 uv.lock
drwxr-xr-x  7 julien julien   4096 Mar 21 12:23 .venv
[0m
Now let me examine the existing code structure and architecture to understand what needs to be implemented:
[0m→ [0mRead ARCHITECTURE.md
[0m→ [0mRead src/pitcherai/models.py
[0m→ [0mRead src/pitcherai/main.py
[0m→ [0mRead pyproject.toml
[0m→ [0mRead src/pitcherai/schemas.py
[0m→ [0mRead src/pitcherai/crud.py
[0m→ [0mRead src/pitcherai/config.py
[0m→ [0mRead src/pitcherai/database.py
[0m✱ [0mGlob "tests/*.py"[90m 0 matches[0m
Let me check the tests directory to understand expected behavior:
[0m
[0m$ [0mls -la /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/tests
total 16
drwxr-xr-x  4 julien julien 4096 Mar 21 12:14 .
drwxr-xr-x 12 julien julien 4096 Mar 21 12:23 ..
drwxr-xr-x  2 julien julien 4096 Mar 21 10:49 integration
drwxr-xr-x  2 julien julien 4096 Mar 21 10:49 unit
[0m
[0m$ [0mfind /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/tests -type f -name "*.py" 2>/dev/null
[0m
[0m# [0mTodos
[ ] Implement CRUD operations for all models (User, Investor, Template, Campaign, CampaignTarget, EmailTracking, Analytics)
[ ] Implement API endpoints for User management (create, get, update)
[ ] Implement API endpoints for Investor management (list with filters, create, get, investments)
[ ] Implement API endpoints for Template management (list, create, update)
[ ] Implement API endpoints for Campaign management (create, list, get, update, delete, start, pause)
[ ] Implement API endpoints for Campaign Targets (add to campaign, update target, manual send)
[ ] Implement email generation service using OpenAI API
[ ] Implement email generation endpoint (/api/generate-email)
[ ] Implement Gmail API integration for sending emails
[ ] Create Streamlit dashboard for review and management
[ ] Write unit tests for CRUD operations
[ ] Write integration tests for API endpoints
[ ] Update README.md with setup and usage instructions
[ ] Run tests and ensure all pass
[ ] Mark TASKS.md task as complete
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

**Completed at:** Sat Mar 21 12:29:02 PM EDT 2026
