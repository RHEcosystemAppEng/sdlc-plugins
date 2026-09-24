# Running sdlc-workflow skills with fullsend

Run sdlc-workflow skills inside secure sandboxes via
[fullsend](https://github.com/fullsend-ai/fullsend). The agent runs in an
isolated container with least-privilege network and filesystem policies, while
all issue-tracker and GitHub writes happen on the trusted runner — never inside
the sandbox.

This guide documents the **native CLI path**: a standalone root-level
harness, the stock digest-pinned `fullsend-code` image, a single pinned-URL
registration, and the plugin referenced in place with zero duplication. The only
skill wired up today is `verify-pr`, which runs both on demand (`fullsend run`,
locally or in CI) and automatically on every pull request via a CI-gated
dispatch (see **CI deployment**).

## How it works

The setup has three moving parts, all in this repo:

- **`harness/verify-pr.yaml`** (repo root) — a **standalone harness** with no
  base composition. Placed at the repo root so that, when fullsend is invoked
  with `--fullsend-dir` = repo root, its relative children resolve against the
  repo root: `plugins/sdlc-workflow` is delivered **in place as a whole plugin**
  and its sibling `shared/` resources resolve intact. It pins the stock
  `fullsend-code` image by digest and declares the policy, provider, profile,
  env mount, pre/post scripts, and validation loop.
- **`.fullsend/config.yaml`** — registers a single agent, `verify-pr`, whose
  source is the **local composing child** `.fullsend/harness/verify-pr.yaml`.
- **`.fullsend/harness/verify-pr.yaml`** — the local composing child. It pins
  the root harness by **raw URL at a commit SHA plus a `#sha256=`** on its
  `base:` line, and adds the runner-local *absolute* mounts (GCP credential,
  OIDC token, pre-script output) that fullsend v0.37.0 refuses to inherit from a
  URL-sourced base. `host_files` are concatenated base + child (dedup by dest,
  child wins).

Because the base is pinned to one commit SHA, **every relative child of the
harness** — the pre/post scripts, schemas, agent prompt, policy, provider,
profile, and the whole `plugins/sdlc-workflow` directory — resolves at that same
SHA. The single `#sha256=` on the `base:` line verifies the base file itself;
`.fullsend/lock.yaml` then freezes the content hash of every transitively
resolved child. One pinned URL, one integrity anchor, everything else covered
transitively.

There is **no custom image and no marketplace baking**. fullsend fabricates the
Claude Code marketplace cache from the in-place `plugins:` entry at runtime, so
the Claude Code marketplace structure is unchanged and the same plugin files
serve interactive Claude Code users and fullsend runs with zero duplication.

### Split-trust I/O

The Jira and GitHub tokens live **only on the runner**. The pre_script prefetches
everything the agent needs (the Jira issue and a GitHub read bundle) and the
post_script performs every write after the sandbox is destroyed. The sandbox
itself receives read-only context only — `JIRA_BASE_URL` (display links) — plus
the prefetched read bundle mounted read-only. The Jira key is not passed as an
env var: the pre_script derives it from the triggering PR URL and records it as
`task_id` inside `verify-pr-input.json`, which the agent reads. The **only**
credential that ever enters the sandbox is the Vertex AI service-account key,
because model inference runs in-sandbox (see below).

## Credential delivery and tiers

Credentials use the highest isolation tier possible. Two of the three services
never place a credential in the sandbox at all.

| Service | Tier | Credential in sandbox? | How it is delivered |
|---|---|---|---|
| **Jira** | 1 | No | The pre_script prefetches the issue on the runner; the post_script posts comments with `fullsend issues post-comment --tracker jira`. The token stays in runner env only. |
| **GitHub** | 1 | No | The pre_script prefetches the read bundle (`gh pr diff` / `gh pr view` → diff, diffstat, reviews, comments, commits), the head-SHA **CI check-run outcomes** (`github.check_runs` — name/status/conclusion/details_url), and the **concatenated `--log-failed` output of every failed check-run** (written to `check-run-logs.txt`, mounted separately; only its path rides in the bundle so the large log text stays off the agent's context until Correctness Check 1b reads it on a FAIL), and records the PR head ref name and head commit SHA in it; the post_script writes via `fullsend issues post-comment --tracker github` and `gh` (PR reviews/replies via `gh api`). The token stays in runner env only. The PR-head working tree is the `--target-repo` clone, checked out at the head SHA before the run (see below) — the pre_script does not check out. |
| **Vertex AI** | 4 (fullsend-mandated) | **Yes** | The in-sandbox runtime does the model inference and reads `GOOGLE_APPLICATION_CREDENTIALS` from a file (`/tmp/.gcp-credentials.json`). Vertex auth requires local JWT signing, so tier 4 (file on the sandbox filesystem) is unavoidable. This is the one credential set in the sandbox. |

Because Vertex is the only in-sandbox credential, the sandbox's **only network
egress is `*.googleapis.com`** (declared in
`plugins/sdlc-workflow/profiles/fullsend-vertex-ai.yaml`). There is no
atlassian, github, or anthropic egress from the sandbox — those are all handled
on the runner.

> GitHub is a **tier-1** service — it needs no OpenShell provider. There is no
> Jira provider and no `github-ro` provider. The only provider is
> `plugins/sdlc-workflow/providers/vertex-ai.yaml`, which selects the Vertex
> egress profile (its credential still arrives via the host-file mount, not a
> proxied placeholder).

## Prerequisites

- [fullsend](https://github.com/fullsend-ai/fullsend) CLI installed (CI pins
  **v0.43.0** — see **Bumping the fullsend version**; a local run needs a
  compatible release).
- An OpenShell gateway running — fullsend uses OpenShell as its sandbox runtime.
- GCP credentials for Vertex AI — a service-account key JSON (local) or a WIF
  external-account config (CI). Referenced by `GOOGLE_APPLICATION_CREDENTIALS`.
- A Jira API token and a GitHub token — used by the pre/post scripts on the
  runner only.
- The Python `jsonschema[format]` package on the runner — the `validation_loop`
  validates agent output against the JSON schema before the post_script runs, and
  the triage-security pre-script enforces URI and date-time schema formats
  (`pip install 'jsonschema[format]'`).

## Running verify-pr

The command is **identical locally and in CI** — same harness, same registration,
only the runtime environment differs (a local SA key vs. a CI WIF config; a CI
run additionally supplies an OIDC token file):

```bash
fullsend run verify-pr \
  --fullsend-dir .fullsend \
  --target-repo /tmp/my-repo-clone \
  --env-file secrets.env \
  --env-file <(echo "FULLSEND_WORK_ITEM_URL=https://github.com/RHEcosystemAppEng/sdlc-plugins/pull/1234")
```

The Jira key is **not** an input — the pre_script resolves it from the triggering
PR URL (`FULLSEND_WORK_ITEM_URL`) by a JQL search on the Git Pull Request custom
field, gates it (status Review + the `ai-generated-jira` label), and records the
resolved key as `task_id` in `verify-pr-input.json`. In CI, `harness-run` exports
`FULLSEND_WORK_ITEM_URL`; a local run must export the same PR URL.

`--target-repo` must be a **disposable clone**, not your working directory —
fullsend deletes and re-creates it after each run. It must already be **checked
out at the PR head** (`github.commit_sha` from the read bundle): neither the
pre_script nor the harness performs the checkout, so the caller establishes the
PR-head working tree. Locally, `gh pr checkout <pr-number>` in the clone before
the run; in CI, the checkout step fetches the PR head. The sandbox then inspects
that tree directly (there is no `gh` CLI in the sandbox).

A minimal `secrets.env` (never commit it):

```bash
# Vertex AI (tier 4 — the only credential that enters the sandbox)
ANTHROPIC_VERTEX_PROJECT_ID=my-project
GOOGLE_CLOUD_PROJECT=my-project
CLOUD_ML_REGION=global
GOOGLE_APPLICATION_CREDENTIALS=/path/to/sa-key.json
# Jira (tier 1 — runner only)
JIRA_SERVER_URL=https://myorg.atlassian.net
JIRA_EMAIL=me@example.com
JIRA_API_TOKEN=my-jira-token
JIRA_PROJECT_KEY=TC
# GitHub (tier 1 — runner only)
GH_TOKEN=my-github-token
```

## CI deployment (per-repo GitHub App)

The same pinned harness that runs locally is dispatched automatically in CI, once
per pull request, after the PR's other checks finish. Three one-time provisioning
steps stand this up (day-0, run by a repo/org admin); the recurring run then needs
no manual step.

### Installation

1. **`fullsend github setup`** — provisions the per-repo installation. It writes
   the two-layer config (`.fullsend/config.base.yaml`, the vendor preset base
   layer, and `.fullsend/config.yaml`, the repo overlay) and installs the vendor
   shim workflow `.github/workflows/fullsend.yaml`. `install_mode: per-repo`
   throughout. **verify-pr is registered only in `config.base.yaml`**, never in
   `config.yaml`: the shim greps `config.yaml` alone for agents, so it never
   dispatches verify-pr, while `fullsend dispatch` / `fullsend run` still resolve
   it because `LoadConfig` merges `config.yaml` over `config.base.yaml` (ADR 0069).
2. **`fullsend inference provision`** — provisions hosted Vertex AI via Workload
   Identity Federation and records the result as the inference override in
   `.fullsend/config.yaml`:
   ```yaml
   inference:
     project: it-gcp-tpa
     wif_provider: projects/442181572212/locations/global/workloadIdentityPools/fullsend-inference/providers/gh-rhecosystemappeng-sdlc-plugin
   ```
   In CI the WIF provider mints a short-lived Vertex credential per run — no
   long-lived key is stored (contrast the local run, which uses an SA key file).
3. **Org GitHub App install** — install the fullsend GitHub App on the org/repo
   with the **review** role. The App mints the review-role token via OIDC at
   dispatch time (the `mint_url` input) for the PR review/report writes. This is an
   org-admin action in GitHub, not a CLI step.

The recurring dispatch is a dedicated workflow,
`.github/workflows/fullsend-verify-pr.yml` (not the vendor shim) — see
**Dispatch design** below.

### Dispatch design

verify-pr must run **after** a PR's other CI finishes, so it can treat CI results
as input data — never as a gate (it runs whether CI passed or failed). fullsend
has no CI-completion event to trigger on, which drives the design:

- There is **no `check_suite` / `check_run` / `workflow_run` TransitionKind** in
  fullsend, and GitHub's recursion guard suppresses `check_suite` / `check_run`
  for suites created by Actions. A CI-completion-triggered dispatch is therefore
  not reliably deliverable.
- The workaround is an **inline `pull_request_target` wait**:
  `fullsend-verify-pr.yml` triggers on `pull_request_target` (`opened`,
  `synchronize`, `reopened`, `labeled`) and its `wait-for-checks` job blocks on
  [`lewagon/wait-on-check-action`](https://github.com/lewagon/wait-on-check-action)
  (pinned by SHA) until every *other* check on the PR head reaches a terminal
  state. Only then does the `verify-pr` job dispatch. This inline wait is the only
  reliable "run after CI" trigger (TC-6180 NFRs). The trigger is
  `pull_request_target` (not `pull_request`) so **fork-origin PRs** get the
  upstream vars/secrets/OIDC the mint step needs — see **Fork PRs** below.
- **CI result is data, not a gate.** `allowed-conclusions` lists *all* terminal
  conclusions (`success`, `failure`, `neutral`, `cancelled`, `skipped`,
  `timed_out`, `action_required`, `stale`, `startup_failure`), so a failing check
  still releases the wait and verify-pr still runs and reports (recording
  `CI Status = FAIL`).
  `fail-on-no-checks: false` lets a PR with no other checks proceed;
  `timeout-minutes: 45` bounds a hung check (the dispatch is then skipped).
- One in-flight run per PR: a `concurrency` group keyed on the PR number with
  `cancel-in-progress: true` supersedes a stale run on a new push.

The dispatch job hands a pre-built single-entry matrix (agent `verify-pr`, role
`review`) to the vendor reusable workflow
`fullsend-ai/fullsend/.github/workflows/reusable-dispatch.yml@v0`, whose
`harness-run` job mints the review-role App token via OIDC and runs `fullsend run`.

This `pull_request_target` trigger is the CI-side equivalent of the harness's own
**CEL trigger**, which drives the `fullsend dispatch` path. The trigger is declared on
the composing child `.fullsend/harness/verify-pr.yaml`:

```
event.entity.kind == "change_proposal" &&
event.transition.kind in ["synchronized", "opened", "reopened"]
```

It **must** live on the child, not only on the base: `mergeBaseIntoChild`
(`internal/harness/compose.go`) carries `role` and other scalars from base→child
but intentionally does **not** carry `trigger`, so a trigger set only on the base
is inert (ADR 0061).

Before the agent runs, the **pre_script gates on Jira** (see **Running
verify-pr**): it resolves the Jira key from the PR URL by a JQL search on the Git
Pull Request custom field and proceeds only when the issue is status `Review` with
the `ai-generated-jira` label (ADR 0072 skip otherwise). This scopes automated
review to sdlc-workflow-tracked PRs.

#### Fork PRs (`pull_request_target` + `ok-to-test`)

The workflow triggers on **`pull_request_target`**, not `pull_request` (TC-6331).
A `pull_request` run whose head branch lives on a **fork** gets no repo
vars/secrets and no OIDC (`id-token`), so `vars.FULLSEND_MINT_URL` resolves empty
and the mint step fails (`FULLSEND_MINT_URL is not set`). `pull_request_target`
runs the **base-branch** version of the workflow with full access to upstream
vars/secrets/OIDC, so a fork PR can dispatch (fullsend **ADR-0009**).

This is only safe because the workflow **never checks out or executes fork code**.
It builds the dispatch matrix from `github.event` alone (`GITHUB_EVENT_PATH`, via
`jq --argjson` — no shell interpolation of PR-controlled strings) and hands off to
`reusable-dispatch.yml`, which does its own checkout/mint in base-repo context.
That closes the classic `pull_request_target` "pwn request" credential-exfiltration
hole.

Defense-in-depth is an **`ok-to-test` maintainer-label gate**, modelled on
fullsend's `docs/guides/dev/e2e-testing.md`:

- **Same-repo (upstream) PRs** need no label — they already carry secrets/OIDC —
  and run on `opened` / `synchronize` / `reopened`.
- **Fork PRs** dispatch **only** when a maintainer applies the `ok-to-test` label
  (the `labeled` trigger). A maintainer reviews the fork's code first, then labels.
- The `remove-ok-to-test` job strips the label on every new push (`synchronize`)
  to a fork PR, so new commits force re-review before the label — and thus another
  verify-pr run — can be re-applied.

There is **no longer an "upstream head branch required" constraint**: fork
contributors open PRs normally, and a maintainer gates each run with the label.

### Variables and secrets (day-2 management)

CI configuration is split between GitHub Actions **variables** (non-secret,
`vars.*`) and **secrets** (`secrets.*`), all consumed by
`.github/workflows/fullsend-verify-pr.yml`. To change any value, edit it under the
repo's **Settings → Secrets and variables → Actions** (or with `gh variable set` /
`gh secret set`) — no code change is needed, and the next dispatch picks it up.

| Name | Kind | Purpose | Update when |
|---|---|---|---|
| `JIRA_EMAIL` | secret | Jira Service Account email for the tier-1 Basic-auth credential (mapped to vendor input `JIRA_USER_EMAIL`); authors the report comment. | Changing the Jira Service Account. |
| `JIRA_API_TOKEN` | secret | Jira scoped API token for the same account (mapped to `JIRA_TOKEN`). | Rotating the SA token (tokens expire / are revoked). |
| `JIRA_BASE_URL` | variable | Jira site URL for display links inside the sandbox. | Jira site moves. |
| `FULLSEND_GCP_WIF_PROVIDER` | secret | Vertex Workload Identity Federation provider resource. | Re-provisioning inference (`fullsend inference provision`). |
| `FULLSEND_GCP_PROJECT_ID` | secret | GCP project hosting Vertex inference. | GCP project changes. |
| `FULLSEND_MINT_URL` | variable | OIDC mint endpoint for the review-role App token. | App / mint endpoint changes. |
| `FULLSEND_GCP_REGION` | variable | Vertex region. | Region changes. |
| `FULLSEND_PROJECT_NUMBER` | variable | GCP project number for OIDC. | GCP project changes. |
| `OTEL_EXPORTER_OTLP_HEADERS`, `OTEL_EXPORTER_OTLP_TRACES_HEADERS` | secret | OpenTelemetry export auth headers (optional observability). | Rotating the OTLP endpoint credential. |

The Jira credential is a dedicated **Service Account** — email + scoped token,
Basic auth (fullsend's Jira tracker is Basic-auth only). It is a **tier-1**
credential: it stays in runner env and never enters the sandbox (see **Credential
delivery and tiers**). To rotate it, issue a new scoped token for the SA and
update `JIRA_API_TOKEN` (and `JIRA_EMAIL` if the account itself changes); the next
dispatch authenticates the post_script Jira comment with the new value. The same
pattern applies to every row above — update the value in repo settings, no code
change.

## Releasing an update (this repo)

The `.fullsend/` registration pins content by commit SHA, so **editing a file is
not enough** — you must re-pin and re-lock in the same change. The full loop:

1. **Edit** the harness (`harness/verify-pr.yaml`) and/or any pinned plugin file
   under `plugins/sdlc-workflow/` (see the re-pin rule below).
2. **Commit and push** to `RHEcosystemAppEng`. `main` is the release channel;
   during feature work, push to the feature branch and merge to `main`.
3. **Re-pin** the `base:` line in `.fullsend/harness/verify-pr.yaml`: set the
   commit SHA to the new commit and the `#sha256=` to the base file's hash:
   ```bash
   shasum -a 256 harness/verify-pr.yaml
   ```
4. **Re-lock** so every transitive child is re-resolved at the new SHA:
   ```bash
   fullsend lock verify-pr --fullsend-dir .fullsend
   ```
   `fullsend lock --all --fullsend-dir .fullsend` locks every harness at once —
   equivalent here since `verify-pr` is the only one (TC-5813 used `--all`).
5. **Commit `.fullsend/`** (the updated `lock.yaml` and re-pinned child) in the
   same PR as the content edit.

> **`fullsend agent update` does not apply to this repo.** The registered
> `verify-pr` agent is a *local path* (`source: harness/verify-pr.yaml`), so
> `fullsend agent update verify-pr` fails with *"agent 'verify-pr' is a local
> path — nothing to update"*. `agent update` re-pins **URL** agents only — it is
> for adopters (below), not for the self-hosted `.fullsend/` model. Here you
> re-pin by editing the `base:` SHA/hash and re-locking.

### Bumping the fullsend version

The CI dispatch pins the fullsend CLI to a released tag so it does not float
(the vendor default floats to `job.workflow_sha`). The pin lives in
`.github/workflows/fullsend-verify-pr.yml`:

```yaml
      fullsend_version: "v0.43.0"
```

The current pin is **v0.43.0** — bumped from v0.37.0 because v0.37.0's bundled
OpenShell never reached sandbox readiness (`not ready after 2m0s` → `Failed to
create sandbox`). To bump:

1. Set `fullsend_version` to the new released tag (v-prefixed, matching the
   vendor's git tags).
2. **Re-validate end to end**: open a throwaway qualifying PR and confirm the
   dispatch reaches sandbox readiness and posts a report (an OpenShell/runtime
   regression surfaces as `Failed to create sandbox`). Only merge once a live run
   passes.
3. Update the local `## Prerequisites` version note to match if the local CLI
   must track CI.

The fullsend CLI version is independent of both the harness `base:` re-pin and the
plugin version below.

### Keeping the two plugin-version files in sync

The plugin/skill version is stored in **two** files that must always match:

- `plugins/sdlc-workflow/.claude-plugin/plugin.json` — the plugin manifest
  (required by CI validation).
- `.claude-plugin/marketplace.json` — the marketplace registry (required for
  relative-path plugins).

When releasing a skill/plugin change, bump **both** files in the same change (both
are currently `0.13.9`). This version bump is orthogonal to — but released
alongside — the `base:` re-pin + re-lock loop above: the re-pin/re-lock is what
makes the edited plugin content take effect at runtime, while the version bump is
the human-facing marker of that release.

### Constraints and gotchas

- **Merge with a merge commit — never squash or rebase.** The pinned raw URL in
  `.fullsend/` (and the adopter `fullsend agent add …/blob/main/…` URL) resolves
  to a specific commit SHA. A squash or rebase merge rewrites or drops that SHA,
  so the pin — and any adopter fetch — 404s. This applies at **every** merge hop
  up to `main`.
- **Re-pin + re-lock is mandatory after editing ANY pinned plugin file** —
  `SKILL.md`, scripts, schemas, sub-skill templates, `plugin.json`, and so on.
  Each such file is locked as a *member* of the `plugins[0]` directory dependency
  in `.fullsend/lock.yaml`. An edit that is not paired with a re-pin/re-lock is
  served **stale** at runtime: the pinned pre-edit content runs. Pair every
  content edit with edit → commit → push → re-pin `base:` → `fullsend lock …` →
  commit `.fullsend/` in the same PR.
- **Scope — what re-pinning does *not* affect.** The re-pin/re-lock loop governs
  only the `fullsend run` path (local + CI). Interactive / marketplace installs
  of the skill ignore `.fullsend/lock.yaml` entirely and use the plugin's
  working-tree copy — so a missed re-pin never affects interactive users, only
  fullsend runs.
- **Troubleshooting `cache integrity check failed`** at harness/lock load: caused
  by a stale `.fullsend/.fullsend-cache` (and the sibling root `./.fullsend-cache`).
  Fix:
  ```bash
  rm -rf .fullsend/.fullsend-cache .fullsend-cache
  ```
  then re-run online so the pinned content re-fetches.

## Adopting verify-pr (external fullsend users)

Other repos do not need to clone sdlc-plugins or copy any files. Register the
harness by URL — no SHA needed, fullsend resolves `main` HEAD and pins it for
you:

```bash
# 1. Register (one command, SHA-free — fullsend pins main HEAD)
fullsend agent add https://github.com/RHEcosystemAppEng/sdlc-plugins/blob/main/harness/verify-pr.yaml

# 2. Lock and run
fullsend lock verify-pr --fullsend-dir .fullsend
fullsend run verify-pr --fullsend-dir .fullsend --target-repo /tmp/clone --env-file secrets.env

# 3. Later, pull in a new release
fullsend agent update verify-pr --fullsend-dir .fullsend
```

`main` is the **release channel** — the URL above tracks it. There is no separate
`release` branch yet because `fullsend agent update` does not track a branch:
it re-pins to a commit SHA you resolve at update time, so a dedicated release
branch would add a maintenance hop without buying reproducibility that the SHA
pin does not already provide. The **merge-commit-only** rule above applies to
adopters too — a squash/rebase on any hop to `main` breaks the pinned URL the
adopter fetched.

## File inventory

All plugin paths are relative to `plugins/sdlc-workflow/`.

| File | Purpose |
|---|---|
| `harness/verify-pr.yaml` (repo root) | Standalone harness — stock digest-pinned image, in-place plugin, policy, provider, profile, env mount, pre/post scripts, validation loop, split-trust env. |
| `.fullsend/config.yaml` | Registers the `verify-pr` agent (local source) and the single allowed remote-resource prefix. |
| `.fullsend/harness/verify-pr.yaml` | Local composing child — pins the root harness by raw URL (`base:` + `#sha256=`) and adds the runner-local absolute mounts. |
| `.fullsend/lock.yaml` | Generated by `fullsend lock` — freezes every transitive dependency URL + SHA256. Do not edit by hand. |
| `agents/verify-pr.md` | Agent prompt (YAML frontmatter). fullsend launches Claude Code with this as the system prompt; it reads `task_id` from the pre-fetched `verify-pr-input.json` and invokes the skill. |
| `policies/verify-pr.yaml` | Sandbox network/filesystem policy. |
| `profiles/fullsend-vertex-ai.yaml` | OpenShell egress profile — `*.googleapis.com:443` only. |
| `providers/vertex-ai.yaml` | Selects the Vertex egress profile (no proxied credential). |
| `env/gcp-vertex.env` | Vertex env template, expanded from the secrets file (`expand: true`); points `GOOGLE_APPLICATION_CREDENTIALS` at `/tmp/.gcp-credentials.json`. |
| `schemas/verify-pr-result.schema.json` | JSON Schema for the agent's structured output; enforced by `validation_loop`. |
| `scripts/pre-verify-pr.sh` | Pre_script — validates inputs, prefetches the Jira issue and the GitHub read bundle, and records the PR head ref name + head commit SHA in the bundle (it does **not** check out — the PR-head working tree comes from `--target-repo`). Delegates to `pre_verify_pr.py`. |
| `scripts/post-verify-pr.sh` | Post_script — finds `agent-result.json` and delegates to `execute-actions.py`. Runs on the trusted runner after the sandbox is destroyed. |
| `scripts/execute-actions.py` | Action executor — posts Jira/GitHub sticky comments via `fullsend issues post-comment`, and PR reviews/replies via `gh api`. |
| `scripts/validate-output-schema.sh` + `strip_extra_properties.py` | Strips benign agent-added metadata, then validates against the schema. |

## Design decisions

### Why a standalone root-level harness

Placing the harness at the repo root lets fullsend resolve its relative children
against the repo root, so `plugins/sdlc-workflow` is delivered in place as a
whole plugin and its `shared/` resources resolve intact. No base composition
keeps the harness self-contained — the Go defaults already supply security
(`enabled: true`, `fail_mode: closed`) plus the sandbox hooks, so no explicit
`security:` block is needed.

### Why the plugin is referenced in place (no duplication)

fullsend fabricates the Claude Code marketplace cache from the `plugins:` entry
at runtime. The same plugin files back both interactive Claude Code installs and
fullsend runs, so there is no custom image, no Dockerfile, no bootstrap script,
and no second copy of the skills to keep in sync.

### Why Jira reads/writes use native fullsend CLI (not MCP) in the sandbox

MCP servers are not available inside the sandbox. All tracker and GitHub I/O is
handled on the runner: the pre_script prefetches with `gh` and the Jira REST
client, and the post_script posts sticky comments with
`fullsend issues post-comment`, which creates a marker-tagged comment on the
first run and edits it in place on re-runs (no comment flooding).

### Why the stock digest-pinned image

The harness pins `ghcr.io/fullsend-ai/fullsend-code` by `@sha256:` digest. The
stock image already carries Claude Code, `git`, the `gh` CLI, Python, and the
fullsend security tooling, so there is nothing to add — the sandbox *policy*, not
the image, is the enforcement layer.

## Acceptance run

The pinned agent was proven end-to-end with the exact command CI runs (TC-5815).
The command is identical locally and in CI (see **Running verify-pr**) — same
harness, same registration, same pinned content; only the runtime environment
differs (a local SA key vs. a CI WIF config).

**Run** — `verify-pr` against **TC-6137 / PR #294** at commit `c0bbad9`, off the
base pin `6572360e`, on 2026-09-09:

```bash
fullsend run verify-pr --fullsend-dir .fullsend \
  --target-repo /tmp/verify-pr-clone \
  --env-file <gcp-vertex.env> --env-file <verify-pr.env> \
  --keep-sandbox
```

`--target-repo` was a **disposable clone checked out at the PR head**, never the
working directory (fullsend deletes it after the run — see **Known issues**).

**Results:**

| Acceptance criterion | Result |
|---|---|
| Sandbox-mode run off the pin | ✅ model `claude-opus-4-6`, 1 iteration, 39 turns, 52 tool calls, 4 sub-agents dispatched |
| Sub-agents dispatched within 30 min | ✅ sandbox wall-clock ≈ 9.5 min |
| Schema-valid `agent-result.json` | ✅ agent exit 0, `Validation: passed` |
| Zero `*.atlassian.net` egress from sandbox | ✅ none |
| Zero `api.github.com` egress from sandbox | ✅ none |
| Real writes (full run, post-script on runner) | ✅ sticky report **edited in place** on PR #294 (idempotent, no flood) + posted to Jira TC-6137 |

**DENIED endpoints — expected, none added.** The sandbox's only allowed egress is
`*.googleapis.com` (Vertex). The OCSF sandbox log records the least-privilege
policy correctly blocking every other attempted endpoint; these DENIED entries are
the control **working**, not failures, and no endpoint needed to be added to make
the run pass:

| Blocked endpoint | Process | Why it is correct |
|---|---|---|
| `github.com:443` | `git-remote-http`, `tirith` | Split-trust — the sandbox never touches GitHub; the PR-head tree arrives via `--target-repo` and writes happen on the runner. |
| `raw.githubusercontent.com:443` | `tirith` | Harness/plugin content is delivered pre-resolved from the pin; no in-sandbox fetch. |
| `downloads.claude.ai:443` | `claude` | Claude CLI self-update/telemetry — irrelevant to the run and correctly denied. |

The run's verdict on PR #294 was `FAIL` (verify-pr's assessment of that PR at
`c0bbad9`); the **run mechanics** above are what this acceptance proves, and they
all pass. This is one of several real production runs of the pinned agent during
Epic D — see the sticky `verify-pr` reports on PRs #292, #293, and #294.

### E2E acceptance via CI dispatch (TC-6192)

TC-5815 above proved the *agent*; TC-6192 proves the *CI-gated dispatch path* end
to end: a qualifying PR triggers `.github/workflows/fullsend-verify-pr.yml`, the
`wait-for-checks` job waits for the PR's other checks to reach a terminal state,
and the `verify-pr` reusable-dispatch job then mints the review-role App token via
OIDC and posts the report — whether CI passed or failed (TC-6180 Reqs 4, 6, 7).

**Vehicle** — a throwaway PR **#300** (`tc-6192-e2e-acceptance` →
`verify-pr-fullsend`, head branch on the **upstream** repo so `pull_request`
secrets + OIDC are available — a fork head would get neither; this pre-TC-6331
constraint is now lifted, see **Fork PRs**), qualified against
Jira task **TC-6254** (status `Review`, label `ai-generated-jira`, Git PR field =
PR #300 URL). The Jira report comment is authored by the tier-1 Jira account
configured for that run (**Marco Rizzi**).

**Results — all five acceptance criteria proven:**

| Acceptance criterion | Result |
|---|---|
| Qualifying PR → CI finishes → verify-pr dispatches | ✅ `wait-for-checks` released after `python-tests` reached terminal, then `verify-pr` ran |
| Report posts to the PR **and** Jira | ✅ sticky report on PR #300 + comment on Jira TC-6254, every run |
| Runs with **CI passing** | ✅ `python-tests` **34990552632 = success** → verify-pr **34990553318** posted report for commit `3271577` (CI Status PASS, Overall **WARN**) |
| Runs with **CI failing** | ✅ `python-tests` **34991800394 = failure** (all 4 matrix jobs, intentional `assert False`) → `wait-for-checks` still released → verify-pr **34991800865** posted report for commit `64b818c` (CI Status **FAIL**, Overall **FAIL**); CI-failure sub-task **TC-6255** auto-created |
| No duplicate reports on re-run of the same head | ✅ re-ran verify-pr **34991800865** on the **same** head `64b818c` (completed/success): PR #300 stayed at exactly **2** report comments (`3271577`, `64b818c` — the second edited in place, not re-posted), Jira TC-6254 stayed at exactly **1** comment (updated in place, both reports appended) |

The **CI-fail** row is the crux: CI result is *data, not a gate*. The
`allowed-conclusions` on `wait-for-checks` includes `failure`, so a failing
`python-tests` still releases the wait and verify-pr runs and reports — it simply
records `CI Status = FAIL` in the report. Idempotency holds independently on each
surface: the PR uses one comment per distinct commit SHA (marker
`<!-- sdlc-workflow:verify-pr report commit:<sha7> -->`); Jira uses a single
comment updated in place per task.

**DENIED endpoints — expected, none added.** As with TC-5815, the sandbox's
only egress is Vertex; the OCSF log's DENIED `github.com` / `raw.githubusercontent.com`
entries are the split-trust policy **working** (prefetch on the runner, writes on
the runner via the post-script), not failures — no endpoint was added to pass.

The vehicle is disposable: PR #300, branch `tc-6192-e2e-acceptance`, test issues
TC-6254/TC-6255, and the scaffolding files (`docs/e2e/tc-6192-vehicle.md`,
`plugins/sdlc-workflow/scripts/test_tc6192_ci_fail.py`) are removed after
acceptance is recorded.

### CI Status sourced from prefetched check-runs (TC-6257)

TC-6192 above recorded a `CI Status` verdict, but the sandbox had **no** way to
retrieve it: with no `gh` CLI and no egress, the check ran off the diff and warned
*"CI status could not be retrieved in sandbox mode."* TC-6257 closes that gap — the
pre_script now prefetches the head-SHA check-run outcomes (`github.check_runs`) on
the trusted runner, and the concatenated `--log-failed` output of every failed
check-run into `check-run-logs.txt` (mounted separately; only its path rides in
the bundle, so the log text stays off the agent's context until Correctness
Check 1b reads it on a FAIL). This supersedes the TC-6192 "unavailable in sandbox"
caveat: `CI Status` is now sourced from real CI data.

**Re-pin is load-bearing.** The children delivered to the sandbox are fetched from
the URL-pinned harness base. Advancing the prefetch code alone is inert until the
base pin moves to a commit that contains it: the base-file bytes are unchanged
(sha256 `3c9dc221…`), so only the pinned commit moves (`a9099de0` → `fa3f4b7d`) and
`fullsend lock` refreezes all 11 children at `fa3f4b7d`. Before the re-pin the
sandbox kept running the pre-TC-6257 skill, whose bundle carries no `check_runs`,
and `CI Status` fell back to the old WARN.

**Vehicle** — throwaway PR **#303** (`tc-6257-e2e-vehicle` → `verify-pr-fullsend`,
**upstream** so `pull_request` gets secrets + OIDC — pre-TC-6331, now lifted),
qualified against Jira task **TC-6266** (status `Review`, label
`ai-generated-jira`, Git PR field = PR #303).

**Results — both prefetch surfaces proven live:**

| Acceptance criterion | Result |
|---|---|
| `CI Status` sourced from prefetched `check_runs` (not the WARN fallback) | ✅ verify-pr **35075966985** (commit `1185ae2`, post-re-pin) named the failed check by run ID + conclusion — data the pre-TC-6257 sandbox could not obtain |
| **CI failing** → prefetched log read by Check 1b | ✅ vehicle-only red commit `8865e11`: `Script Unit Tests` **35077403829 = failure** (deliberate canary) → `wait-for-checks` released → verify-pr **35077404421** reported `CI Status = FAIL` and Check 1b surfaced the **runtime-computed canary `cc08a78a24bc66f6`** — a value present **only** in the prefetched `--log-failed` output, never as a literal in the diff — proving the log was read, not inferred |
| CI-failure sub-task auto-created | ✅ **TC-6271** ("Fix failing CI check Script Unit Tests … intentional canary") created, blocks TC-6266, with the `details_url` for the full log |

The canary is the crux: because its value is computed at test runtime and never
written in the source, the only way the report could quote `cc08a78a24bc66f6` is by
reading the prefetched `check-run-logs.txt` — end-to-end proof of the failed-CI log
prefetch path. (The live run also surfaced two real hardening follow-ups on the
prefetch code — treat `startup_failure`/`stale` as failed conclusions, and only
expose `check_run_logs_path` when the log fetch actually succeeds.)

The vehicle is disposable: PR #303, branch `tc-6257-e2e-vehicle`, test issue
TC-6266 (and its sub-tasks), and the scaffolding file
(`plugins/sdlc-workflow/scripts/test_tc6257_ci_fail.py`, vehicle-only — never on
the TC-6257 deliverable branch) are removed after acceptance is recorded.

## Known issues

- **fullsend deletes the target repo directory** after each run — always pass a
  disposable clone as `--target-repo`, never your working directory.
- **Markdown tables collapse to one line in Jira comments** posted via
  `fullsend issues n --tracker jira` — the vendor's markdown→ADF conversion
  doesn't support GFM tables (parser has no table extension; no table node
  handler). GitHub renders the same body correctly. Tracked upstream:
  <https://github.com/fullsend-ai/fullsend/issues/7345>.
