# Iteration 7 - pitcherai

**Timestamp:** Sat Mar 21 12:29:05 PM EDT 2026
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
- Iteration: 7 / 64k Token Budget
- Attempt: 4 (previous attempts may have partial progress)
- **Mandate:** Operate efficiently. Use partial edits, not full file rewrites when possible.
- **Output:** Be concise and action-oriented.
### Previous Attempt (Iteration 6):
**Files created/modified:**
```
**Created:** Sat Mar 21 12:11:43 AM EDT 2026
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


## CURRENT PROJECT STATE (Iteration 7)

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
I need to understand the current project structure and implement the main features for this AI-powered pitch automation agent. Let me start by exploring what already exists.
[0m✱ [0mGlob "**/*.json"[90m in . · 1 match[0m
[0m✱ [0mGlob "**/*.py"[90m in . · 7 matches[0m
[0m
[0m$ [0mls -la /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai
total 660
drwxr-xr-x 12 julien julien   4096 Mar 21 12:23 .
drwxr-xr-x 30 julien julien   4096 Mar 21 00:10 ..
-rw-r--r--  1 julien julien  10447 Mar 21 12:16 ARCHITECTURE.md
-rw-r--r--  1 julien julien  53248 Mar 21 12:23 .coverage
drwxr-xr-x  2 julien julien   4096 Mar 21 10:49 data
-rw-r--r--  1 julien julien    737 Mar 21 12:19 .env.example
drwxr-xr-x  7 julien julien   4096 Mar 21 12:29 .git
drwxr-xr-x  3 julien julien   4096 Mar 21 00:10 .github
-rw-r--r--  1 julien julien      4 Mar 21 10:38 .gitignore
drwxr-xr-x  2 julien julien   4096 Mar 21 12:23 htmlcov
drwxr-xr-x  2 julien julien   4096 Mar 21 12:29 logs
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
[0m→ [0mRead TASKS.md
[0m→ [0mRead README.md
[0m→ [0mRead pyproject.toml
Let me examine the existing code structure and TASKS.md to understand what's already been implemented:
Now let me check what's already implemented in the source files:
[0m→ [0mRead src/pitcherai/main.py
[0m→ [0mRead src/pitcherai/models.py
[0m→ [0mRead src/pitcherai/database.py
[0m→ [0mRead src/pitcherai/config.py
[0m→ [0mRead src/pitcherai/schemas.py
[0m→ [0mRead src/pitcherai/crud.py
Let me check what tests exist and the directory structure:
[0m
[0m$ [0mfind /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/tests -type f -name "*.py" | head -20
[0m
[0m$ [0mls -la /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/src/pitcherai/
total 68
drwxr-xr-x 7 julien julien 4096 Mar 21 12:18 .
drwxr-xr-x 3 julien julien 4096 Mar 21 12:16 ..
drwxr-xr-x 2 julien julien 4096 Mar 21 12:16 api
-rw-r--r-- 1 julien julien 2256 Mar 21 12:17 config.py
-rw-r--r-- 1 julien julien 2050 Mar 21 12:17 crud.py
drwxr-xr-x 2 julien julien 4096 Mar 21 12:16 dashboard
-rw-r--r-- 1 julien julien 1150 Mar 21 12:17 database.py
-rw-r--r-- 1 julien julien   82 Mar 21 12:17 __init__.py
-rw-r--r-- 1 julien julien 4480 Mar 21 12:18 main.py
-rw-r--r-- 1 julien julien 9447 Mar 21 12:18 models.py
-rw-r--r-- 1 julien julien 4017 Mar 21 12:17 schemas.py
drwxr-xr-x 2 julien julien 4096 Mar 21 12:16 services
drwxr-xr-x 2 julien julien 4096 Mar 21 12:16 tasks
drwxr-xr-x 2 julien julien 4096 Mar 21 12:16 utils
[0m
[0m$ [0mls -la /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/src/pitcherai/api/ && ls -la /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/src/pitcherai/services/ && ls -la /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/src/pitcherai/tasks/ && ls -la /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/src/pitcherai/dashboard/
total 8
drwxr-xr-x 2 julien julien 4096 Mar 21 12:16 .
drwxr-xr-x 7 julien julien 4096 Mar 21 12:18 ..
total 8
drwxr-xr-x 2 julien julien 4096 Mar 21 12:16 .
drwxr-xr-x 7 julien julien 4096 Mar 21 12:18 ..
total 8
drwxr-xr-x 2 julien julien 4096 Mar 21 12:16 .
drwxr-xr-x 7 julien julien 4096 Mar 21 12:18 ..
total 8
drwxr-xr-x 2 julien julien 4096 Mar 21 12:16 .
drwxr-xr-x 7 julien julien 4096 Mar 21 12:18 ..
[0m
[0m# [0mTodos
[ ] Implement CRUD operations for all models (User, Investor, Template, Campaign, CampaignTarget)
[ ] Create email generation service with OpenAI integration
[ ] Create investor matching/service layer
[ ] Create campaign management service
[ ] Implement all API endpoints in main.py
[ ] Set up Celery tasks for async email sending and data collection
[ ] Create Streamlit dashboard for email review
[ ] Write unit tests for CRUD and services
[ ] Test the application locally and verify all endpoints work
[ ] Update TASKS.md to mark Phase 2 tasks complete
[0m
Perfect! The directories are empty. Now I understand the task: implement the core features. Let me create a comprehensive plan and start building.

Based on the project structure, I need to:
1. Implement CRUD operations for each model
2. Create service layer (AI email generation, investor matching, campaign management)
3. Implement all API endpoints
4. Create Celery tasks for async operations
5. Build Streamlit dashboard
6. Write tests

Let me start by creating the necessary files and implementing the core functionality:
Now let me implement the CRUD operations for all models:
[0m← [0mEdit src/pitcherai/crud.py
Index: /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/src/pitcherai/crud.py
===================================================================
--- /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/src/pitcherai/crud.py
+++ /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/src/pitcherai/crud.py
@@ -1,11 +1,36 @@
-"""Basic CRUD operations."""
+"""CRUD operations for all models."""
 
-from sqlalchemy import select, update, delete
+from sqlalchemy import select, update, delete, and_
 from sqlalchemy.ext.asyncio import AsyncSession
 from typing import Generic, TypeVar, Type, Optional, List
 from uuid import UUID
+from datetime import datetime
 
+from .models import (
+    User,
+    Investor,
+    Investment,
+    SharedConnection,
+    Template,
+    Campaign,
+    CampaignTarget,
+    EmailTracking,
+    Analytics,
+)
+from .schemas import (
+    UserCreate,
+    UserUpdate,
+    InvestorCreate,
+    InvestorUpdate,
+    TemplateCreate,
+    TemplateUpdate,
+    CampaignCreate,
+    CampaignUpdate,
+    CampaignTargetCreate,
+    CampaignTargetUpdate,
+)
+
 ModelType = TypeVar("ModelType")
 CreateSchemaType = TypeVar("CreateSchemaType")
 UpdateSchemaType = TypeVar("UpdateSchemaType")
 
@@ -53,4 +78,170 @@
     async def delete(self, session: AsyncSession, *, id: UUID) -> bool:
         """Delete record by ID."""
         result = await session.execute(delete(self.model).where(self.model.id == id))
         return result.rowcount > 0
+
+
+# Specific CRUD classes
+class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
+    """CRUD operations for User model."""
+
+    async def get_by_email(self, session: AsyncSession, email: str) -> Optional[User]:
+        """Get user by email."""
+        result = await session.execute(select(User).where(User.email == email))
+        return result.scalar_one_or_none()
+
+
+class CRUDInvestor(CRUDBase[Investor, InvestorCreate, InvestorUpdate]):
+    """CRUD operations for Investor model."""
+
+    async def list_by_type(
+        self, session: AsyncSession, investor_type: str, skip: int = 0, limit: int = 100
+    ) -> List[Investor]:
+        """List investors by type (vc or angel)."""
+        result = await session.execute(
+            select(Investor)
+            .where(Investor.investor_type == investor_type)
+            .offset(skip)
+            .limit(limit)
+        )
+        return result.scalars().all()
+
+    async def search_by_focus(
+        self, session: AsyncSession, focus_area: str, skip: int = 0, limit: int = 100
+    ) -> List[Investor]:
+        """Search investors by focus area."""
+        result = await session.execute(
+            select(Investor)
+            .where(Investor.focus_areas.contains([focus_area]))
+            .offset(skip)
+            .limit(limit)
+        )
+        return result.scalars().all()
+
+
+class CRUDTemplate(CRUDBase[Template, TemplateCreate, TemplateUpdate]):
+    """CRUD operations for Template model."""
+
+    async def get_active(self, session: AsyncSession) -> List[Template]:
+        """Get all active templates."""
+        result = await session.execute(
+            select(Template).where(Template.is_active == True)
+        )
+        return result.scalars().all()
+
+
+class CRUDCampaign(CRUDBase[Campaign, CampaignCreate, CampaignUpdate]):
+    """CRUD operations for Campaign model."""
+
+    async def get_by_user(
+        self, session: AsyncSession, user_id: UUID, skip: int = 0, limit: int = 100
+    ) -> List[Campaign]:
+        """Get campaigns for a specific user."""
+        result = await session.execute(
+            select(Campaign)
+            .where(Campaign.user_id == user_id)
+            .offset(skip)
+            .limit(limit)
+        )
+        return result.scalars().all()
+
+    async def start_campaign(
+        self, session: AsyncSession, campaign_id: UUID
+    ) -> Optional[Campaign]:
+        """Mark campaign as active and set start time."""
+        from datetime import datetime
+
+        update_data = CampaignUpdate(status="active", started_at=datetime.utcnow())
+        return await self.update(
+            session, db_obj=await self.get(session, campaign_id), obj_in=update_data
+        )
+
+    async def complete_campaign(
+        self, session: AsyncSession, campaign_id: UUID
+    ) -> Optional[Campaign]:
+        """Mark campaign as completed and set completion time."""
+        from datetime import datetime
+
+        update_data = CampaignUpdate(status="completed", completed_at=datetime.utcnow())
+        return await self.update(
+            session, db_obj=await self.get(session, campaign_id), obj_in=update_data
+        )
+
+
+class CRUDCampaignTarget(
+    CRUDBase[CampaignTarget, CampaignTargetCreate, CampaignTargetUpdate]
+):
+    """CRUD operations for CampaignTarget model."""
+
+    async def get_by_campaign(
+        self, session: AsyncSession, campaign_id: UUID, skip: int = 0, limit: int = 100
+    ) -> List[CampaignTarget]:
+        """Get targets for a campaign."""
+        result = await session.execute(
+            select(CampaignTarget)
+            .where(CampaignTarget.campaign_id == campaign_id)
+            .offset(skip)
+            .limit(limit)
+        )
+        return result.scalars().all()
+
+    async def get_pending(
+        self, session: AsyncSession, campaign_id: UUID
+    ) -> List[CampaignTarget]:
+        """Get pending targets for a campaign."""
+        result = await session.execute(
+            select(CampaignTarget).where(
+                and_(
+                    CampaignTarget.campaign_id == campaign_id,
+                    CampaignTarget.status == "pending",
+                )
+            )
+        )
+        return result.scalars().all()
+
+    async def mark_sent(
+        self, session: AsyncSession, target_id: UUID
+    ) -> Optional[CampaignTarget]:
+        """Mark a target as sent."""
+        update_data = CampaignTargetUpdate(status="sent", sent_at=datetime.utcnow())
+        return await self.update(
+            session, db_obj=await self.get(session, target_id), obj_in=update_data
+        )
+
+
+class CRUDEmailTracking(CRUDBase[EmailTracking, None, None]):
+    """CRUD operations for EmailTracking model."""
+
+    async def get_by_target(
+        self, session: AsyncSession, target_id: UUID
+    ) -> Optional[EmailTracking]:
+        """Get tracking info for a campaign target."""
+        result = await session.execute(
+            select(EmailTracking).where(EmailTracking.campaign_target_id == target_id)
+        )
+        return result.scalar_one_or_none()
+
+
+class CRUDAnalytics(CRUDBase[Analytics, None, None]):
+    """CRUD operations for Analytics model."""
+
+    async def get_by_campaign_date(
+        self, session: AsyncSession, campaign_id: UUID, date: datetime
+    ) -> Optional[Analytics]:
+        """Get analytics for a campaign on a specific date."""
+        result = await session.execute(
+            select(Analytics).where(
+                and_(Analytics.campaign_id == campaign_id, Analytics.date == date)
+            )
+        )
+        return result.scalar_one_or_none()
+
+
+# Instances
+user = CRUDUser(User)
+investor = CRUDInvestor(Investor)
+template = CRUDTemplate(Template)
+campaign = CRUDCampaign(Campaign)
+campaign_target = CRUDCampaignTarget(CampaignTarget)
+email_tracking = CRUDEmailTracking(EmailTracking)
+analytics = CRUDAnalytics(Analytics)

[0m
Let me fix the imports and type issues:
[0m← [0mEdit src/pitcherai/crud.py
Index: /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/src/pitcherai/crud.py
===================================================================
--- /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/src/pitcherai/crud.py
+++ /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/src/pitcherai/crud.py
@@ -1,9 +1,9 @@
 """CRUD operations for all models."""
 
 from sqlalchemy import select, update, delete, and_
 from sqlalchemy.ext.asyncio import AsyncSession
-from typing import Generic, TypeVar, Type, Optional, List
+from typing import Optional, List
 from uuid import UUID
 from datetime import datetime
 
 from .models import (
@@ -29,13 +29,9 @@
     CampaignTargetCreate,
     CampaignTargetUpdate,
 )
 
-ModelType = TypeVar("ModelType")
-CreateSchemaType = TypeVar("CreateSchemaType")
-UpdateSchemaType = TypeVar("UpdateSchemaType")
 
-
 class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
     """Base CRUD operations for any model."""
 
     def __init__(self, model: Type[ModelType]):

[0m
I see the issue - there's no InvestorUpdate schema. Let me first add it to schemas.py:
[0m← [0mEdit src/pitcherai/schemas.py
Index: /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/src/pitcherai/schemas.py
===================================================================
--- /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/src/pitcherai/schemas.py
+++ /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/src/pitcherai/schemas.py
@@ -47,8 +47,19 @@
     source: str
     raw_data: Optional[dict] = None
 
 
+class InvestorUpdate(BaseModel):
+    name: Optional[str] = None
+    investor_type: Optional[Literal["vc", "angel"]] = None
+    firm_name: Optional[str] = None
+    email: Optional[EmailStr] = None
+    linkedin_url: Optional[str] = None
+    focus_areas: Optional[list] = None
+    stage_preferences: Optional[list] = None
+    location: Optional[str] = None
+
+
 class InvestorResponse(InvestorBase):
     model_config = ConfigDict(from_attributes=True)
 
     id: UUID

[0m
Now let me completely rewrite crud.py with proper imports and simpler structure (avoiding generic complexity):
[0m← [0mWrite src/pitcherai/crud.py
Wrote file successfully.

LSP errors detected in other files:
<diagnostics file="/home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/src/pitcherai/main.py">
ERROR [7:6] Stub file not found for "pitcherai.config"
ERROR [8:6] Stub file not found for "pitcherai.database"
ERROR [9:6] Stub file not found for "pitcherai.models"
ERROR [10:6] Stub file not found for "pitcherai.schemas"
ERROR [55:42] "datetime" is not defined
ERROR [55:42] Type of "datetime" is unknown
ERROR [55:42] Type of "utcnow" is unknown
ERROR [55:42] Type of "isoformat" is unknown
ERROR [55:12] Return type, "dict[str, str | Unknown]", is partially unknown
ERROR [53:11] Return type, "dict[str, str | Unknown]", is partially unknown
ERROR [4:39] Import "HTTPException" is not accessed
ERROR [9:30] Import "User" is not accessed
ERROR [9:36] Import "Investor" is not accessed
ERROR [9:46] Import "Campaign" is not accessed
ERROR [9:56] Import "Template" is not accessed
ERROR [17:5] Import "CampaignUpdate" is not accessed
</diagnostics>

LSP errors detected in other files:
<diagnostics file="/home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/src/pitcherai/database.py">
ERROR [5:6] Stub file not found for "pitcherai.config"
ERROR [32:19] Return type of async generator function must be compatible with "AsyncGenerator[AsyncSession, Any]"
  "AsyncGenerator[AsyncSession, Unknown, Unknown]" is not assignable to "AsyncSession"
ERROR [28:23] Return type of async generator function must be compatible with "AsyncGenerator[Any, Any]"
  "AsyncGenerator[Any, Any, Any]" is not assignable to "AsyncSession"
</diagnostics>

LSP errors detected in other files:
<diagnostics file="/home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/src/pitcherai/models.py">
ERROR [18:6] Stub file not found for "pitcherai.database"
ERROR [119:36] Object of type "MappedColumn[Any]" is not callable
  Attribute "__call__" is unknown
ERROR [119:5] Type of "investor" is unknown
</diagnostics>

LSP errors detected in other files:
<diagnostics file="/home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/src/pitcherai/schemas.py">
ERROR [114:31] Expected type arguments for generic class "dict"
ERROR [41:27] Expected type arguments for generic class "list"
ERROR [42:33] Expected type arguments for generic class "list"
ERROR [48:24] Expected type arguments for generic class "dict"
ERROR [57:27] Expected type arguments for generic class "list"
ERROR [58:33] Expected type arguments for generic class "list"
ERROR [103:31] Expected type arguments for generic class "dict"
ERROR [165:27] Expected type arguments for generic class "dict"
</diagnostics>

LSP errors detected in this file, please fix:
<diagnostics file="/home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/src/pitcherai/crud.py">
ERROR [67:23] Cannot access attribute "rowcount" for class "Result[Any]"
  Attribute "rowcount" is unknown
ERROR [67:16] Type of "rowcount" is unknown
ERROR [67:16] Return type is unknown
ERROR [73:16] Type "Sequence[User]" is not assignable to return type "List[User]"
  "Sequence[User]" is not assignable to "List[User]"
ERROR [105:23] Cannot access attribute "rowcount" for class "Result[Any]"
  Attribute "rowcount" is unknown
ERROR [105:16] Type of "rowcount" is unknown
ERROR [105:16] Return type is unknown
ERROR [111:16] Type "Sequence[Investor]" is not assignable to return type "List[Investor]"
  "Sequence[Investor]" is not assignable to "List[Investor]"
ERROR [122:16] Type "Sequence[Investor]" is not assignable to return type "List[Investor]"
  "Sequence[Investor]" is not assignable to "List[Investor]"
ERROR [133:16] Type "Sequence[Investor]" is not assignable to return type "List[Investor]"
  "Sequence[Investor]" is not assignable to "List[Investor]"
ERROR [165:23] Cannot access attribute "rowcount" for class "Result[Any]"
  Attribute "rowcount" is unknown
ERROR [165:16] Type of "rowcount" is unknown
ERROR [165:16] Return type is unknown
ERROR [171:16] Type "Sequence[Template]" is not assignable to return type "List[Template]"
  "Sequence[Template]" is not assignable to "List[Template]"
ERROR [177:16] Type "Sequence[Template]" is not assignable to return type "List[Template]"
  "Sequence[Template]" is not assignable to "List[Template]"
ERROR [209:23] Cannot access attribute "rowcount" for class "Result[Any]"
  Attribute "rowcount" is unknown
ERROR [209:16] Type of "rowcount" is unknown
ERROR [209:16] Return type is unknown
ERROR [215:16] Type "Sequence[Campaign]" is not assignable to return type "List[Campaign]"
  "Sequence[Campaign]" is not assignable to "List[Campaign]"
ERROR [226:16] Type "Sequence[Campaign]" is not assignable to return type "List[Campaign]"
  "Sequence[Campaign]" is not assignable to "List[Campaign]"
... and 18 more
</diagnostics>
[0m
[0m# [0mTodos
[ ] Implement CRUD operations for all models (User, Investor, Template, Campaign, CampaignTarget)
[ ] Create email generation service with OpenAI integration
[ ] Create investor matching/service layer
[ ] Create campaign management service
[ ] Implement all API endpoints in main.py
[ ] Set up Celery tasks for async email sending and data collection
[ ] Create Streamlit dashboard for email review
[ ] Write unit tests for CRUD and services
[ ] Test the application locally and verify all endpoints work
[ ] Update TASKS.md to mark Phase 2 tasks complete
[0m
Let me mark the first task as in progress and create the email generation service:
