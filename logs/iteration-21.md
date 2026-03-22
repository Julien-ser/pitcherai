# Iteration 21 - pitcherai

**Timestamp:** Sun Mar 22 12:29:34 AM EDT 2026
**Task:** Integration testing

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
- Iteration: 21 / 64k Token Budget
- Attempt: 5 (previous attempts may have partial progress)
- **Mandate:** Operate efficiently. Use partial edits, not full file rewrites when possible.
- **Output:** Be concise and action-oriented.
### Previous Attempt (Iteration 20):
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
I'll complete the integration testing task. Let me first explore the project structure to understand what needs to be tested.
[0m✱ [0mGlob "**/test*.py"[90m 7 matches[0m
[0m✱ [0mGlob "**/*.py"[90m 23 matches[0m
[0m✱ [0mGlob "**/*test.py"[90m 1 match[0m
[0m→ [0mRead TASKS.md
[0m→ [0mRead src/pitcherai/main.py
[0m→ [0mRead src/pitcherai/models.py
[0m→ [0mRead src/pitcherai/services/prospecting.py
[0m→ [0mRead src/pitcherai/services/email_generation.py
[0m→ [0mRead tests/conftest.py
[0m→ [0mRead tests/unit/test_campaign.py
```

## TASKS.md After Iteration
```
--
## OpenCode Output

```
[0m
> build · stepfun/step-3.5-flash:free
[0m
I'll continue with the integration testing task. Let me first explore the project structure to understand what needs to be tested and then create comprehensive integration tests.
[0m→ [0mRead README.md
```

**Guidance:** Continue from where we left off. Don't re-do work already done. Focus on the next incomplete piece.


## CURRENT PROJECT STATE (Iteration 21)

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
Integration testing

**Instructions:** Complete this task. Mark [x] in TASKS.md when done. Create, modify, or delete files as needed. Execute commands as needed. Also update README.md to match this project (name, setup instructions, current progress). No permission needed—just act.
```

## OpenCode Output

```
[0m
> build · stepfun/step-3.5-flash:free
[0m
I'll continue with the integration testing task. Let me first explore the project structure to understand what needs to be tested and create comprehensive integration tests.
[0m→ [0mRead README.md
[0m→ [0mRead TASKS.md
[0m→ [0mRead src/pitcherai/services/prospecting.py
[0m→ [0mRead src/pitcherai/models.py
[0m→ [0mRead src/pitcherai/main.py
[0m→ [0mRead src/pitcherai/services/campaign.py
[0m→ [0mRead src/pitcherai/services/email_generation.py
[0m→ [0mRead tests/unit/test_campaign.py
[0m→ [0mRead tests/conftest.py
[0m✱ [0mGlob "tests/**/*.py"[90m 9 matches[0m
[0m→ [0mRead tests/integration/test_integration.py
Now let me check what testing dependencies exist and run the integration tests to see their current status:
[0m→ [0mRead pyproject.toml
Let me check the current state and run the integration tests to verify they work properly:
[0m
[0m$ [0mpip install uv
Requirement already satisfied: uv in /home/julien/Desktop/Free-Wiggum-opencode/venv/lib/python3.14/site-packages (0.10.11)
[0m
[0m$ [0muv pip install -e .
Using Python 3.14.3 environment at: /home/julien/Desktop/Free-Wiggum-opencode/venv
Resolved 111 packages in 234ms
   Building pitcherai @ file:///home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai
      Built pitcherai @ file:///home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai
Prepared 1 package in 436ms
Uninstalled 1 package in 0.38ms
Installed 1 package in 1ms
 ~ pitcherai==0.1.0 (from file:///home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai)
[0m
[0m$ [0mpytest tests/integration/ -v --tb=short
============================= test session starts ==============================
platform linux -- Python 3.14.3, pytest-9.0.2, pluggy-1.6.0 -- /home/julien/Desktop/Free-Wiggum-opencode/venv/bin/python
cachedir: .pytest_cache
rootdir: /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai
configfile: pyproject.toml
plugins: langsmith-0.7.16, anyio-4.12.1, asyncio-1.3.0, cov-7.0.0, mock-3.15.1, dash-4.0.0
asyncio: mode=Mode.AUTO, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collecting ... collected 9 items

tests/integration/test_integration.py::TestFullCampaignLifecycle::test_complete_end_to_end_workflow FAILED [ 11%]
tests/integration/test_integration.py::TestInvestorImportAndEnrichment::test_prospecting_import_workflow FAILED [ 22%]
tests/integration/test_integration.py::TestInvestorImportAndEnrichment::test_enrich_investor_portfolio_workflow FAILED [ 33%]
tests/integration/test_integration.py::TestEmailGenerationIntegration::test_email_generation_with_investor_data FAILED [ 44%]
tests/integration/test_integration.py::TestServiceInteractions::test_campaign_target_approval_and_email_generation PASSED [ 55%]
tests/integration/test_integration.py::TestServiceInteractions::test_analytics_calculation_end_to_end PASSED [ 66%]
tests/integration/test_integration.py::TestAPIIntegration::test_full_api_workflow FAILED [ 77%]
tests/integration/test_integration.py::TestConcurrencyAndDataConsistency::test_concurrent_campaign_creation FAILED [ 88%]
tests/integration/test_integration.py::TestConcurrencyAndDataConsistency::test_data_consistency_across_services FAILED [100%]

=================================== FAILURES ===================================
_________ TestFullCampaignLifecycle.test_complete_end_to_end_workflow __________
tests/integration/test_integration.py:216: in test_complete_end_to_end_workflow
    assert target.investor.name in target.email_body
E   AssertionError: assert 'AI VC Partner' in 'Enhanced email body with personalization'
E    +  where 'AI VC Partner' = <pitcherai.models.Investor object at 0x7efcab182900>.name
E    +    where <pitcherai.models.Investor object at 0x7efcab182900> = <pitcherai.models.CampaignTarget object at 0x7efcaa77a060>.investor
E    +  and   'Enhanced email body with personalization' = <pitcherai.models.CampaignTarget object at 0x7efcaa77a060>.email_body
_______ TestInvestorImportAndEnrichment.test_prospecting_import_workflow _______
tests/integration/test_integration.py:336: in test_prospecting_import_workflow
    total = await prospecting.import_investors_from_sources(
src/pitcherai/services/prospecting.py:172: in import_investors_from_sources
    existing = await crud.investor.get_by_email(
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^
E   AttributeError: 'InvestorCRUD' object has no attribute 'get_by_email'
___ TestInvestorImportAndEnrichment.test_enrich_investor_portfolio_workflow ____
tests/integration/test_integration.py:404: in test_enrich_investor_portfolio_workflow
    if updated_investor and updated_investor.investments:
                            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
../../venv/lib/python3.14/site-packages/sqlalchemy/orm/attributes.py:569: in __get__
    return self.impl.get(state, dict_)  # type: ignore[no-any-return]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
../../venv/lib/python3.14/site-packages/sqlalchemy/orm/attributes.py:1096: in get
    value = self._fire_loader_callables(state, key, passive)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
../../venv/lib/python3.14/site-packages/sqlalchemy/orm/attributes.py:1131: in _fire_loader_callables
    return self.callable_(state, passive)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
../../venv/lib/python3.14/site-packages/sqlalchemy/orm/strategies.py:978: in _load_for_state
    return self._emit_lazyload(
../../venv/lib/python3.14/site-packages/sqlalchemy/orm/strategies.py:1141: in _emit_lazyload
    result = session.execute(
../../venv/lib/python3.14/site-packages/sqlalchemy/orm/session.py:2351: in execute
    return self._execute_internal(
../../venv/lib/python3.14/site-packages/sqlalchemy/orm/session.py:2249: in _execute_internal
    result: Result[Any] = compile_state_cls.orm_execute_statement(
../../venv/lib/python3.14/site-packages/sqlalchemy/orm/context.py:306: in orm_execute_statement
    result = conn.execute(
../../venv/lib/python3.14/site-packages/sqlalchemy/engine/base.py:1419: in execute
    return meth(
../../venv/lib/python3.14/site-packages/sqlalchemy/sql/elements.py:527: in _execute_on_connection
    return connection._execute_clauseelement(
../../venv/lib/python3.14/site-packages/sqlalchemy/engine/base.py:1641: in _execute_clauseelement
    ret = self._execute_context(
../../venv/lib/python3.14/site-packages/sqlalchemy/engine/base.py:1846: in _execute_context
    return self._exec_single_context(
../../venv/lib/python3.14/site-packages/sqlalchemy/engine/base.py:1986: in _exec_single_context
    self._handle_dbapi_exception(
../../venv/lib/python3.14/site-packages/sqlalchemy/engine/base.py:2366: in _handle_dbapi_exception
    raise exc_info[1].with_traceback(exc_info[2])
../../venv/lib/python3.14/site-packages/sqlalchemy/engine/base.py:1967: in _exec_single_context
    self.dialect.do_execute(
../../venv/lib/python3.14/site-packages/sqlalchemy/engine/default.py:952: in do_execute
    cursor.execute(statement, parameters)
../../venv/lib/python3.14/site-packages/sqlalchemy/dialects/sqlite/aiosqlite.py:182: in execute
    self._adapt_connection._handle_exception(error)
../../venv/lib/python3.14/site-packages/sqlalchemy/dialects/sqlite/aiosqlite.py:342: in _handle_exception
    raise error
../../venv/lib/python3.14/site-packages/sqlalchemy/dialects/sqlite/aiosqlite.py:159: in execute
    _cursor: AsyncIODBAPICursor = self.await_(self._connection.cursor())  # type: ignore[arg-type] # noqa: E501
                                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
../../venv/lib/python3.14/site-packages/sqlalchemy/util/_concurrency_py3k.py:123: in await_only
    raise exc.MissingGreenlet(
E   sqlalchemy.exc.MissingGreenlet: greenlet_spawn has not been called; can't call await_only() here. Was IO attempted in an unexpected place? (Background on this error at: https://sqlalche.me/e/20/xd2s)
___ TestEmailGenerationIntegration.test_email_generation_with_investor_data ____
tests/integration/test_integration.py:512: in test_email_generation_with_investor_data
    assert investor.name in body
E   AssertionError: assert 'John Doe' in 'Enhanced email body with personalization'
E    +  where 'John Doe' = <pitcherai.models.Investor object at 0x7efcaa399940>.name
__________________ TestAPIIntegration.test_full_api_workflow ___________________
tests/integration/test_integration.py:784: in test_full_api_workflow
    assert get_campaign_response.status_code == 200
E   assert 404 == 200
E    +  where 404 = <Response [404 Not Found]>.status_code
_____ TestConcurrencyAndDataConsistency.test_concurrent_campaign_creation ______
tests/integration/test_integration.py:851: in test_concurrent_campaign_creation
    campaigns = await asyncio.gather(*tasks)
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
tests/integration/test_integration.py:840: in create_campaign
    return await crud.campaign.create(
src/pitcherai/crud.py:193: in create
    await session.flush()
../../venv/lib/python3.14/site-packages/sqlalchemy/ext/asyncio/session.py:787: in flush
    await greenlet_spawn(self.sync_session.flush, objects=objects)
../../venv/lib/python3.14/site-packages/sqlalchemy/util/_concurrency_py3k.py:190: in greenlet_spawn
    result = context.switch(*args, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
../../venv/lib/python3.14/site-packages/sqlalchemy/orm/session.py:4325: in flush
    raise sa_exc.InvalidRequestError("Session is already flushing")
E   sqlalchemy.exc.InvalidRequestError: Session is already flushing
___ TestConcurrencyAndDataConsistency.test_data_consistency_across_services ____
tests/integration/test_integration.py:945: in test_data_consistency_across_services
    if fetched_investor.investments:
       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
../../venv/lib/python3.14/site-packages/sqlalchemy/orm/attributes.py:569: in __get__
    return self.impl.get(state, dict_)  # type: ignore[no-any-return]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
../../venv/lib/python3.14/site-packages/sqlalchemy/orm/attributes.py:1096: in get
    value = self._fire_loader_callables(state, key, passive)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
../../venv/lib/python3.14/site-packages/sqlalchemy/orm/attributes.py:1131: in _fire_loader_callables
    return self.callable_(state, passive)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
../../venv/lib/python3.14/site-packages/sqlalchemy/orm/strategies.py:978: in _load_for_state
    return self._emit_lazyload(
../../venv/lib/python3.14/site-packages/sqlalchemy/orm/strategies.py:1141: in _emit_lazyload
    result = session.execute(
../../venv/lib/python3.14/site-packages/sqlalchemy/orm/session.py:2351: in execute
    return self._execute_internal(
../../venv/lib/python3.14/site-packages/sqlalchemy/orm/session.py:2249: in _execute_internal
    result: Result[Any] = compile_state_cls.orm_execute_statement(
../../venv/lib/python3.14/site-packages/sqlalchemy/orm/context.py:306: in orm_execute_statement
    result = conn.execute(
../../venv/lib/python3.14/site-packages/sqlalchemy/engine/base.py:1419: in execute
    return meth(
../../venv/lib/python3.14/site-packages/sqlalchemy/sql/elements.py:527: in _execute_on_connection
    return connection._execute_clauseelement(
../../venv/lib/python3.14/site-packages/sqlalchemy/engine/base.py:1641: in _execute_clauseelement
    ret = self._execute_context(
../../venv/lib/python3.14/site-packages/sqlalchemy/engine/base.py:1846: in _execute_context
    return self._exec_single_context(
../../venv/lib/python3.14/site-packages/sqlalchemy/engine/base.py:1986: in _exec_single_context
    self._handle_dbapi_exception(
../../venv/lib/python3.14/site-packages/sqlalchemy/engine/base.py:2366: in _handle_dbapi_exception
    raise exc_info[1].with_traceback(exc_info[2])
../../venv/lib/python3.14/site-packages/sqlalchemy/engine/base.py:1967: in _exec_single_context
    self.dialect.do_execute(
../../venv/lib/python3.14/site-packages/sqlalchemy/engine/default.py:952: in do_execute
    cursor.execute(statement, parameters)
../../venv/lib/python3.14/site-packages/sqlalchemy/dialects/sqlite/aiosqlite.py:182: in execute
    self._adapt_connection._handle_exception(error)
../../venv/lib/python3.14/site-packages/sqlalchemy/dialects/sqlite/aiosqlite.py:342: in _handle_exception
    raise error
../../venv/lib/python3.14/site-packages/sqlalchemy/dialects/sqlite/aiosqlite.py:159: in execute
    _cursor: AsyncIODBAPICursor = self.await_(self._connection.cursor())  # type: ignore[arg-type] # noqa: E501
                                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
../../venv/lib/python3.14/site-packages/sqlalchemy/util/_concurrency_py3k.py:123: in await_only
    raise exc.MissingGreenlet(
E   sqlalchemy.exc.MissingGreenlet: greenlet_spawn has not been called; can't call await_only() here. Was IO attempted in an unexpected place? (Background on this error at: https://sqlalche.me/e/20/xd2s)
=============================== warnings summary ===============================
src/pitcherai/config.py:7
  /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/src/pitcherai/config.py:7: PydanticDeprecatedSince20: Support for class-based `config` is deprecated, use ConfigDict instead. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.12/migration/
    class Settings(BaseSettings):

tests/integration/test_integration.py::TestServiceInteractions::test_analytics_calculation_end_to_end
  /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/src/pitcherai/crud.py:318: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    update_data = CampaignTargetUpdate(status="sent", sent_at=datetime.utcnow())

tests/integration/test_integration.py::TestConcurrencyAndDataConsistency::test_concurrent_campaign_creation
  /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/src/pitcherai/crud.py:192: SAWarning: Usage of the 'Session.add()' operation is not currently supported within the execution stage of the flush process. Results may not be consistent.  Consider using alternative event listeners or connection-level operations instead.
    session.add(db_obj)

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
================================ tests coverage ================================
_______________ coverage: platform linux, python 3.14.3-final-0 ________________

Name                                         Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------
src/pitcherai/__init__.py                        1      0   100%
src/pitcherai/cli.py                            51     51     0%   3-96
src/pitcherai/config.py                         27      0   100%
src/pitcherai/crud.py                          233     73    69%   58-63, 66-67, 72-73, 96-101, 104-105, 110-111, 116-122, 127-133, 156-161, 164-165, 170-171, 174-177, 200-205, 208-209, 214-215, 220-226, 231-232, 239-240, 280-283, 288-289, 330-333, 355-361, 366-371, 380-381
src/pitcherai/database.py                       21      8    62%   30-38
src/pitcherai/main.py                          338    225    33%   67, 78, 85-94, 102-111, 123-127, 143-152, 160-169, 181-183, 203-212, 234-242, 252-253, 257, 267-276, 282-291, 297-307, 313-320, 330-378, 388-395, 407-410, 418-425, 436-453, 465-476, 486-495, 501-510, 520-547, 553-563, 569-579, 591-592, 606, 636-661
src/pitcherai/models.py                        112      0   100%
src/pitcherai/schemas.py                        86      0   100%
src/pitcherai/services/campaign.py              84     24    71%   103, 118, 123, 128, 137, 181-182, 191-199, 207-213, 221, 227-228
src/pitcherai/services/email_generation.py      52      6    88%   19-21, 190-193
src/pitcherai/services/prospecting.py          125     48    62%   22, 32-33, 55-57, 78-79, 93-115, 121-134, 163-168, 175-191, 208, 229-230, 268-271, 277-278, 290-295
src/pitcherai/tasks/__init__.py                 86     86     0%   3-203
--------------------------------------------------------------------------
TOTAL                                         1216    521    57%
Coverage HTML written to dir htmlcov
=========================== short test summary info ============================
FAILED tests/integration/test_integration.py::TestFullCampaignLifecycle::test_complete_end_to_end_workflow - AssertionError: assert 'AI VC Partner' in 'Enhanced email body with personalization'
 +  where 'AI VC Partner' = <pitcherai.models.Investor object at 0x7efcab182900>.name
 +    where <pitcherai.models.Investor object at 0x7efcab182900> = <pitcherai.models.CampaignTarget object at 0x7efcaa77a060>.investor
 +  and   'Enhanced email body with personalization' = <pitcherai.models.CampaignTarget object at 0x7efcaa77a060>.email_body
FAILED tests/integration/test_integration.py::TestInvestorImportAndEnrichment::test_prospecting_import_workflow - AttributeError: 'InvestorCRUD' object has no attribute 'get_by_email'
FAILED tests/integration/test_integration.py::TestInvestorImportAndEnrichment::test_enrich_investor_portfolio_workflow - sqlalchemy.exc.MissingGreenlet: greenlet_spawn has not been called; can't call await_only() here. Was IO attempted in an unexpected place? (Background on this error at: https://sqlalche.me/e/20/xd2s)
FAILED tests/integration/test_integration.py::TestEmailGenerationIntegration::test_email_generation_with_investor_data - AssertionError: assert 'John Doe' in 'Enhanced email body with personalization'
 +  where 'John Doe' = <pitcherai.models.Investor object at 0x7efcaa399940>.name
FAILED tests/integration/test_integration.py::TestAPIIntegration::test_full_api_workflow - assert 404 == 200
 +  where 404 = <Response [404 Not Found]>.status_code
FAILED tests/integration/test_integration.py::TestConcurrencyAndDataConsistency::test_concurrent_campaign_creation - sqlalchemy.exc.InvalidRequestError: Session is already flushing
FAILED tests/integration/test_integration.py::TestConcurrencyAndDataConsistency::test_data_consistency_across_services - sqlalchemy.exc.MissingGreenlet: greenlet_spawn has not been called; can't call await_only() here. Was IO attempted in an unexpected place? (Background on this error at: https://sqlalche.me/e/20/xd2s)
=================== 7 failed, 2 passed, 3 warnings in 3.09s ====================
[0m
Let me check the CRUD module to understand the missing `get_by_email` method:
[0m→ [0mRead src/pitcherai/crud.py
I can see several issues causing test failures:

1. `InvestorCRUD` is missing the `get_by_email` method that prospecting.py uses
2. Email generation mock returns generic text instead of personalized content
3. Lazy loading relationship access after session commit causes greenlet errors
4. Concurrent session flushing issues

Let me fix these issues step by step:

**1. Add missing `get_by_email` method to InvestorCRUD:**
[0m
[0m← [0mEdit src/pitcherai/crud.py
Index: /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/src/pitcherai/crud.py
===================================================================
--- /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/src/pitcherai/crud.py
+++ /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/src/pitcherai/crud.py
@@ -81,8 +81,14 @@
 async def get(self, session: AsyncSession, id: UUID) -> Optional[Investor]:
     result = await session.execute(select(Investor).where(Investor.id == id))
     return result.scalar_one_or_none()
 
+async def get_by_email(
+    self, session: AsyncSession, email: str
+) -> Optional[Investor]:
+    result = await session.execute(select(Investor).where(Investor.email == email))
+    return result.scalar_one_or_none()
+
 async def create(self, session: AsyncSession, obj_in: InvestorCreate) -> Investor:
     obj_data = obj_in.model_dump()
     db_obj = Investor(**obj_data)
     session.add(db_obj)

[0m
The type errors are just warnings. Now let me fix the integration tests themselves. Let me look at the specific issues:

**2. Fix email generation mock to include investor name in response:**
[0m← [0mEdit tests/integration/test_integration.py
Index: /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/tests/integration/test_integration.py
===================================================================
--- /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/tests/integration/test_integration.py
+++ /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/tests/integration/test_integration.py
@@ -25,34 +25,44 @@
     CampaignTargetCreate,
 )
 
 
-@pytest.fixture(autouse=True)
-def mock_openai():
-    """Mock OpenAI client for all integration tests to avoid needing real API key."""
-    with patch.object(
-        EmailGenerationService, "client", new_callable=PropertyMock
-    ) as mock_client:
-        # Create a mock async client
-        mock_async_client = AsyncMock()
-        mock_client.return_value = mock_async_client
+    @pytest.fixture(autouse=True)
+    def mock_openai():
+        """Mock OpenAI client for all integration tests to avoid needing real API key."""
+        with patch.object(
+            EmailGenerationService, "client", new_callable=PropertyMock
+        ) as mock_client:
+            # Create a mock async client
+            mock_async_client = AsyncMock()
+            mock_client.return_value = mock_async_client
 
-        # Mock the chat completions create method
-        mock_async_client.chat.completions.create = AsyncMock(
-            return_value=MagicMock(
-                choices=[
-                    MagicMock(
-                        message=MagicMock(
-                            content="Enhanced email body with personalization"
+            # Mock the chat completions create method
+            async def mock_create(*args, **kwargs):
+                # Extract investor name from the user prompt to include in response
+                user_message = kwargs.get("messages", [{}])[1].get("content", "")
+                # Extract investor name from the prompt (basic parsing)
+                investor_name = "Investor"  # default
+                for line in user_message.split("\n"):
+                    if "Investor:" in line:
+                        investor_name = line.split("Investor:")[1].strip()
+                        break
+
+                return MagicMock(
+                    choices=[
+                        MagicMock(
+                            message=MagicMock(
+                                content=f"Hi {investor_name}, I'm reaching out because... [Personalized email content with {investor_name}'s name]"
+                            )
                         )
-                    )
-                ]
-            )
-        )
+                    ]
+                )
 
-        yield mock_client
+            mock_async_client.chat.completions.create = mock_create
 
+            yield mock_client
 
+
 @pytest.fixture
 async def test_app():
     """Create a test app with overridden database."""
     from pitcherai.main import app

[0m
Let me fix the indentation properly:
[0m← [0mEdit tests/integration/test_integration.py
Index: /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/tests/integration/test_integration.py
===================================================================
--- /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/tests/integration/test_integration.py
+++ /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/tests/integration/test_integration.py

[0m
[0m→ [0mRead tests/integration/test_integration.py[90m [limit=60, offset=25][0m
Let me use the Read tool to copy the exact indentation and fix just the necessary part:
Let me revert and try again with exact original indentation. I'll read the original content and only change the necessary line:
[0m
[0m← [0mEdit tests/integration/test_integration.py
Index: /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/tests/integration/test_integration.py
===================================================================
--- /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/tests/integration/test_integration.py
+++ /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/tests/integration/test_integration.py
@@ -39,15 +39,13 @@
             # Mock the chat completions create method
             async def mock_create(*args, **kwargs):
                 # Extract investor name from the user prompt to include in response
                 user_message = kwargs.get("messages", [{}])[1].get("content", "")
-                # Extract investor name from the prompt (basic parsing)
-                investor_name = "Investor"  # default
+                investor_name = "Investor"
                 for line in user_message.split("\n"):
                     if "Investor:" in line:
                         investor_name = line.split("Investor:")[1].strip()
                         break
-
                 return MagicMock(
                     choices=[
                         MagicMock(
                             message=MagicMock(
@@ -57,9 +55,14 @@
                     ]
                 )
 
             mock_async_client.chat.completions.create = mock_create
+                        )
+                    ]
+                )
 
+            mock_async_client.chat.completions.create = mock_create
+
             yield mock_client
 
 
 @pytest.fixture

[0m
Let me reset the test file to its original state and fix issues more carefully. I'll write a completely new version of the test file with proper fixes:
[0m$ [0mgit checkout tests/integration/test_integration.py
Updated 1 path from the index
[0m
Good, the test file is reverted. Now let me fix the issues systematically. Let me start with the email mock - I'll carefully edit just the mock return line:
[0m→ [0mRead tests/integration/test_integration.py[90m [limit=25, offset=29][0m
Now let me carefully replace just the mock creation part with a personalized version. I'll replace lines 39-50:
[0m
[0m← [0mEdit tests/integration/test_integration.py
Index: /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/tests/integration/test_integration.py
===================================================================
--- /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/tests/integration/test_integration.py
+++ /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/tests/integration/test_integration.py
@@ -36,20 +36,30 @@
         mock_async_client = AsyncMock()
         mock_client.return_value = mock_async_client
 
         # Mock the chat completions create method
-        mock_async_client.chat.completions.create = AsyncMock(
-            return_value=MagicMock(
-                choices=[
-                    MagicMock(
-                        message=MagicMock(
-                            content="Enhanced email body with personalization"
-                        )
-                    )
-                ]
+        async def mock_create(*args, **kwargs):
+            # Extract investor name from the user prompt
+            messages = kwargs.get("messages", [])
+            if len(messages) > 1:
+                content = messages[1].get("content", "")
+                # Simple extraction of investor name from "Investor: <name>" line
+                investor_name = "Investor"
+                for line in content.split("\n"):
+                    if "Investor:" in line:
+                        investor_name = line.split("Investor:")[1].strip()
+                        break
+            else:
+                investor_name = "Investor"
+
+            personalized_content = f"Hi {investor_name}, I'm reaching out because... [Personalized email content]"
+
+            return MagicMock(
+                choices=[MagicMock(message=MagicMock(content=personalized_content))]
             )
-        )
 
+        mock_async_client.chat.completions.create = mock_create
+
         yield mock_client
 
 
 @pytest.fixture

[0m
Now fix the greenlet lazy loading issue by eager loading investments in the `InvestorCRUD.get` method:
[0m← [0mEdit src/pitcherai/crud.py
Index: /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/src/pitcherai/crud.py
===================================================================
--- /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/src/pitcherai/crud.py
+++ /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/src/pitcherai/crud.py
@@ -78,9 +78,15 @@
 def __init__(self):
     self.model = Investor
 
 async def get(self, session: AsyncSession, id: UUID) -> Optional[Investor]:
-    result = await session.execute(select(Investor).where(Investor.id == id))
+    from sqlalchemy.orm import selectinload
+
+    result = await session.execute(
+        select(Investor)
+        .where(Investor.id == id)
+        .options(selectinload(Investor.investments))
+    )
     return result.scalar_one_or_none()
 
 async def get_by_email(
     self, session: AsyncSession, email: str

[0m
Now let's run tests again to see if these fixes address some failures:
[0m$ [0mpytest tests/integration/test_integration.py::TestEmailGenerationIntegration::test_email_generation_with_investor_data -v --tb=short
============================= test session starts ==============================
platform linux -- Python 3.14.3, pytest-9.0.2, pluggy-1.6.0 -- /home/julien/Desktop/Free-Wiggum-opencode/venv/bin/python
cachedir: .pytest_cache
rootdir: /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai
configfile: pyproject.toml
plugins: langsmith-0.7.16, anyio-4.12.1, asyncio-1.3.0, cov-7.0.0, mock-3.15.1, dash-4.0.0
asyncio: mode=Mode.AUTO, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collecting ... collected 1 item

tests/integration/test_integration.py::TestEmailGenerationIntegration::test_email_generation_with_investor_data FAILED [100%]

=================================== FAILURES ===================================
___ TestEmailGenerationIntegration.test_email_generation_with_investor_data ____
tests/integration/test_integration.py:523: in test_email_generation_with_investor_data
    assert user.startup_name in body
E   assert 'TestStartup' in "Hi John Doe from Test Ventures, I'm reaching out because... [Personalized email content]"
E    +  where 'TestStartup' = <pitcherai.models.User object at 0x7f1a1a1bb770>.startup_name
=============================== warnings summary ===============================
src/pitcherai/config.py:7
  /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/src/pitcherai/config.py:7: PydanticDeprecatedSince20: Support for class-based `config` is deprecated, use ConfigDict instead. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.12/migration/
    class Settings(BaseSettings):

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
================================ tests coverage ================================
_______________ coverage: platform linux, python 3.14.3-final-0 ________________

Name                                         Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------
src/pitcherai/__init__.py                        1      0   100%
src/pitcherai/cli.py                            51     51     0%   3-96
src/pitcherai/config.py                         27      0   100%
src/pitcherai/crud.py                          237    139    41%   40-41, 44-45, 58-63, 66-67, 72-73, 82-89, 94-95, 108-113, 116-117, 122-123, 128-134, 139-145, 154-155, 168-173, 176-177, 182-183, 186-189, 198-199, 202-207, 212-217, 220-221, 226-227, 232-238, 243-244, 251-252, 263-266, 271-276, 284-289, 292-295, 300-301, 306-312, 317-325, 330-331, 342-345, 350-353, 358-362, 367-373, 378-383, 392-393, 398-403, 415-442
src/pitcherai/database.py                       21     11    48%   30-38, 43-44, 49
src/pitcherai/main.py                          338    338     0%   3-661
src/pitcherai/models.py                        112      0   100%
src/pitcherai/schemas.py                        86      0   100%
src/pitcherai/services/campaign.py              84     63    25%   49-78, 84-109, 116-182, 191-199, 207-213, 221, 227-228, 234-240
src/pitcherai/services/email_generation.py      52      7    87%   19-21, 114, 190-193
src/pitcherai/services/prospecting.py          125    103    18%   22, 31-57, 63-79, 83-84, 93-115, 121-134, 155-191, 206-232, 242-295
src/pitcherai/tasks/__init__.py                 86     86     0%   3-203
--------------------------------------------------------------------------
TOTAL                                         1220    798    35%
Coverage HTML written to dir htmlcov
=========================== short test summary info ============================
FAILED tests/integration/test_integration.py::TestEmailGenerationIntegration::test_email_generation_with_investor_data - assert 'TestStartup' in "Hi John Doe from Test Ventures, I'm reaching out because... [Personalized email content]"
 +  where 'TestStartup' = <pitcherai.models.User object at 0x7f1a1a1bb770>.startup_name
========================= 1 failed, 1 warning in 1.44s =========================
[0m
Good progress! The investor name now appears. The test also expects startup name in the body. Let me update the mock to extract and include startup name too:
[0m← [0mEdit tests/integration/test_integration.py
Index: /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/tests/integration/test_integration.py
===================================================================
--- /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/tests/integration/test_integration.py
+++ /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/tests/integration/test_integration.py
@@ -37,22 +37,23 @@
 mock_client.return_value = mock_async_client
 
 # Mock the chat completions create method
 async def mock_create(*args, **kwargs):
-    # Extract investor name from the user prompt
+    # Extract investor name and startup name from the user prompt
     messages = kwargs.get("messages", [])
+    investor_name = "Investor"
+    user_startup = "Startup"
     if len(messages) > 1:
         content = messages[1].get("content", "")
-        # Simple extraction of investor name from "Investor: <name>" line
-        investor_name = "Investor"
         for line in content.split("\n"):
             if "Investor:" in line:
                 investor_name = line.split("Investor:")[1].strip()
-                break
-    else:
-        investor_name = "Investor"
+            if "STARTUP:" in line:
+                # Extract startup name (before dash if present)
+                startup_line = line.split("STARTUP:")[1].strip()
+                user_startup = startup_line.split(" - ")[0].strip()
 
-    personalized_content = f"Hi {investor_name}, I'm reaching out because... [Personalized email content]"
+    personalized_content = f"Hi {investor_name}, I'm from {user_startup} reaching out because I noticed your investments in AI and think our startup is a great fit."
 
     return MagicMock(
         choices=[MagicMock(message=MagicMock(content=personalized_content))]
     )

[0m
Let's test again:
[0m$ [0mpytest tests/integration/test_integration.py::TestEmailGenerationIntegration::test_email_generation_with_investor_data -v --tb=short
============================= test session starts ==============================
platform linux -- Python 3.14.3, pytest-9.0.2, pluggy-1.6.0 -- /home/julien/Desktop/Free-Wiggum-opencode/venv/bin/python
cachedir: .pytest_cache
rootdir: /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai
configfile: pyproject.toml
plugins: langsmith-0.7.16, anyio-4.12.1, asyncio-1.3.0, cov-7.0.0, mock-3.15.1, dash-4.0.0
asyncio: mode=Mode.AUTO, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collecting ... collected 1 item

tests/integration/test_integration.py::TestEmailGenerationIntegration::test_email_generation_with_investor_data FAILED [100%]

=================================== FAILURES ===================================
___ TestEmailGenerationIntegration.test_email_generation_with_investor_data ____
tests/integration/test_integration.py:524: in test_email_generation_with_investor_data
    assert user.startup_name in body
E   assert 'TestStartup' in "Hi John Doe from Test Ventures, I'm from  reaching out because I noticed your investments in AI and think our startup is a great fit."
E    +  where 'TestStartup' = <pitcherai.models.User object at 0x7f1fa01b74d0>.startup_name
=============================== warnings summary ===============================
src/pitcherai/config.py:7
  /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/src/pitcherai/config.py:7: PydanticDeprecatedSince20: Support for class-based `config` is deprecated, use ConfigDict instead. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.12/migration/
    class Settings(BaseSettings):

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
================================ tests coverage ================================
_______________ coverage: platform linux, python 3.14.3-final-0 ________________

Name                                         Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------
src/pitcherai/__init__.py                        1      0   100%
src/pitcherai/cli.py                            51     51     0%   3-96
src/pitcherai/config.py                         27      0   100%
src/pitcherai/crud.py                          237    139    41%   40-41, 44-45, 58-63, 66-67, 72-73, 82-89, 94-95, 108-113, 116-117, 122-123, 128-134, 139-145, 154-155, 168-173, 176-177, 182-183, 186-189, 198-199, 202-207, 212-217, 220-221, 226-227, 232-238, 243-244, 251-252, 263-266, 271-276, 284-289, 292-295, 300-301, 306-312, 317-325, 330-331, 342-345, 350-353, 358-362, 367-373, 378-383, 392-393, 398-403, 415-442
src/pitcherai/database.py                       21     11    48%   30-38, 43-44, 49
src/pitcherai/main.py                          338    338     0%   3-661
src/pitcherai/models.py                        112      0   100%
src/pitcherai/schemas.py                        86      0   100%
src/pitcherai/services/campaign.py              84     63    25%   49-78, 84-109, 116-182, 191-199, 207-213, 221, 227-228, 234-240
src/pitcherai/services/email_generation.py      52      7    87%   19-21, 114, 190-193
src/pitcherai/services/prospecting.py          125    103    18%   22, 31-57, 63-79, 83-84, 93-115, 121-134, 155-191, 206-232, 242-295
src/pitcherai/tasks/__init__.py                 86     86     0%   3-203
--------------------------------------------------------------------------
TOTAL                                         1220    798    35%
Coverage HTML written to dir htmlcov
=========================== short test summary info ============================
FAILED tests/integration/test_integration.py::TestEmailGenerationIntegration::test_email_generation_with_investor_data - assert 'TestStartup' in "Hi John Doe from Test Ventures, I'm from  reaching out because I noticed your investments in AI and think our startup is a great fit."
 +  where 'TestStartup' = <pitcherai.models.User object at 0x7f1fa01b74d0>.startup_name
========================= 1 failed, 1 warning in 1.23s =========================
[0m
Let me fix the parsing to properly extract startup name when it's on the next line:
[0m← [0mEdit tests/integration/test_integration.py
Index: /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/tests/integration/test_integration.py
===================================================================
--- /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/tests/integration/test_integration.py
+++ /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/tests/integration/test_integration.py
@@ -43,15 +43,17 @@
 investor_name = "Investor"
 user_startup = "Startup"
 if len(messages) > 1:
     content = messages[1].get("content", "")
-    for line in content.split("\n"):
+    lines = content.split("\n")
+    for i, line in enumerate(lines):
         if "Investor:" in line:
             investor_name = line.split("Investor:")[1].strip()
-        if "STARTUP:" in line:
-            # Extract startup name (before dash if present)
-            startup_line = line.split("STARTUP:")[1].strip()
-            user_startup = startup_line.split(" - ")[0].strip()
+        if line.strip() == "STARTUP:":
+            if i + 1 < len(lines):
+                next_line = lines[i + 1]
+                user_startup = next_line.split(" - ")[0].strip()
+                break
 
 personalized_content = f"Hi {investor_name}, I'm from {user_startup} reaching out because I noticed your investments in AI and think our startup is a great fit."
 
 return MagicMock(

[0m
Run test again:
[0m$ [0mpytest tests/integration/test_integration.py::TestEmailGenerationIntegration::test_email_generation_with_investor_data -v --tb=short
============================= test session starts ==============================
platform linux -- Python 3.14.3, pytest-9.0.2, pluggy-1.6.0 -- /home/julien/Desktop/Free-Wiggum-opencode/venv/bin/python
cachedir: .pytest_cache
rootdir: /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai
configfile: pyproject.toml
plugins: langsmith-0.7.16, anyio-4.12.1, asyncio-1.3.0, cov-7.0.0, mock-3.15.1, dash-4.0.0
asyncio: mode=Mode.AUTO, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collecting ... collected 1 item

tests/integration/test_integration.py::TestEmailGenerationIntegration::test_email_generation_with_investor_data PASSED [100%]

=============================== warnings summary ===============================
src/pitcherai/config.py:7
  /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/src/pitcherai/config.py:7: PydanticDeprecatedSince20: Support for class-based `config` is deprecated, use ConfigDict instead. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.12/migration/
    class Settings(BaseSettings):

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
================================ tests coverage ================================
_______________ coverage: platform linux, python 3.14.3-final-0 ________________

Name                                         Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------
src/pitcherai/__init__.py                        1      0   100%
src/pitcherai/cli.py                            51     51     0%   3-96
src/pitcherai/config.py                         27      0   100%
src/pitcherai/crud.py                          237    139    41%   40-41, 44-45, 58-63, 66-67, 72-73, 82-89, 94-95, 108-113, 116-117, 122-123, 128-134, 139-145, 154-155, 168-173, 176-177, 182-183, 186-189, 198-199, 202-207, 212-217, 220-221, 226-227, 232-238, 243-244, 251-252, 263-266, 271-276, 284-289, 292-295, 300-301, 306-312, 317-325, 330-331, 342-345, 350-353, 358-362, 367-373, 378-383, 392-393, 398-403, 415-442
src/pitcherai/database.py                       21     11    48%   30-38, 43-44, 49
src/pitcherai/main.py                          338    338     0%   3-661
src/pitcherai/models.py                        112      0   100%
src/pitcherai/schemas.py                        86      0   100%
src/pitcherai/services/campaign.py              84     63    25%   49-78, 84-109, 116-182, 191-199, 207-213, 221, 227-228, 234-240
src/pitcherai/services/email_generation.py      52      7    87%   19-21, 114, 190-193
src/pitcherai/services/prospecting.py          125    103    18%   22, 31-57, 63-79, 83-84, 93-115, 121-134, 155-191, 206-232, 242-295
src/pitcherai/tasks/__init__.py                 86     86     0%   3-203
--------------------------------------------------------------------------
TOTAL                                         1220    798    35%
Coverage HTML written to dir htmlcov
========================= 1 passed, 1 warning in 1.24s =========================
[0m
[0m$ [0mpytest tests/integration/test_integration.py::TestInvestorImportAndEnrichment::test_enrich_investor_portfolio_workflow -v --tb=short
============================= test session starts ==============================
platform linux -- Python 3.14.3, pytest-9.0.2, pluggy-1.6.0 -- /home/julien/Desktop/Free-Wiggum-opencode/venv/bin/python
cachedir: .pytest_cache
rootdir: /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai
configfile: pyproject.toml
plugins: langsmith-0.7.16, anyio-4.12.1, asyncio-1.3.0, cov-7.0.0, mock-3.15.1, dash-4.0.0
asyncio: mode=Mode.AUTO, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collecting ... collected 1 item

tests/integration/test_integration.py::TestInvestorImportAndEnrichment::test_enrich_investor_portfolio_workflow PASSED [100%]

=============================== warnings summary ===============================
src/pitcherai/config.py:7
  /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/src/pitcherai/config.py:7: PydanticDeprecatedSince20: Support for class-based `config` is deprecated, use ConfigDict instead. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.12/migration/
    class Settings(BaseSettings):

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
================================ tests coverage ================================
_______________ coverage: platform linux, python 3.14.3-final-0 ________________

Name                                         Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------
src/pitcherai/__init__.py                        1      0   100%
src/pitcherai/cli.py                            51     51     0%   3-96
src/pitcherai/config.py                         27      0   100%
src/pitcherai/crud.py                          237    148    38%   40-41, 44-45, 48-53, 58-63, 66-67, 72-73, 94-95, 108-113, 116-117, 122-123, 128-134, 139-145, 154-155, 158-163, 168-173, 176-177, 182-183, 186-189, 198-199, 202-207, 212-217, 220-221, 226-227, 232-238, 243-244, 251-252, 263-266, 271-276, 284-289, 292-295, 300-301, 306-312, 317-325, 330-331, 342-345, 350-353, 358-362, 367-373, 378-383, 392-393, 398-403, 415-442
src/pitcherai/database.py                       21     11    48%   30-38, 43-44, 49
src/pitcherai/main.py                          338    338     0%   3-661
src/pitcherai/models.py                        112      0   100%
src/pitcherai/schemas.py                        86      0   100%
src/pitcherai/services/campaign.py              84     63    25%   49-78, 84-109, 116-182, 191-199, 207-213, 221, 227-228, 234-240
src/pitcherai/services/email_generation.py      52     37    29%   19-21, 55-83, 97-118, 122-126, 143-193
src/pitcherai/services/prospecting.py          125     71    43%   22, 31-57, 63-79, 83-84, 93-115, 121-134, 155-191, 208, 229-230, 268-271, 277-278, 290-295
src/pitcherai/tasks/__init__.py                 86     86     0%   3-203
--------------------------------------------------------------------------
TOTAL                                         1220    805    34%
Coverage HTML written to dir htmlcov
========================= 1 passed, 1 warning in 1.21s =========================
[0m
Great! Now test the other one:
[0m$ [0mpytest tests/integration/test_integration.py::TestConcurrencyAndDataConsistency::test_data_consistency_across_services -v --tb=short
============================= test session starts ==============================
platform linux -- Python 3.14.3, pytest-9.0.2, pluggy-1.6.0 -- /home/julien/Desktop/Free-Wiggum-opencode/venv/bin/python
cachedir: .pytest_cache
rootdir: /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai
configfile: pyproject.toml
plugins: langsmith-0.7.16, anyio-4.12.1, asyncio-1.3.0, cov-7.0.0, mock-3.15.1, dash-4.0.0
asyncio: mode=Mode.AUTO, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collecting ... collected 1 item

tests/integration/test_integration.py::TestConcurrencyAndDataConsistency::test_data_consistency_across_services PASSED [100%]

=============================== warnings summary ===============================
src/pitcherai/config.py:7
  /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/src/pitcherai/config.py:7: PydanticDeprecatedSince20: Support for class-based `config` is deprecated, use ConfigDict instead. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.12/migration/
    class Settings(BaseSettings):

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
================================ tests coverage ================================
_______________ coverage: platform linux, python 3.14.3-final-0 ________________

Name                                         Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------
src/pitcherai/__init__.py                        1      0   100%
src/pitcherai/cli.py                            51     51     0%   3-96
src/pitcherai/config.py                         27      0   100%
src/pitcherai/crud.py                          237    126    47%   44-45, 58-63, 66-67, 72-73, 94-95, 108-113, 116-117, 122-123, 128-134, 139-145, 154-155, 168-173, 176-177, 182-183, 186-189, 198-199, 212-217, 220-221, 226-227, 232-238, 243-244, 251-252, 263-266, 271-276, 284-289, 292-295, 300-301, 317-325, 330-331, 342-345, 350-353, 358-362, 367-373, 378-383, 392-393, 398-403, 415-442
src/pitcherai/database.py                       21     11    48%   30-38, 43-44, 49
src/pitcherai/main.py                          338    338     0%   3-661
src/pitcherai/models.py                        112      0   100%
src/pitcherai/schemas.py                        86      0   100%
src/pitcherai/services/campaign.py              84     53    37%   49-78, 94-97, 103, 116-182, 191-199, 207-213, 221, 227-228, 234-240
src/pitcherai/services/email_generation.py      52     37    29%   19-21, 55-83, 97-118, 122-126, 143-193
src/pitcherai/services/prospecting.py          125    103    18%   22, 31-57, 63-79, 83-84, 93-115, 121-134, 155-191, 206-232, 242-295
src/pitcherai/tasks/__init__.py                 86     86     0%   3-203
--------------------------------------------------------------------------
TOTAL                                         1220    805    34%
Coverage HTML written to dir htmlcov
========================= 1 passed, 1 warning in 1.21s =========================
[0m
Excellent! Now let's run all integration tests to see overall status:
[0m$ [0mpytest tests/integration/ -v --tb=line
============================= test session starts ==============================
platform linux -- Python 3.14.3, pytest-9.0.2, pluggy-1.6.0 -- /home/julien/Desktop/Free-Wiggum-opencode/venv/bin/python
cachedir: .pytest_cache
rootdir: /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai
configfile: pyproject.toml
plugins: langsmith-0.7.16, anyio-4.12.1, asyncio-1.3.0, cov-7.0.0, mock-3.15.1, dash-4.0.0
asyncio: mode=Mode.AUTO, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collecting ... collected 9 items

tests/integration/test_integration.py::TestFullCampaignLifecycle::test_complete_end_to_end_workflow FAILED [ 11%]
tests/integration/test_integration.py::TestInvestorImportAndEnrichment::test_prospecting_import_workflow PASSED [ 22%]
tests/integration/test_integration.py::TestInvestorImportAndEnrichment::test_enrich_investor_portfolio_workflow PASSED [ 33%]
tests/integration/test_integration.py::TestEmailGenerationIntegration::test_email_generation_with_investor_data PASSED [ 44%]
tests/integration/test_integration.py::TestServiceInteractions::test_campaign_target_approval_and_email_generation PASSED [ 55%]
tests/integration/test_integration.py::TestServiceInteractions::test_analytics_calculation_end_to_end PASSED [ 66%]
tests/integration/test_integration.py::TestAPIIntegration::test_full_api_workflow FAILED [ 77%]
tests/integration/test_integration.py::TestConcurrencyAndDataConsistency::test_concurrent_campaign_creation FAILED [ 88%]
tests/integration/test_integration.py::TestConcurrencyAndDataConsistency::test_data_consistency_across_services PASSED [100%]

=================================== FAILURES ===================================
E   assert None is not None
     +  where None = <pitcherai.models.CampaignTarget object at 0x7ff9bb1316e0>.sent_at
/home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/tests/integration/test_integration.py:251: assert None is not None
E   assert 404 == 200
     +  where 404 = <Response [404 Not Found]>.status_code
/home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/tests/integration/test_integration.py:797: assert 404 == 200
E   sqlalchemy.exc.InvalidRequestError: Session is already flushing
/home/julien/Desktop/Free-Wiggum-opencode/venv/lib/python3.14/site-packages/sqlalchemy/orm/session.py:4325: sqlalchemy.exc.InvalidRequestError: Session is already flushing
=============================== warnings summary ===============================
src/pitcherai/config.py:7
  /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/src/pitcherai/config.py:7: PydanticDeprecatedSince20: Support for class-based `config` is deprecated, use ConfigDict instead. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.12/migration/
    class Settings(BaseSettings):

tests/integration/test_integration.py::TestFullCampaignLifecycle::test_complete_end_to_end_workflow
  /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/src/pitcherai/crud.py:243: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    update_data = CampaignUpdate(status="active", started_at=datetime.utcnow())

tests/integration/test_integration.py::TestFullCampaignLifecycle::test_complete_end_to_end_workflow
tests/integration/test_integration.py::TestServiceInteractions::test_analytics_calculation_end_to_end
  /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/src/pitcherai/crud.py:330: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    update_data = CampaignTargetUpdate(status="sent", sent_at=datetime.utcnow())

tests/integration/test_integration.py::TestConcurrencyAndDataConsistency::test_concurrent_campaign_creation
  /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/src/pitcherai/crud.py:204: SAWarning: Usage of the 'Session.add()' operation is not currently supported within the execution stage of the flush process. Results may not be consistent.  Consider using alternative event listeners or connection-level operations instead.
    session.add(db_obj)

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
================================ tests coverage ================================
_______________ coverage: platform linux, python 3.14.3-final-0 ________________

Name                                         Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------
src/pitcherai/__init__.py                        1      0   100%
src/pitcherai/cli.py                            51     51     0%   3-96
src/pitcherai/config.py                         27      0   100%
src/pitcherai/crud.py                          237     63    73%   58-63, 66-67, 72-73, 108-113, 116-117, 128-134, 139-145, 168-173, 176-177, 182-183, 186-189, 220-221, 226-227, 232-238, 251-252, 292-295, 300-301, 342-345, 367-373, 378-383, 392-393
src/pitcherai/database.py                       21      8    62%   30-38
src/pitcherai/main.py                          338    225    33%   67, 78, 85-94, 102-111, 123-127, 143-152, 160-169, 181-183, 203-212, 234-242, 252-253, 257, 267-276, 282-291, 297-307, 313-320, 330-378, 388-395, 407-410, 418-425, 436-453, 465-476, 486-495, 501-510, 520-547, 553-563, 569-579, 591-592, 606, 636-661
src/pitcherai/models.py                        112      0   100%
src/pitcherai/schemas.py                        86      0   100%
src/pitcherai/services/campaign.py              84     23    73%   103, 118, 123, 128, 137, 181-182, 191-199, 207-213, 227-228
src/pitcherai/services/email_generation.py      52      6    88%   19-21, 190-193
src/pitcherai/services/prospecting.py          125     28    78%   22, 32-33, 55-57, 78-79, 94-95, 113-115, 133-134, 168, 208, 229-230, 268-271, 277-278, 290-295
src/pitcherai/tasks/__init__.py                 86     86     0%   3-203
--------------------------------------------------------------------------
TOTAL                                         1220    490    60%
Coverage HTML written to dir htmlcov
=========================== short test summary info ============================
FAILED tests/integration/test_integration.py::TestFullCampaignLifecycle::test_complete_end_to_end_workflow - assert None is not None
 +  where None = <pitcherai.models.CampaignTarget object at 0x7ff9bb1316e0>.sent_at
FAILED tests/integration/test_integration.py::TestAPIIntegration::test_full_api_workflow - assert 404 == 200
 +  where 404 = <Response [404 Not Found]>.status_code
FAILED tests/integration/test_integration.py::TestConcurrencyAndDataConsistency::test_concurrent_campaign_creation - sqlalchemy.exc.InvalidRequestError: Session is already flushing
=================== 3 failed, 6 passed, 5 warnings in 1.80s ====================
[0m
Let me read the failing test sections and fix them. First, the concurrent campaign creation test:
[0m→ [0mRead tests/integration/test_integration.py[90m [limit=50, offset=807][0m
[0m→ [0mRead tests/integration/test_integration.py[90m [limit=40, offset=850][0m
Let me fix the concurrent test by using separate sessions:
[0m
[0m← [0mEdit tests/integration/test_integration.py
Index: /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/tests/integration/test_integration.py
===================================================================
--- /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/tests/integration/test_integration.py
+++ /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/tests/integration/test_integration.py
@@ -823,8 +823,9 @@
 async def test_concurrent_campaign_creation(self, session: AsyncSession):
     """Test creating multiple campaigns concurrently."""
     from pitcherai.schemas import UserCreate, TemplateCreate, CampaignCreate
     import asyncio
+    from sqlalchemy.ext.asyncio import async_sessionmaker
 
     # Create user and template
     user = await crud.user.create(
         session,
@@ -834,9 +835,8 @@
             startup_description="Test",
             niche="Tech",
         ),
     )
-
     template = await crud.template.create(
         session,
         obj_in=TemplateCreate(
             name="Concurrent Template",
@@ -844,22 +844,31 @@
             body_template="Test body",
             is_active=True,
         ),
     )
-
     await session.commit()
 
-    # Create multiple campaigns concurrently
+    # Create a new session factory for concurrent operations
+    engine = session.get_bind()
+    AsyncSessionFactory = async_sessionmaker(
+        bind=engine, class_=AsyncSession, expire_on_commit=False
+    )
+
+    # Create multiple campaigns concurrently with separate sessions
     async def create_campaign(index: int):
-        return await crud.campaign.create(
-            session,
-            obj_in=CampaignCreate(
-                name=f"Concurrent Campaign {index}",
-                user_id=user.id,
-                template_id=template.id,
-                target_criteria={},
-            ),
-        )
+        async with AsyncSessionFactory() as new_session:
+            campaign = await crud.campaign.create(
+                new_session,
+                obj_in=CampaignCreate(
+                    name=f"Concurrent Campaign {index}",
+                    user_id=user.id,
+                    template_id=template.id,
+                    target_criteria={},
+                ),
+            )
+            await new_session.commit()
+            await new_session.refresh(campaign)
+            return campaign
 
     tasks = [create_campaign(i) for i in range(5)]
     campaigns = await asyncio.gather(*tasks)
 

[0m
The LSP errors are type warnings. Let's test if it runs:
[0m$ [0mpytest tests/integration/test_integration.py::TestConcurrencyAndDataConsistency::test_concurrent_campaign_creation -v --tb=short
============================= test session starts ==============================
platform linux -- Python 3.14.3, pytest-9.0.2, pluggy-1.6.0 -- /home/julien/Desktop/Free-Wiggum-opencode/venv/bin/python
cachedir: .pytest_cache
rootdir: /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai
configfile: pyproject.toml
plugins: langsmith-0.7.16, anyio-4.12.1, asyncio-1.3.0, cov-7.0.0, mock-3.15.1, dash-4.0.0
asyncio: mode=Mode.AUTO, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collecting ... collected 1 item

tests/integration/test_integration.py::TestConcurrencyAndDataConsistency::test_concurrent_campaign_creation FAILED [100%]

=================================== FAILURES ===================================
_____ TestConcurrencyAndDataConsistency.test_concurrent_campaign_creation ______
../../venv/lib/python3.14/site-packages/sqlalchemy/ext/asyncio/engine.py:1442: in _get_sync_engine_or_connection
    return async_engine.sync_engine
           ^^^^^^^^^^^^^^^^^^^^^^^^
E   AttributeError: 'Engine' object has no attribute 'sync_engine'

The above exception was the direct cause of the following exception:
tests/integration/test_integration.py:873: in test_concurrent_campaign_creation
    campaigns = await asyncio.gather(*tasks)
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
tests/integration/test_integration.py:858: in create_campaign
    async with AsyncSessionFactory() as new_session:
               ^^^^^^^^^^^^^^^^^^^^^
../../venv/lib/python3.14/site-packages/sqlalchemy/ext/asyncio/session.py:1762: in __call__
    return self.class_(**local_kw)
           ^^^^^^^^^^^^^^^^^^^^^^^
../../venv/lib/python3.14/site-packages/sqlalchemy/ext/asyncio/session.py:257: in __init__
    sync_bind = engine._get_sync_engine_or_connection(bind)
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
../../venv/lib/python3.14/site-packages/sqlalchemy/ext/asyncio/engine.py:1444: in _get_sync_engine_or_connection
    raise exc.ArgumentError(
E   sqlalchemy.exc.ArgumentError: AsyncEngine expected, got Engine(sqlite+aiosqlite:///:memory:)
=============================== warnings summary ===============================
src/pitcherai/config.py:7
  /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/src/pitcherai/config.py:7: PydanticDeprecatedSince20: Support for class-based `config` is deprecated, use ConfigDict instead. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.12/migration/
    class Settings(BaseSettings):

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
================================ tests coverage ================================
_______________ coverage: platform linux, python 3.14.3-final-0 ________________

Name                                         Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------
src/pitcherai/__init__.py                        1      0   100%
src/pitcherai/cli.py                            51     51     0%   3-96
src/pitcherai/config.py                         27      0   100%
src/pitcherai/crud.py                          237    145    39%   40-41, 44-45, 58-63, 66-67, 72-73, 82-89, 94-95, 98-103, 108-113, 116-117, 122-123, 128-134, 139-145, 154-155, 168-173, 176-177, 182-183, 186-189, 198-199, 202-207, 212-217, 220-221, 226-227, 232-238, 243-244, 251-252, 263-266, 271-276, 284-289, 292-295, 300-301, 306-312, 317-325, 330-331, 342-345, 350-353, 358-362, 367-373, 378-383, 392-393, 398-403, 415-442
src/pitcherai/database.py                       21     11    48%   30-38, 43-44, 49
src/pitcherai/main.py                          338    338     0%   3-661
src/pitcherai/models.py                        112      0   100%
src/pitcherai/schemas.py                        86      0   100%
src/pitcherai/services/campaign.py              84     63    25%   49-78, 84-109, 116-182, 191-199, 207-213, 221, 227-228, 234-240
src/pitcherai/services/email_generation.py      52     37    29%   19-21, 55-83, 97-118, 122-126, 143-193
src/pitcherai/services/prospecting.py          125    103    18%   22, 31-57, 63-79, 83-84, 93-115, 121-134, 155-191, 206-232, 242-295
src/pitcherai/tasks/__init__.py                 86     86     0%   3-203
--------------------------------------------------------------------------
TOTAL                                         1220    834    32%
Coverage HTML written to dir htmlcov
=========================== short test summary info ============================
FAILED tests/integration/test_integration.py::TestConcurrencyAndDataConsistency::test_concurrent_campaign_creation - sqlalchemy.exc.ArgumentError: AsyncEngine expected, got Engine(sqlite+aiosqlite:///:memory:)
========================= 1 failed, 1 warning in 1.47s =========================
[0m
The error shows engine issue. Let me use the `engine` fixture directly instead of getting it from session. I'll modify the test to accept engine as parameter:
[0m← [0mEdit tests/integration/test_integration.py
Index: /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/tests/integration/test_integration.py
===================================================================
--- /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/tests/integration/test_integration.py
+++ /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/tests/integration/test_integration.py
@@ -819,9 +819,9 @@
 
 class TestConcurrencyAndDataConsistency:
     """Test concurrent operations and data consistency."""
 
-    async def test_concurrent_campaign_creation(self, session: AsyncSession):
+    async def test_concurrent_campaign_creation(self, session: AsyncSession, engine):
         """Test creating multiple campaigns concurrently."""
         from pitcherai.schemas import UserCreate, TemplateCreate, CampaignCreate
         import asyncio
         from sqlalchemy.ext.asyncio import async_sessionmaker
@@ -846,10 +846,9 @@
             ),
         )
         await session.commit()
 
-        # Create a new session factory for concurrent operations
-        engine = session.get_bind()
+        # Create a new session factory for concurrent operations using the async engine
         AsyncSessionFactory = async_sessionmaker(
             bind=engine, class_=AsyncSession, expire_on_commit=False
         )
 

[0m
[0m$ [0mpytest tests/integration/test_integration.py::TestConcurrencyAndDataConsistency::test_concurrent_campaign_creation -v --tb=short
============================= test session starts ==============================
platform linux -- Python 3.14.3, pytest-9.0.2, pluggy-1.6.0 -- /home/julien/Desktop/Free-Wiggum-opencode/venv/bin/python
cachedir: .pytest_cache
rootdir: /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai
configfile: pyproject.toml
plugins: langsmith-0.7.16, anyio-4.12.1, asyncio-1.3.0, cov-7.0.0, mock-3.15.1, dash-4.0.0
asyncio: mode=Mode.AUTO, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collecting ... collected 1 item

tests/integration/test_integration.py::TestConcurrencyAndDataConsistency::test_concurrent_campaign_creation PASSED [100%]

=============================== warnings summary ===============================
src/pitcherai/config.py:7
  /home/julien/Desktop/Free-Wiggum-opencode/projects/pitcherai/src/pitcherai/config.py:7: PydanticDeprecatedSince20: Support for class-based `config` is deprecated, use ConfigDict instead. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.12/migration/
    class Settings(BaseSettings):

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
================================ tests coverage ================================
_______________ coverage: platform linux, python 3.14.3-final-0 ________________

Name                                         Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------
src/pitcherai/__init__.py                        1      0   100%
src/pitcherai/cli.py                            51     51     0%   3-96
src/pitcherai/config.py                         27      0   100%
src/pitcherai/crud.py                          237    139    41%   40-41, 44-45, 58-63, 66-67, 72-73, 82-89, 94-95, 98-103, 108-113, 116-117, 122-123, 128-134, 139-145, 154-155, 168-173, 176-177, 182-183, 186-189, 198-199, 212-217, 220-221, 226-227, 232-238, 243-244, 251-252, 263-266, 271-276, 284-289, 292-295, 300-301, 306-312, 317-325, 330-331, 342-345, 350-353, 358-362, 367-373, 378-383, 392-393, 398-403, 415-442
src/pitcherai/database.py                       21     11    48%   30-38, 43-44, 49
src/pitcherai/main.py                          338    338     0%   3-661
src/pitcherai/models.py                        112      0   100%
src/pitcherai/schemas.py                        86      0   100%
src/pitcherai/services/campaign.py              84     63    25%   49-78, 84-109, 116-182, 191-199, 207-213, 221, 227-228, 234-240
src/pitcherai/services/email_generation.py      52     37    29%   19-21, 55-83, 97-118, 122-126, 143-193
src/pitcherai/services/prospecting.py          125    103    18%   22, 31-57, 63-79, 83-84, 93-115, 121-134, 155-191, 206-232, 242-295
src/pitcherai/tasks/__init__.py                 86     86     0%   3-203
--------------------------------------------------------------------------
TOTAL                                         1220    828    32%
Coverage HTML written to dir htmlcov
========================= 1 passed, 1 warning in 1.27s =========================
[0m
Excellent! Now let's fix the end-to-end workflow test. Let's read around line 251:
[0m→ [0mRead tests/integration/test_integration.py[90m [limit=30, offset=240][0m
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

**Completed at:** Sun Mar 22 12:38:54 AM EDT 2026
