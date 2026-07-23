# Eval PR Fork Dispatch

**Date**: 2026-05-07
**Scope**: Secure eval execution for fork PRs via `workflow_run` dispatch
**Relates to**: [Eval Skills CI Workflow](2026-04-21-eval-skills-ci-workflow-design.md)

## Problem

The `eval-pr.yml` workflow requires repository secrets (`GCP_SA_KEY`, `CLOUD_ML_REGION`) to authenticate to Google Cloud for running Claude Code via Vertex AI. GitHub does not pass secrets to workflows triggered from forked repositories:

> "With the exception of `GITHUB_TOKEN`, secrets are not passed to the runner when a workflow is triggered from a forked repository."
> — [Using secrets in GitHub Actions](https://docs.github.com/en/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions)

This means fork PRs that modify skills or evals cannot produce eval results.

## Solution

Split `eval-pr.yml` into two workflows using the `workflow_run` event, which runs in the base repository context with full secret access:

> "The workflow started by the `workflow_run` event is able to access secrets and write tokens, even if the previous workflow was not."
> — [Events that trigger workflows: workflow_run](https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs/events-that-trigger-workflows#workflow_run)

A trust check auto-approves eval runs for repository collaborators with write access, while external contributors require manual approval via a GitHub protected environment.

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Dispatch mechanism | `workflow_run` | Only mechanism that works for fork PRs — `workflow_dispatch`/`repository_dispatch` require write tokens that fork PR `GITHUB_TOKEN` lacks |
| Trust signal | Collaborator permission API | `GET /repos/{owner}/{repo}/collaborators/{username}/permission` — uses GitHub's actual permission model, handles teams automatically, no file parsing |
| Trust threshold | `admin` or `write` | Collaborators with write access can already push to the repo directly — granting them secret access in CI adds no new attack surface |
| Untrusted gate | Protected environment | GitHub's built-in approval mechanism — reviewers click "Approve" in the Actions UI |
| PR coverage | All PRs (fork and non-fork) | Single code path avoids duplicate logic and ensures consistent behavior |
| Data flow | No artifact — Stage 2 derives everything | Artifact is attacker-controlled (fork PR can modify Stage 1 workflow). Stage 2 derives PR identity from GitHub API and skills from `pulls.listFiles` (no checkout needed) |
| Skill discovery | `pulls.listFiles` API (no checkout) | Eliminates fork code checkout in the discover job entirely — no `allow-unsafe-pr-checkout` needed for discovery |
| Workspace isolation | Base branch at root, PR in subdirectory | Workspace root is trusted (CLAUDE.md, .claude/ config). PR code in `pr-head/` via `--add-dir`. Requires `allow-unsafe-pr-checkout: true` for the subdirectory checkout |
| Credential isolation | `sandbox.credentials.envVars` deny mode | GCP/Vertex AI env vars stripped from sandboxed Bash subprocesses. Claude Code runtime retains access for API auth. Belt-and-suspenders: `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB=1` |

## Architecture

```
Fork PR opened
    │
    ▼
┌──────────────────────────────┐
│  eval-pr.yml (pull_request)  │  Path-filtered gate only
│  No work — just triggers     │
│  workflow_run on completion  │
└──────────────┬───────────────┘
               │ workflow_run (completed)
               ▼
┌──────────────────────────────────────┐
│  eval-pr-run.yml (workflow_run)      │  Base repo context — secrets available
│                                      │
│  Job 1: discover                     │
│  - Set pending commit status on PR   │
│  - Resolve PR identity via GitHub API│
│  - Discover skills via pulls.listFiles│
│  - Check collaborator permission     │
│  - Update status if awaiting approval│
│  - Output: trusted, skills, PR#      │
│  (No checkout — pure API discovery)  │
│                                      │
│  Job 2: gate                         │
│  - Runs ONLY if trusted != true      │
│  - environment: eval-protected       │
│  - Blocks until reviewer approves    │
│                                      │
│  Job 3: run-evals                    │
│  - Checkout base branch (workspace   │
│    root = trusted CLAUDE.md)         │
│  - Checkout PR into pr-head/         │
│  - Install bubblewrap + socat        │
│  - Authenticate GCP                  │
│  - Run evals (sandbox + --add-dir)   │
│  - Post PR review                    │
│                                      │
│  Job 4: report-status                │
│  - Set final commit status (pass/fail)│
└──────────────────────────────────────┘
```

## Workflow 1: eval-pr.yml (modified)

### Changes from Current

The workflow is reduced to a minimal path-filtered trigger. All logic is removed — no checkout, no discovery, no artifact. Its sole purpose is to act as a gate: GitHub's path filter ensures it only runs when skill or eval files change, and its completion triggers Stage 2 via `workflow_run`.

### Trigger

Unchanged:

```yaml
on:
  pull_request:
    branches: [main]
    paths:
      - 'plugins/sdlc-workflow/skills/**/*.md'
      - 'evals/**/evals.json'
      - '.github/workflows/eval-pr.yml'
```

### Steps

Single no-op step. The workflow just needs to complete successfully to trigger Stage 2.

## Workflow 2: eval-pr-run.yml (new)

### Trigger

```yaml
on:
  workflow_run:
    workflows: ["Eval PR"]
    types: [completed]
```

No path filtering — `workflow_run` does not support it. The `completed` type fires on both success and failure, so the `discover` job checks `github.event.workflow_run.conclusion == 'success'` before proceeding.

### Permissions

```yaml
permissions:
  contents: read
  pull-requests: write
```

### Job 1: discover

Resolves PR identity from the GitHub API, discovers changed skills via `pulls.listFiles`, and determines trust level. Skips early if the triggering workflow failed. No data from the triggering workflow is used — everything is derived independently. **No checkout is performed in this job.**

**Steps:**

1. **Resolve PR identity and check trust** via `actions/github-script@v9`:
   - Find PR via `pulls.list` filtered by `base: 'main'`, matched by `head.sha == workflow_run.head_sha`
   - Check collaborator permission level for the PR author
   - Output `pr_number`, `author`, `trusted`

Note: `listPullRequestsAssociatedWithCommit` does not work for fork PRs because the commit lives in the fork's repository, not the base repo's commit graph. `pulls.list` with SHA matching is the reliable alternative.

```javascript
const headSha = context.payload.workflow_run.head_sha;
const prs = await github.paginate(github.rest.pulls.list, {
  owner: context.repo.owner, repo: context.repo.repo,
  state: 'open', base: 'main', per_page: 100
});
const pr = prs.find(p => p.head.sha === headSha);
const { data } = await github.rest.repos.getCollaboratorPermissionLevel({
  owner: context.repo.owner, repo: context.repo.repo, username: pr.user.login
});
const trusted = ['admin', 'write'].includes(data.permission);
```

2. **Discover changed skills** via `actions/github-script@v9` — uses `pulls.listFiles` to get changed filenames, matches against skill/eval path patterns, confirms `evals/<skill>/evals.json` exists via the file list or `repos.getContent`. No checkout needed.

3. **Set outputs**: `skills`, `pr_number`, `author`, `trusted`

### Job 2: gate

```yaml
gate:
  needs: discover
  if: >-
    needs.discover.result == 'success' &&
    needs.discover.outputs.trusted != 'true' &&
    needs.discover.outputs.skills != ''
  runs-on: ubuntu-latest
  environment: eval-protected
  steps:
    - run: echo "Approved by reviewer"
```

Skipped entirely for trusted authors and when there are no skills to evaluate. For untrusted authors, the job is created but paused until a designated reviewer approves it in the Actions UI.

### Job 3: run-evals

```yaml
run-evals:
  needs: [discover, gate]
  if: >-
    !cancelled() &&
    needs.discover.result == 'success' &&
    needs.discover.outputs.skills != '' &&
    (needs.discover.outputs.trusted == 'true' || needs.gate.result == 'success')
  runs-on: ubuntu-latest
```

**Steps:**

1. **Checkout base branch** — `actions/checkout@v7` with no `ref:` (defaults to the base branch). This establishes a trusted workspace root with the repository's CLAUDE.md and `.claude/` configuration.

2. **Checkout PR merge commit into subdirectory** — `actions/checkout@v7` with `ref: refs/pull/<pr_number>/merge`, `path: pr-head`, and `allow-unsafe-pr-checkout: true`. The `allow-unsafe-pr-checkout` flag is required because `actions/checkout@v7` blocks fork PR refs in `workflow_run` workflows regardless of the `path:` parameter ([GitHub Changelog, June 2026](https://github.blog/changelog/2026-06-18-safer-pull_request_target-defaults-for-github-actions-checkout/)).

3. **Install sandbox dependencies** — `bubblewrap` and `socat` via `apt-get`. Required by `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB=1` on Linux runners.

4. **Authenticate to Google Cloud** via Workload Identity Federation:

```yaml
- uses: google-github-actions/auth@v3
  with:
    project_id: ${{ secrets.GCP_PROJECT_ID }}
    workload_identity_provider: ${{ secrets.GCP_WIF_PROVIDER }}
```

5. **Install Claude Code**

6. **Write sandbox settings** — generates `/tmp/eval-sandbox-settings.json` with `sandbox.credentials.envVars` deny entries for GCP/Vertex AI env vars (see [Credential Isolation](#credential-isolation) below).

7. **Run PR evals** — invokes `claude -p` with `--settings /tmp/eval-sandbox-settings.json --add-dir pr-head` and `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB=1`. Eval paths reference `pr-head/evals/<skill>/evals.json`.

8. **Post eval results review** — reads `summary.md` from eval workspaces and posts as a PR review via `pulls.createReview`. Uses `needs.discover.outputs.pr_number`.

### Job 4: report-status

Sets a final commit status on the PR's head SHA via the Commit Status API. Runs unconditionally (`always()`) after all other jobs complete so a pending status is never left unresolved — including when the discover job itself fails.

This is necessary because `workflow_run` workflows run in the default branch context and don't appear as status checks on the PR page. Without explicit commit statuses, PR authors and reviewers have no visibility that evals are pending, waiting for approval, running, or complete.

Status transitions:
- **pending** — set immediately when the discover job starts ("Eval run in progress...")
- **pending** — updated if the author is untrusted ("Waiting for approval in eval-protected environment")
- **success** — eval run completed, results posted as PR review
- **failure** — discover failed (could not resolve PR context), approval rejected, or eval run failed

All statuses use the same `context: 'Eval PR Run'` so GitHub updates the existing status rather than creating duplicates.

## Trust Model

### Trusted Authors (auto-approve)

Repository collaborators with `write` or `admin` permission. Determined by the GitHub REST API:

```
GET /repos/{owner}/{repo}/collaborators/{username}/permission
```

This returns the highest permission level across all grant sources (direct, teams, org, enterprise). Collaborators with write access can already push directly to the repository, so granting them secret access in CI adds no new attack surface.

### Untrusted Authors (manual approval)

All other PR authors. Their eval runs require a reviewer to click "Approve" in the GitHub Actions UI. The protected environment `eval-protected` enforces this gate.

### Security Properties

- The `workflow_run` workflow executes on the base repository's default branch — a fork PR cannot modify the workflow definition or trust logic
- No data passes from Stage 1 to Stage 2 — there is no artifact. Stage 2 derives everything independently: PR identity from the GitHub API, skills from `pulls.listFiles`. This eliminates artifact poisoning as an attack vector entirely
- The discover job performs no checkout — skill discovery uses only GitHub API calls, so no fork code is fetched in the discovery phase
- The collaborator permission check uses GitHub's API, not a file in the repo — it cannot be manipulated by a PR
- The workspace root is the trusted base branch (CLAUDE.md, `.claude/` config). Fork PR code is isolated in the `pr-head/` subdirectory via `--add-dir`
- GCP/Vertex AI credential env vars are stripped from sandboxed Bash subprocesses via `sandbox.credentials.envVars` deny mode. Claude Code's own runtime retains access for API authentication
- `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB=1` provides blanket scrubbing of Anthropic, cloud, and GitHub Actions secrets from all subprocesses as belt-and-suspenders
- The `dontAsk` permission mode with explicit `--allowedTools` limits Claude Code's capabilities
- Once approved, the workflow does execute skill files from the PR — this is inherent to the use case (evaluating skills requires running them). The credential isolation mitigates but does not eliminate prompt injection risk

### Credential Isolation

The run-evals job uses two layers of credential protection:

1. **`sandbox.credentials.envVars`** (deny mode) — declaratively strips specific env vars from sandboxed Bash subprocesses. The deny list covers all env vars set by `google-github-actions/auth@v3` in WIF mode and the workflow's own secret-derived env vars:
   - `ANTHROPIC_VERTEX_PROJECT_ID`, `CLOUD_ML_REGION`
   - `GOOGLE_APPLICATION_CREDENTIALS`, `CLOUDSDK_AUTH_CREDENTIAL_FILE_OVERRIDE`, `GOOGLE_GHA_CREDS_PATH`
   - `CLOUDSDK_PROJECT`, `CLOUDSDK_CORE_PROJECT`, `GCP_PROJECT`, `GCLOUD_PROJECT`, `GOOGLE_CLOUD_PROJECT`

2. **`CLAUDE_CODE_SUBPROCESS_ENV_SCRUB=1`** — blanket best-effort scrub of Anthropic, cloud, and GitHub Actions secrets from subprocess environments. Requires `bubblewrap` and `socat` on Linux runners.

Both layers are independent — the deny list targets specific known vars, the env scrub catches patterns. See [Claude Code Sandboxing: Protect credentials](https://code.claude.com/docs/en/sandboxing#protect-credentials) for full documentation.

### Why Not Other Approaches

| Approach | Why not |
|----------|---------|
| `workflow_dispatch` / `repository_dispatch` | Cannot be triggered from fork PR workflows — `GITHUB_TOKEN` is read-only for fork PRs |
| `pull_request_target` | Runs in base repo context with secrets, but GitHub warns: "Avoid using this event if you need to build or run code from the pull request" |
| CODEOWNERS parsing | Text file parsing is fragile (teams, globs, multiple entries); collaborator API is authoritative |
| Skip evals for fork PRs | Fork contributors would never see eval results |

## Setup Requirements

### GitHub Environment

Create a protected environment in the repository:

1. Settings > Environments > New environment: `eval-protected`
2. Add required reviewers (at minimum, repository maintainers)
3. No environment-specific secrets needed — existing repository-level secrets (`GCP_PROJECT_ID`, `GCP_WIF_PROVIDER`, `GCP_CLOUD_ML_REGION`) are available to all `workflow_run` jobs

### Runner Dependencies

The sandbox credential isolation requires `bubblewrap` and `socat` on Linux runners. These are installed by the workflow via `apt-get` before Claude Code runs.

### No Other Infrastructure

- No CODEOWNERS file needed
- No GitHub App or PAT required
- No changes to `eval-baseline.yml` (runs on push to main, secrets always available)

## File Changes

| File | Change |
|------|--------|
| `.github/workflows/eval-pr.yml` | Reduce to minimal path-filtered trigger (no discovery, no artifact) |
| `.github/workflows/eval-pr-run.yml` | New workflow: trust check, gate, eval execution, review posting |
| `docs/specs/2026-04-21-eval-skills-ci-workflow-design.md` | Add reference to this spec |

## References

- [Using secrets in GitHub Actions](https://docs.github.com/en/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions) — fork PR secret restriction
- [Events that trigger workflows: workflow_run](https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs/events-that-trigger-workflows#workflow_run) — secret access in `workflow_run`
- [GitHub Security Lab: Preventing pwn requests](https://securitylab.github.com/resources/github-actions-preventing-pwn-requests/) — two-stage pattern for fork PR processing
- [GitHub Security Lab: New patterns and mitigations](https://securitylab.github.com/resources/github-actions-new-patterns-and-mitigations/) — `workflow_run` security mitigations
- [GitHub Changelog: Safer pull_request_target defaults](https://github.blog/changelog/2026-06-18-safer-pull_request_target-defaults-for-github-actions-checkout/) — `actions/checkout@v7` fork guard and backport to supported major versions
- [Claude Code Sandboxing: Protect credentials](https://code.claude.com/docs/en/sandboxing#protect-credentials) — `sandbox.credentials.envVars` deny/mask modes
- [claude-code-action security: Fork PRs](https://github.com/anthropics/claude-code-action/blob/main/docs/security.md) — safe fork PR patterns with `--add-dir`
- [Repository collaborators API](https://docs.github.com/en/rest/collaborators/collaborators) — permission check endpoint
