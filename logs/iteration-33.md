# Iteration 33 - pitcherai

**Timestamp:** Fri Mar 27 01:20:08 PM EDT 2026
**Task:** Deploy and validate

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
- Iteration: 33 / 64k Token Budget
- Attempt: 1 (previous attempts may have partial progress)
- **Mandate:** Operate efficiently. Use partial edits, not full file rewrites when possible.
- **Output:** Be concise and action-oriented.


## CURRENT PROJECT STATE (Iteration 33)

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
- [x] Prepare deployment ✅
- [ ] Deploy and validate

**Created:** Sat Mar 21 12:11:43 AM EDT 2026
**Mission:** *AI-Pitched** — an autonomous agent that monitors startup funding announcements (Crunchbase, AngelList, press releases), identifies relevant VCs/angels for your specific niche, and auto-drafts personalized cold emails using recent investments, shared connections, and portfolio alignment. The agent also tracks response rates, learns which templates and targets convert, and iteratively improves.

**Why now:** AI agents are hot, but founders still waste hours on manual outreach. This automates the funnel from target discovery to first contact, while keeping it personalized enough to actually get replies. You could charge $99/mo for access, or take a success fee on raised capital.

**Tech stack:** Use your own Wiggum loops (or OpenCode agents) to scrape, filter, draft, and send via Gmail API. Add a simple dashboard to review targets and override before sending.

**Differentiator:** Not just a contact list — it's an autonomous outreach campaign manager that learns what works for your vertical.
```

## NEXT TASK TO COMPLETE:
Deploy and validate

**Instructions:** Complete this task. Mark [x] in TASKS.md when done. Create, modify, or delete files as needed. Execute commands as needed. Also update README.md to match this project (name, setup instructions, current progress). No permission needed—just act.
```

## OpenCode Output

