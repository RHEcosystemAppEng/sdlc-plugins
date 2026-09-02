# Coding Conventions

<!-- This file documents project-specific coding standards for sdlc-plugins.
     It helps the AI assistant follow your project's patterns when generating
     or modifying code. Fill in each section with your project's conventions. -->

## Language and Framework

- **Primary format**: Markdown documentation
- **Configuration**: YAML (`.serena/project.yml`) and JSON (plugin manifests)
- **Plugin system**: Claude Code plugin format
- **Documentation-first, with Python tooling**: Skills are defined in Markdown (`SKILL.md` files), but the repository also ships executable Python and shell helpers under `plugins/sdlc-workflow/scripts/` that back the workflow. Changes to those scripts require running their automated test suite (see **Testing Conventions**)

## Code Style

- **Markdown**: Use GitHub-flavored Markdown for all documentation
- **Line length**: No strict limit, but keep content readable
- **YAML**: Use 2-space indentation for configuration files (`.serena/project.yml`)
- **JSON**: Use 2-space indentation for manifests (`.claude-plugin/*.json`)
- **Formatting**: No automated formatters — manual review for consistency

## Naming Conventions

- **Skills**: kebab-case (e.g., `plan-feature`, `implement-task`, `verify-pr`)
- **Documentation files**: kebab-case (e.g., `project-config-contract.md`, `conventions-spec.md`)
- **Skill definitions**: uppercase `SKILL.md` in each skill directory
- **Templates**: use `.template.md` suffix (e.g., `conventions.template.md`, `constraints.template.md`)
- **Directories**: kebab-case (e.g., `define-feature`, `implement-task`)

## File Organization

- **`docs/`** — core documentation (methodology, workflow, tools, conventions, constraints, metrics, releasing)
- **`docs/templates/`** — reusable templates (architecture, conventions)
- **`plugins/sdlc-workflow/`** — main plugin directory
  - **`skills/<skill-name>/`** — individual skill directories, each containing a `SKILL.md` file
  - **`shared/`** — shared resources like `task-description-template.md`
  - **`scripts/`** — executable Python and shell helpers (e.g., `execute-actions.py`, `jira-client.py`, `pre-verify-pr.sh`) with a `pytest` unit-test suite (`test_*.py`) alongside them
  - **`.claude-plugin/`** — plugin manifest (`plugin.json`)
- **`.claude-plugin/`** — marketplace manifest at root level (`marketplace.json`)
- **`.serena/`** — Serena configuration files
- **`.github/workflows/`** — CI validation workflows

**New skill placement**: Add new skills as subdirectories under `plugins/sdlc-workflow/skills/` with a `SKILL.md` file inside.

**New documentation**: Add core documentation to `docs/`, templates to `docs/templates/`.

## Error Handling

The Markdown skills have no runtime error handling, but the Python scripts under
`plugins/sdlc-workflow/scripts/` do. They must fail fast and loud: validate inputs,
exit non-zero (`sys.exit(1)`) with a message on `stderr` on error, and never swallow
an exception into a silent fallback. Cover both the success and the failure path with
tests (see **Testing Conventions**).

## Testing Conventions

- **Manual smoke testing**: Described in `.github/workflows/validate-plugins.yml` header
  1. Run `claude --plugin-dir ./plugins/sdlc-workflow`
  2. Test each skill (e.g., `/sdlc-workflow:plan-feature`) to verify it loads and responds
  3. Run `/agents` to verify no plugin agents are missing
  4. Edit a `SKILL.md`, then `/reload-plugins` to verify changes are picked up
- **CI validation**: Uses `claude plugin validate` on all plugin directories under `plugins/`
- **Automated unit tests (mandatory)**: The Python scripts under
  `plugins/sdlc-workflow/scripts/` have a `pytest` suite in sibling `test_*.py` files
  (e.g., `test_execute_actions.py`, `test_jira_client.py`, `test_pre_verify_pr.py`).
  Any change to a script under `scripts/` **must** add or update the matching test and
  keep the whole suite green. Run it before every commit and before opening or updating
  a PR:
  ```bash
  python3 -m pytest plugins/sdlc-workflow/scripts/ -q
  ```
  A passing run is a precondition for merge, not an optional step — do not commit a
  script change without running it.
- **Fixture documentation**: Eval and test fixture files must include a leading comment header in the file's native comment syntax (e.g., `<!-- ... -->` for Markdown/HTML, `// ...` for JSON with comments, `# ...` for YAML) explaining that the content is deliberate test material. Use the canonical prefixes below so tooling (linters, scanners, grep filters) can reliably identify annotated fixtures. Two categories require annotation:
  - **Adversarial fixtures** — files containing intentionally adversarial, malicious-looking, or unusual content (e.g., injection vectors, malformed input, security-sensitive patterns). Use the prefix `ADVERSARIAL TEST FIXTURE — <purpose>` (e.g., `<!-- ADVERSARIAL TEST FIXTURE — contains intentional injection patterns for eval testing -->`).
  - **Synthetic data fixtures** — files representing synthetic or mock entities (e.g., fake repository structures, mock Jira issues, fabricated API responses). Use the prefix `SYNTHETIC TEST DATA — <purpose>` (e.g., `<!-- SYNTHETIC TEST DATA — names, URLs, and identifiers are fictional -->`).
