# Running sdlc-workflow skills with fullsend

Run sdlc-workflow skills inside secure sandboxes via
[fullsend](https://github.com/fullsend-ai/fullsend). The agent runs in an
isolated container with least-privilege network and filesystem policies, while
all issue-tracker and GitHub writes happen on the trusted runner — never inside
the sandbox.

This guide documents the **native v0.37.0 path**: a standalone root-level
harness, the stock digest-pinned `fullsend-code` image, a single pinned-URL
registration, and the plugin referenced in place with zero duplication. The only
skill wired up today is `verify-pr`.

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
itself receives read-only context only — `JIRA_ISSUE_ID` and `JIRA_BASE_URL`
(display links) — plus the prefetched read bundle mounted read-only. The **only**
credential that ever enters the sandbox is the Vertex AI service-account key,
because model inference runs in-sandbox (see below).

## Credential delivery and tiers

Credentials use the highest isolation tier possible. Two of the three services
never place a credential in the sandbox at all.

| Service | Tier | Credential in sandbox? | How it is delivered |
|---|---|---|---|
| **Jira** | 1 | No | The pre_script prefetches the issue on the runner; the post_script posts comments with `fullsend issues post-comment --tracker jira`. The token stays in runner env only. |
| **GitHub** | 1 | No | The pre_script prefetches the read bundle (`gh pr diff` / `gh pr view` → diff, diffstat, reviews, comments, commits) and records the PR head ref name and head commit SHA in it; the post_script writes via `fullsend issues post-comment --tracker github` and `gh` (PR reviews/replies via `gh api`). The token stays in runner env only. The PR-head working tree is the `--target-repo` clone, checked out at the head SHA before the run (see below) — the pre_script does not check out. |
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

- [fullsend](https://github.com/fullsend-ai/fullsend) v0.37.0 CLI installed.
- An OpenShell gateway running — fullsend uses OpenShell as its sandbox runtime.
- GCP credentials for Vertex AI — a service-account key JSON (local) or a WIF
  external-account config (CI). Referenced by `GOOGLE_APPLICATION_CREDENTIALS`.
- A Jira API token and a GitHub token — used by the pre/post scripts on the
  runner only.
- The Python `jsonschema` package on the runner — the `validation_loop`
  validates agent output against the JSON schema before the post_script runs
  (`pip install jsonschema`).

## Running verify-pr

The command is **identical locally and in CI** — same harness, same registration,
only the runtime environment differs (a local SA key vs. a CI WIF config; a CI
run additionally supplies an OIDC token file):

```bash
fullsend run verify-pr \
  --fullsend-dir .fullsend \
  --target-repo /tmp/my-repo-clone \
  --env-file secrets.env \
  --env-file <(echo "JIRA_ISSUE_ID=TC-1234")
```

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
| `agents/verify-pr.md` | Agent prompt (YAML frontmatter). fullsend launches Claude Code with this as the system prompt; it reads `JIRA_ISSUE_ID` and invokes the skill. |
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

## Known issues

- **fullsend deletes the target repo directory** after each run — always pass a
  disposable clone as `--target-repo`, never your working directory.