```
[0m
> build · stepfun/step-3.5-flash:free
[0m
I'll help you deploy and validate the PitcherAI project. Let me first explore the project structure to understand what we're deploying.
[0m→ [0mRead .
[0m→ [0mRead README.md
[0m✱ [0mGlob "**/*.py"[90m 24 matches[0m
[0m✱ [0mGlob "**/*.json"[90m 1 match[0m
[0m✱ [0mGlob "**/Dockerfile*"[90m 1 match[0m
[0m→ [0mRead Dockerfile
Let me check the deployment configuration files:
[0m→ [0mRead docker-compose.yml
[0m→ [0mRead .env.production
[0m→ [0mRead DEPLOYMENT.md
[0m→ [0mRead TASKS.md
Now let me check the TASKS.md file to see the current status and the specific "Deploy and validate" task:
Now let me deploy and validate the application. First, I'll check if Docker is available and prepare the environment:
[0m
[0m$ [0mwhich docker && docker --version
which: no docker in (/home/julien/Desktop/Free-Wiggum-opencode/venv/bin:/home/julien/.cargo/bin:/home/julien/.local/bin:/home/julien/.nvm/versions/node/v22.21.1/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/usr/bin/site_perl:/usr/bin/vendor_perl:/usr/bin/core_perl)
[0m
[0m$ [0mwhich docker-compose && docker-compose --version
which: no docker-compose in (/home/julien/Desktop/Free-Wiggum-opencode/venv/bin:/home/julien/.cargo/bin:/home/julien/.local/bin:/home/julien/.nvm/versions/node/v22.21.1/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/usr/bin/site_perl:/usr/bin/vendor_perl:/usr/bin/core_perl)
[0m
[0m$ [0mls -la /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/.env
-rw-r--r-- 1 julien julien 948 Mar 22 12:59 /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/.env
[0m
[0m$ [0mwhich psql && psql --version
which: no psql in (/home/julien/Desktop/Free-Wiggum-opencode/venv/bin:/home/julien/.cargo/bin:/home/julien/.local/bin:/home/julien/.nvm/versions/node/v22.21.1/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/usr/bin/site_perl:/usr/bin/vendor_perl:/usr/bin/core_perl)
[0m
[0m$ [0mwhich redis-cli && redis-cli --version
which: no redis-cli in (/home/julien/Desktop/Free-Wiggum-opencode/venv/bin:/home/julien/.cargo/bin:/home/julien/.local/bin:/home/julien/.nvm/versions/node/v22.21.1/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/usr/bin/site_perl:/usr/bin/vendor_perl:/usr/bin/core_perl)
[0m
Docker is not installed on this system. Since we need to deploy and validate, let me check what's available for manual deployment or validate that the application can run directly:
[0m$ [0msystemctl status postgresql 2>/dev/null || service postgresql status 2>/dev/null || echo "PostgreSQL service not running"
PostgreSQL service not running
[0m
[0m$ [0msystemctl status redis 2>/dev/null || service redis status 2>/dev/null || echo "Redis service not running"
Redis service not running
[0m
Let me check if we can run tests to validate the application code:
[0m$ [0mwhich uv
/home/julien/Desktop/Free-Wiggum-opencode/venv/bin/uv
[0m
[0m$ [0msource .venv/bin/activate && which python && python --version
/home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/.venv/bin/python
Python 3.12.13
[0m
[0m→ [0mRead tests/conftest.py
[0m→ [0mRead pyproject.toml
Good! We have a virtual environment set up. Now let me check the test configuration to see if tests can run without PostgreSQL/Redis:
Excellent! The tests use SQLite in-memory database, so they don't require PostgreSQL or Redis. Let me run the tests to validate code correctness:
[0m
[0m$ [0msource .venv/bin/activate && uv run pytest tests/ -v
============================= test session starts ==============================
platform linux -- Python 3.12.13, pytest-9.0.2, pluggy-1.6.0 -- /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/.venv/bin/python
cachedir: .pytest_cache
rootdir: /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai
configfile: pyproject.toml
plugins: anyio-4.12.1, asyncio-1.3.0, cov-7.0.0
asyncio: mode=Mode.AUTO, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collecting ... collected 52 items / 4 errors

==================================== ERRORS ====================================
____________ ERROR collecting tests/integration/test_integration.py ____________
ImportError while importing test module '/home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/tests/integration/test_integration.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
.venv/lib/python3.12/site-packages/_pytest/python.py:507: in importtestmodule
    mod = import_path(
.venv/lib/python3.12/site-packages/_pytest/pathlib.py:587: in import_path
    importlib.import_module(module_name)
../../../../.local/share/uv/python/cpython-3.12.13-linux-x86_64-gnu/lib/python3.12/importlib/__init__.py:90: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
<frozen importlib._bootstrap>:1387: in _gcd_import
    ???
<frozen importlib._bootstrap>:1360: in _find_and_load
    ???
<frozen importlib._bootstrap>:1331: in _find_and_load_unlocked
    ???
<frozen importlib._bootstrap>:935: in _load_unlocked
    ???
.venv/lib/python3.12/site-packages/_pytest/assertion/rewrite.py:197: in exec_module
    exec(co, module.__dict__)
tests/integration/test_integration.py:16: in <module>
    from pitcherai.services.prospecting import ProspectingService
src/pitcherai/services/prospecting.py:11: in <module>
    from ..config import settings
E   ImportError: cannot import name 'settings' from 'pitcherai.config' (/home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/src/pitcherai/config.py)
_________________ ERROR collecting tests/unit/test_campaign.py _________________
ImportError while importing test module '/home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/tests/unit/test_campaign.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
.venv/lib/python3.12/site-packages/_pytest/python.py:507: in importtestmodule
    mod = import_path(
.venv/lib/python3.12/site-packages/_pytest/pathlib.py:587: in import_path
    importlib.import_module(module_name)
../../../../.local/share/uv/python/cpython-3.12.13-linux-x86_64-gnu/lib/python3.12/importlib/__init__.py:90: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
<frozen importlib._bootstrap>:1387: in _gcd_import
    ???
<frozen importlib._bootstrap>:1360: in _find_and_load
    ???
<frozen importlib._bootstrap>:1331: in _find_and_load_unlocked
    ???
<frozen importlib._bootstrap>:935: in _load_unlocked
    ???
.venv/lib/python3.12/site-packages/_pytest/assertion/rewrite.py:197: in exec_module
    exec(co, module.__dict__)
tests/unit/test_campaign.py:11: in <module>
    from pitcherai.services.campaign import CampaignService
src/pitcherai/services/campaign.py:10: in <module>
    from .email_generation import email_generator
src/pitcherai/services/email_generation.py:6: in <module>
    from ..config import settings
E   ImportError: cannot import name 'settings' from 'pitcherai.config' (/home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/src/pitcherai/config.py)
_____________ ERROR collecting tests/unit/test_email_generation.py _____________
ImportError while importing test module '/home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/tests/unit/test_email_generation.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
.venv/lib/python3.12/site-packages/_pytest/python.py:507: in importtestmodule
    mod = import_path(
.venv/lib/python3.12/site-packages/_pytest/pathlib.py:587: in import_path
    importlib.import_module(module_name)
../../../../.local/share/uv/python/cpython-3.12.13-linux-x86_64-gnu/lib/python3.12/importlib/__init__.py:90: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
<frozen importlib._bootstrap>:1387: in _gcd_import
    ???
<frozen importlib._bootstrap>:1360: in _find_and_load
    ???
<frozen importlib._bootstrap>:1331: in _find_and_load_unlocked
    ???
<frozen importlib._bootstrap>:935: in _load_unlocked
    ???
.venv/lib/python3.12/site-packages/_pytest/assertion/rewrite.py:197: in exec_module
    exec(co, module.__dict__)
tests/unit/test_email_generation.py:7: in <module>
    from pitcherai.services.email_generation import EmailGenerationService
src/pitcherai/services/email_generation.py:6: in <module>
    from ..config import settings
E   ImportError: cannot import name 'settings' from 'pitcherai.config' (/home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/src/pitcherai/config.py)
_______________ ERROR collecting tests/unit/test_prospecting.py ________________
.venv/lib/python3.12/site-packages/_pytest/python.py:507: in importtestmodule
    mod = import_path(
.venv/lib/python3.12/site-packages/_pytest/pathlib.py:587: in import_path
    importlib.import_module(module_name)
../../../../.local/share/uv/python/cpython-3.12.13-linux-x86_64-gnu/lib/python3.12/importlib/__init__.py:90: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
<frozen importlib._bootstrap>:1387: in _gcd_import
    ???
<frozen importlib._bootstrap>:1360: in _find_and_load
    ???
<frozen importlib._bootstrap>:1331: in _find_and_load_unlocked
    ???
<frozen importlib._bootstrap>:935: in _load_unlocked
    ???
.venv/lib/python3.12/site-packages/_pytest/assertion/rewrite.py:188: in exec_module
    source_stat, co = _rewrite_test(fn, self.config)
                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.12/site-packages/_pytest/assertion/rewrite.py:357: in _rewrite_test
    tree = ast.parse(source, filename=strfn)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
../../../../.local/share/uv/python/cpython-3.12.13-linux-x86_64-gnu/lib/python3.12/ast.py:52: in parse
    return compile(source, filename, mode, flags,
E     File "/home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/tests/unit/test_prospecting.py", line 28
E       from pitcherai.config import get_get_settings()
E                                                    ^
E   SyntaxError: invalid syntax
=========================== short test summary info ============================
ERROR tests/integration/test_integration.py
ERROR tests/unit/test_campaign.py
ERROR tests/unit/test_email_generation.py
ERROR tests/unit/test_prospecting.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 3.41s ===============================
[0m
[0m→ [0mRead src/pitcherai/config.py
[0m→ [0mRead tests/unit/test_prospecting.py
There are import errors and syntax errors in the codebase. I need to fix these before validating deployment. Let me check the config.py file to understand the issue:
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

**Completed at:** Fri Mar 27 01:22:18 PM EDT 2026