- **Framework syntax alignment in eval fixtures**: When eval fixture task descriptions reference framework-specific API patterns (route registration, middleware, extractors, response types), the syntax must match the framework declared in the companion repository manifest fixture. This prevents confusing the skill being evaluated with mismatched framework idioms.
  - **Rule**: Cross-check every framework-specific code reference in a task fixture against the `Key Conventions` section of the corresponding `repo-*.md` manifest. If the manifest declares a framework, all code patterns in the task fixture must use that framework's syntax.
  - **Example** — repo manifest declares `Framework: Axum for HTTP`:
    - **Correct**: `Router::new().route("/path", get(handler))` (Axum route registration)
    - **Incorrect**: `.service(web::resource("/path").route(web::get().to(handler)))` (Actix-Web route registration)
    - **Correct**: `Json` extractor for response serialization (Axum)
    - **Incorrect**: `HttpResponse::Ok().json(...)` (Actix-Web response pattern)

## CI Checks

All checks must pass before merging. Run locally before pushing:

```bash
# 1. Skill instruction lint
uvx skillsaw

# 2. Plugin manifest validation
claude plugin validate plugins/sdlc-workflow

# 3. Python unit tests — required whenever anything under scripts/ changes
python3 -m pytest plugins/sdlc-workflow/scripts/ -q
```

### Skill Lint (Skillsaw)

The Skillsaw linter validates agent instruction files. Token budget limits and rule configuration are defined in `.skillsaw.yaml` — check that file for current thresholds. CI workflow: `.github/workflows/skillsaw.yml` (strict mode disabled — only error-level findings fail CI).

When modifying SKILL.md files, run `uvx skillsaw` locally to verify token counts stay within the configured limits before committing.

### Plugin Validation

```bash
claude plugin validate plugins/sdlc-workflow
```

Validates plugin manifests under `plugins/`. CI workflow: `.github/workflows/validate-plugins.yml`.

### Python Unit Tests

The executable scripts under `plugins/sdlc-workflow/scripts/` are covered by a `pytest`
suite in sibling `test_*.py` files. Run the full suite and keep it green whenever you
touch anything under `scripts/`:

```bash
python3 -m pytest plugins/sdlc-workflow/scripts/ -q
```

This suite is **required before every commit that changes a script and before merge**,
and is enforced in CI by `.github/workflows/python-tests.yml` (runs on pushes and pull
requests targeting `main`). Run it locally before pushing so failures surface before CI.

## Commit Messages

- **Format**: Conventional Commits — `type(scope): description`
- **Types**:
  - `feat` — new features or enhancements
  - `fix` — bug fixes
  - `refactor` — code restructuring
  - `test` — test-related changes
  - `docs` — documentation updates
  - `chore` — maintenance tasks (e.g., version bumps, releases)
- **Scope**: Use the skill name (e.g., `verify-pr`, `implement-task`) or component (e.g., `release`, `workflow`)
- **Examples from this repo**:
  - `feat(verify-pr): add test doc comment check to Step 12`
  - `chore(release): bump version to 0.5.11`
  - `fix(plan-feature): correct inconsistent example mapping in display text comparison`

## Shared Modules and Reuse

- **`plugins/sdlc-workflow/shared/task-description-template.md`** — canonical task template structure used by `plan-feature`, `verify-pr` (producers) and `implement-task` (consumer)
- **`plugins/sdlc-workflow/shared/description-digest-protocol.md`** — cross-phase integrity protocol: `plan-feature` posts a SHA-256 digest of each task description, `implement-task` verifies it before implementation
- **`plugins/sdlc-workflow/shared/convention-applicability-rules.md`** — file-type applicability validation for conventions: `plan-feature` checks before enriching tasks, `verify-pr` checks before upgrading suggestions
- **`plugins/sdlc-workflow/skills/setup/*.template.md`** — templates for scaffolding:
  - `conventions.template.md` — CONVENTIONS.md scaffold
  - `constraints.template.md` — constraints document scaffold
  - `project-config.template.md` — Project Configuration section scaffold
- **Skill patterns**: When creating new skills, follow the structure of existing skills (e.g., `implement-task/SKILL.md`, `plan-feature/SKILL.md`) — each has clear step-by-step instructions, guardrails, and important rules sections

## Documentation

- **`README.md`** (root) — project overview, installation instructions, plugin catalog; update when:
  - New skills are added
  - Installation steps change
  - Project description changes
- **`docs/`** directory — comprehensive documentation:
  - `methodology.md` — core principles and SDLC phases
  - `workflow.md` — execution workflow
  - `tools.md` — MCP server catalog
  - `conventions-spec.md` — workflow conventions
  - `constraints.md` — deterministic rules (update when skill behavior rules change)
  - `project-config-contract.md` — CLAUDE.md configuration contract
  - `metrics.md` — workflow metrics
  - `releasing.md` — release process
- **`CHANGELOG.md`** — release history; update with every version bump
- **`SKILL.md`** files — skill-specific instructions; update when skill behavior changes
- **Format**: All documentation uses Markdown (GitHub-flavored)
- **Triggers for doc updates**:
  - New skills added → update `README.md`, add skill to documentation index
  - Skill behavior changes → update corresponding `SKILL.md` and `docs/constraints.md`
  - Configuration contract changes → update `docs/project-config-contract.md`
  - Release process changes → update `docs/releasing.md`

## Dependencies

- **No external dependencies** — this repository contains only documentation and configuration files
- **Runtime dependency**: Claude Code CLI (users must have Claude Code installed to use the plugins)
- **Plugin system**: Uses Claude Code's plugin marketplace and validation system (`claude plugin validate`)
- **Version synchronization**: The plugin version must be kept in sync between:
  - `.claude-plugin/marketplace.json` (required for update detection)
  - `plugins/sdlc-workflow/.claude-plugin/plugin.json` (required by CI validation)
