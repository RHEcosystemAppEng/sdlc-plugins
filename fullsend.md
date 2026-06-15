# Running sdlc-workflow skills with fullsend

Run sdlc-workflow skills inside secure sandboxes via [fullsend](https://github.com/fullsend-ai/fullsend). Each skill runs in an isolated container with least-privilege network and filesystem policies.

## Prerequisites

- [fullsend](https://github.com/fullsend-ai/fullsend) CLI installed
- [OpenShell](https://github.com/NVIDIA/OpenShell) gateway running — fullsend uses OpenShell as its sandbox runtime; the gateway manages container lifecycle
- GCP credentials for Vertex AI (or Anthropic API key) — Claude Code needs LLM API access from inside the sandbox
- Jira API token — skills read/write Jira issues via REST API (MCP is not available inside the sandbox)
- GitHub token — skills read PRs and post comments via `gh` CLI
- Python `jsonschema` package on the runner — the `validation_loop` validates agent output against the JSON schema before the post_script runs (`pip install jsonschema`)

## Quick start (local mode)

```bash
fullsend run verify-pr \
  --fullsend-dir plugins/sdlc-workflow \
  --target-repo /tmp/my-repo-clone \
  --env-file secrets.env
```

This assumes sdlc-plugins is cloned locally. For target repos without the
clone, see [Deployment modes](#deployment-modes) below.

The `--fullsend-dir` points to the plugin directory itself — it doubles as the
fullsend config directory, so the same skill files serve both Claude Code plugin
users and fullsend users with zero duplication.

The `--target-repo` must be a disposable clone, not your working directory —
fullsend deletes and re-creates this directory after each run
([fullsend#2075](https://github.com/fullsend-ai/fullsend/issues/2075)).

The post_script handles all Jira/GitHub write operations (sub-task creation,
PR comment replies, verification report posting) after the sandbox agent
completes and output validation passes.

## Secrets env file

Create a secrets file (never commit this). The `--env-file` flag is repeatable —
use a separate file for per-run variables like `JIRA_ISSUE_ID`:

```bash
# secrets.env — long-lived credentials
ANTHROPIC_VERTEX_PROJECT_ID=my-project
GOOGLE_CLOUD_PROJECT=my-project
CLOUD_ML_REGION=global
GOOGLE_APPLICATION_CREDENTIALS=/path/to/sa-key.json
JIRA_SERVER_URL=https://myorg.atlassian.net
JIRA_EMAIL=me@example.com
JIRA_API_TOKEN=my-jira-token
GH_TOKEN=my-github-token
```

```bash
# task.env — per-run variables
JIRA_ISSUE_ID=PROJ-123
```

```bash
fullsend run verify-pr \
  --fullsend-dir plugins/sdlc-workflow \
  --target-repo /tmp/my-repo-clone \
  --env-file secrets.env \
  --env-file task.env
```

Later env files override earlier ones, so `task.env` can override any value
from `secrets.env`.

## Building the image

Fullsend runs agents inside sandboxed containers. Claude Code discovers plugins
through a marketplace cache structure under `$CLAUDE_CONFIG_DIR/plugins/`. The
Dockerfile extends fullsend's base image and bakes the sdlc-workflow plugin into
this cache so Claude Code auto-discovers the skills — no `--plugin-dir` flag needed
at runtime.

```bash
podman build -f plugins/sdlc-workflow/sandboxes/base/Dockerfile \
  -t ghcr.io/mrizzi/sdlc-plugins/sdlc-base:latest .
```

The image only needs rebuilding when the plugin's skills or shared files change.

## File inventory

All paths are relative to `plugins/sdlc-workflow/`.

| File | Purpose | Why |
|---|---|---|
| `sandboxes/base/Dockerfile` | Container image extending `fullsend-code` with the sdlc-workflow plugin baked into Claude Code's marketplace cache | Extends fullsend's own image to inherit TLS proxy CA workaround, security tooling (gitleaks, tirith), and all system dependencies. We only add the plugin. |
| `sandboxes/base/Dockerfile.hummingbird` | Alternative image based on Red Hat Hummingbird (near-zero CVE) | For environments that require RPM-based images. Self-contained — installs all tools via `dnf` from official repos (Anthropic, GitHub, Hummingbird). |
| `sandboxes/base/bootstrap-plugin-cache.sh` | Generates Claude Code marketplace cache structure at build time | Claude Code auto-discovers plugins from `$CLAUDE_CONFIG_DIR/plugins/` only if the marketplace cache JSON files exist. This script replicates the structure that fullsend's `bootstrapPlugins()` Go function creates at runtime, but baked into the image so no host-side plugin upload is needed. |
| `sandboxes/base/claude-code.repo` | Anthropic's official RPM repo definition for Claude Code | Only used by `Dockerfile.hummingbird`. The default Dockerfile inherits Claude Code from the fullsend base image. |
| `providers/jira.yaml` | OpenShell provider for Jira credentials | The gateway proxy swaps opaque placeholder tokens for real `JIRA_EMAIL` and `JIRA_API_TOKEN` at the HTTP layer. Credentials never enter the sandbox ([ADR-0025](https://github.com/fullsend-ai/fullsend/blob/main/docs/ADRs/0025-provider-credential-delivery-for-sandboxed-agents.md), tier 2). |
| `providers/github.yaml` | OpenShell provider for GitHub token | Uses the built-in `github` provider type. The gateway injects `GH_TOKEN` as an opaque placeholder, swapped transparently when `gh` CLI makes API calls. |
| `harness/verify-pr.yaml` | Fullsend harness config for the verify-pr skill | Declares the image, policy, providers, env file mounts, and timeout. Fullsend reads this to know how to create the sandbox, what credentials to inject, and how long the agent can run. |
| `agents/verify-pr.md` | Agent prompt with YAML frontmatter | Fullsend launches Claude Code with `--agent verify-pr` which loads this file as the system prompt. The YAML frontmatter is required — without it Claude Code treats the file as a generic prompt and ignores the instructions. The agent reads `JIRA_ISSUE_ID` from the environment and invokes the skill. |
| `policies/verify-pr.yaml` | Sandbox network/filesystem policy | Controls which endpoints the sandbox can reach and whether the filesystem is read-only or read-write. Each network policy entry requires a `name:` field (OpenShell supervisor crashes without it), prefix wildcards only (`*.googleapis.com`, not `*-pattern.domain`), and `**/binary` double-star globs for binary paths. These constraints were discovered by testing against OpenShell and verified against fullsend's production policies. |
| `env/gcp-vertex.env` | Vertex AI env var template | Expanded at runtime from the secrets file via fullsend's `host_files` with `expand: true`. Sets `CLAUDE_CODE_USE_VERTEX=1` and points `GOOGLE_APPLICATION_CREDENTIALS` to the uploaded credential file at `/tmp/gcp-creds.json`. |
| `env/jira.env` | Jira non-credential config | Carries `JIRA_SERVER_URL` (for URL construction) and `JIRA_ISSUE_ID` (task identifier). Credentials (`JIRA_EMAIL`, `JIRA_API_TOKEN`) are injected by the Jira provider, not this file. |
| `schemas/verify-pr-result.schema.json` | JSON Schema for verify-pr structured output | Defines the action types, cross-reference format, and report structure. Validated by fullsend's `validation_loop` before the post_script runs. |
| `scripts/pre-verify-pr.sh` | Pre_script for verify-pr | Validates inputs before sandbox creation: checks required env vars, JIRA_ISSUE_ID format, issue existence, and PR linkage. Fails fast to avoid wasting sandbox compute time. |
| `scripts/post-verify-pr.sh` | Post_script for verify-pr | Shell wrapper that finds `agent-result.json` and delegates to `execute-actions.py`. Runs on the trusted runner after sandbox is destroyed. |
| `scripts/execute-actions.py` | Action executor | Processes the ordered actions array, resolves `{{ref.key}}` placeholders as Jira entities are created, calls `jira-client.py` and `gh` CLI for all write operations. |
| `scripts/validate-output-schema.sh` | Output schema validator | Generic script from fullsend that validates JSON against a schema using Python's `jsonschema`. Used by `validation_loop`. |

## Adding a new skill

Each skill needs 3 files. The env templates are shared across all skills — only
add a new env file if the skill requires variables not already covered.

### 1. Agent prompt — `agents/<skill>.md`

YAML frontmatter is required — without it, Claude Code treats the file as a
generic prompt rather than an agent definition, and the startup instructions
are ignored. The agent receives "Run the agent task" as the user message from
fullsend and must read env vars to determine what to do.

```markdown
---
name: <skill>
description: >-
  One-line description of what this agent does.
model: opus
---

# <Skill> Agent

You are running inside an OpenShell sandbox with the sdlc-workflow plugin
pre-installed.

## Startup procedure

1. Read the relevant environment variable:
   ```bash
   echo $JIRA_ISSUE_ID
   ```

2. Invoke the skill:
   ```
   /sdlc-workflow:<skill> <issue-id>
   ```

## Constraints

- <list constraints relevant to this skill>
```

### 2. Harness — `harness/<skill>.yaml`

Defines the image, policy, env files, and timeout. All skills share the same
image — the policy (not the image) controls per-skill network and filesystem
access. Security is enabled so fullsend runs pre-agent scans (context injection
detection, secret scanning) using the tools baked into the fullsend base image.

```yaml
agent: agents/<skill>.md
model: opus
image: ghcr.io/mrizzi/sdlc-plugins/sdlc-base:latest
policy: policies/<skill>.yaml

security:
  enabled: true

host_files:
  - src: env/gcp-vertex.env
    dest: /tmp/workspace/.env.d/gcp-vertex.env
    expand: true
  - src: env/jira.env
    dest: /tmp/workspace/.env.d/jira.env
    expand: true
  - src: env/github.env
    dest: /tmp/workspace/.env.d/github.env
    expand: true
  - src: ${GOOGLE_APPLICATION_CREDENTIALS}
    dest: /tmp/gcp-creds.json
  - src: ${GCP_OIDC_TOKEN_FILE}
    dest: /tmp/gcp-oidc-token
    optional: true

timeout_minutes: 30
```

### 3. Policy — `policies/<skill>.yaml`

Defines which network endpoints and filesystem paths the skill can access.
Start from the verify-pr policy and adjust based on what the skill needs:

- **Read-only skills** (plan-feature, verify-pr, define-feature): set
  `include_workdir: false` and list workspace in `read_only`. This prevents
  the skill from modifying code — the sandbox enforces it via Landlock LSM.
- **Read-write skills** (implement-task, setup): set `include_workdir: true`
  and list workspace in `read_write`. The skill can modify files, but network
  access is still constrained by the policy.
- **GitHub write access**: add a `github_git` policy entry with port 22 for
  SSH push. Only implement-task needs this.
- **Figma access**: add a `figma` policy entry for `api.figma.com`. Only
  plan-feature needs this (to read design mockups).
- **Package registries**: add `npm_registry`, `crates_io`, `pypi` entries.
  Only implement-task needs these (to install dependencies for building/testing).

Policy format constraints discovered during testing:

- Every network policy entry requires a `name:` field — the OpenShell sandbox
  supervisor crashes silently without it
- Only prefix wildcards work (`*.googleapis.com`) — mid-string wildcards
  (`*-aiplatform.googleapis.com`) cause the supervisor to crash
- Binary paths must use `**/binary` double-star globs — absolute paths
  (`/usr/local/bin/claude`) don't match inside the sandbox
- `landlock: compatibility: best_effort` is required — without it Landlock
  may block sandbox startup depending on the kernel version

```yaml
version: 1

filesystem_policy:
  include_workdir: false
  read_only:
    - /var/log
    - /usr
    - /lib
    - /lib64
    - /proc
    - /dev/urandom
    - /etc
    - /opt
    - /sandbox
  read_write:
    - /tmp
    - /dev/null

landlock:
  compatibility: best_effort

process:
  run_as_user: sandbox
  run_as_group: sandbox

network_policies:
  claude_code:
    name: claude-code
    endpoints:
      - { host: api.anthropic.com, port: 443 }
      - { host: "*.googleapis.com", port: 443 }
      - { host: "*.amazonaws.com", port: 443 }
      - { host: statsig.anthropic.com, port: 443 }
      - { host: sentry.io, port: 443 }
      - { host: raw.githubusercontent.com, port: 443 }
      - { host: platform.claude.com, port: 443 }
    binaries:
      - { path: "**/claude" }
      - { path: "**/node" }
  jira:
    name: jira
    endpoints:
      - { host: "*.atlassian.net", port: 443 }
    binaries:
      - { path: "**/claude" }
      - { path: "**/python3" }
  github_api:
    name: github-api
    endpoints:
      - { host: api.github.com, port: 443 }
    binaries:
      - { path: "**/claude" }
      - { path: "**/gh" }
```

## Deployment modes

There are two ways to run sdlc-workflow skills via fullsend, depending on
whether the user has sdlc-plugins cloned locally.

### Local mode — for sdlc-plugins developers

When sdlc-plugins is cloned locally, point `--fullsend-dir` at the plugin
directory. All files (harness, agents, policies, env) are resolved locally.
Updates arrive via `git pull`.

```bash
fullsend run verify-pr \
  --fullsend-dir plugins/sdlc-workflow \
  --target-repo /tmp/my-repo-clone \
  --env-file secrets.env
```

The post_script handles all Jira/GitHub write operations (sub-task creation,
PR comment replies, verification report posting) after the sandbox agent
completes and output validation passes.

### Remote mode — for target repos without sdlc-plugins

Target repos that consume sdlc-workflow skills without cloning sdlc-plugins
use URL-referenced resources in their own `.fullsend/` directory. The agent
prompt and policy are fetched from GitHub at runtime; the plugin is baked
into the custom image.

```
my-repo/
├── .fullsend/
│   ├── harness/
│   │   └── verify-pr.yaml      # URL refs to agent/policy + image tag
│   └── env/
│       ├── gcp-vertex.env       # ${VAR} templates (identical across repos)
│       ├── jira.env
│       └── github.env
├── AGENTS.md → CLAUDE.md        # symlink (recommended)
└── ...
```

The harness references the agent and policy via URLs with mandatory SHA-256
integrity hashes ([ADR-0038](https://github.com/fullsend-ai/fullsend/blob/58cc443/docs/ADRs/0038-universal-harness-access.md)).
The plugin comes from the custom image — `plugins:` does not support URL
references today ([fullsend#2113](https://github.com/fullsend-ai/fullsend/issues/2113)).

```yaml
# .fullsend/harness/verify-pr.yaml
agent: https://raw.githubusercontent.com/mrizzi/sdlc-plugins/<commit>/plugins/sdlc-workflow/agents/verify-pr.md#sha256=<hash>
model: opus
image: ghcr.io/mrizzi/sdlc-plugins/sdlc-base:<version>
policy: https://raw.githubusercontent.com/mrizzi/sdlc-plugins/<commit>/plugins/sdlc-workflow/policies/verify-pr.yaml#sha256=<hash>

security:
  enabled: true

host_files:
  - src: env/gcp-vertex.env
    dest: /tmp/workspace/.env.d/gcp-vertex.env
    expand: true
  - src: env/jira.env
    dest: /tmp/workspace/.env.d/jira.env
    expand: true
  - src: env/github.env
    dest: /tmp/workspace/.env.d/github.env
    expand: true
  - src: ${GOOGLE_APPLICATION_CREDENTIALS}
    dest: /tmp/gcp-creds.json
  - src: ${GCP_OIDC_TOKEN_FILE}
    dest: /tmp/gcp-oidc-token
    optional: true

allowed_remote_resources:
  - https://raw.githubusercontent.com/mrizzi/sdlc-plugins/

timeout_minutes: 30
```

```bash
fullsend run verify-pr \
  --fullsend-dir .fullsend \
  --target-repo . \
  --env-file secrets.env
```

### Keeping target repos up to date

When sdlc-plugins publishes a new version, target repos need to bump three
values in their harness YAML: the two SHA-256 hashes (agent, policy) and the
image tag.

Use [Renovate](https://docs.renovatebot.com/) or
[Dependabot](https://docs.github.com/en/code-security/dependabot) to automate
this. On each sdlc-plugins release, the bot computes new hashes, opens a PR
to bump them, and the maintainer merges when ready. This is the same model
used for GitHub Actions SHA pinning.

The env template files (`gcp-vertex.env`, `jira.env`, `github.env`) are pure
`${VAR}` placeholders and rarely change — they do not need version tracking.

When [fullsend#2113](https://github.com/fullsend-ai/fullsend/issues/2113) is
resolved, the custom image is eliminated: the plugin is also URL-referenced,
and the image becomes the standard `fullsend-code:latest`. This reduces the
bump to two hashes + one plugin hash — still automated by Renovate.

## Design decisions

### Why the plugin directory is the fullsend dir

Fullsend's `--fullsend-dir` requires all referenced files (harness, agents,
policies, env, skills) to be inside that directory — paths that resolve outside
are rejected for security. By placing the fullsend config files alongside the
existing plugin files, both Claude Code users and fullsend users consume the
same skill definitions with zero duplication.

### Why one image for all skills

The policy (not the image) controls what each skill can access. All skills need
the same tools (Claude Code, Git, GH CLI, Python) and the same plugin. Building
per-skill images would multiply build time and storage with no security benefit —
the sandbox policy is the enforcement layer.

### Why `--dangerously-skip-permissions`

Fullsend launches Claude Code with `--dangerously-skip-permissions` because the
sandbox policy is the permission layer. Claude Code's built-in permission prompts
are designed for interactive use; inside a headless sandbox, the OpenShell network
and filesystem policies enforce the same boundaries without user interaction.

### Why Jira REST API instead of MCP

MCP servers are not available inside the sandbox — they run as separate processes
that require localhost network access and configuration that doesn't transfer
into the container. Skills detect MCP unavailability and fall back to the Jira
REST API v3 using env vars (`JIRA_SERVER_URL`, `JIRA_EMAIL`, `JIRA_API_TOKEN`).

### Credential delivery tiers

Per [ADR-0025](https://github.com/fullsend-ai/fullsend/blob/main/docs/ADRs/0025-provider-credential-delivery-for-sandboxed-agents.md),
credentials use the highest isolation tier possible:

| Service | Tier | Model | Credentials in sandbox? |
|---|---|---|---|
| Jira | 2 | OpenShell provider (`providers/jira.yaml`) | No — gateway proxy swaps placeholder tokens |
| GitHub | 2 | OpenShell provider (`providers/github.yaml`) | No — gateway proxy swaps placeholder tokens |
| GCP Vertex AI | 4 | Host file (`${GOOGLE_APPLICATION_CREDENTIALS}`) | Yes — file-based auth requires local JWT signing |

Tier 1 (prefetch + post-process with zero credential access) is partially
achieved: the pre_script pre-fetches the Jira issue, and the post_script
handles all writes. The sandbox still needs runtime GitHub API access for
PR diff, reviews, and CI status.

## Comparison with fullsend canonical patterns

Full comparison of our approach against fullsend's conventions. References are
permalinked to fullsend commit `58cc443`.

| Aspect | Fullsend canonical | Our approach | Aligned? | Justification or convergence plan | References |
|---|---|---|---|---|---|
| Harness YAML location | `harness/<agent>.yaml` | `harness/verify-pr.yaml` | ✓ | — | [customizing-agents.md](https://github.com/fullsend-ai/fullsend/blob/58cc443/docs/guides/user/customizing-agents.md) |
| Agent prompts | `agents/<agent>.md` with YAML frontmatter | `agents/verify-pr.md` with frontmatter | ✓ | — | [customizing-agents.md](https://github.com/fullsend-ai/fullsend/blob/58cc443/docs/guides/user/customizing-agents.md) |
| Policies | `policies/<agent>.yaml` | `policies/verify-pr.yaml` | ✓ | — | [ADR-0020](https://github.com/fullsend-ai/fullsend/blob/58cc443/docs/ADRs/0020-composable-single-responsibility-agents-with-individual-sandboxes.md) |
| Env templates | `env/*.env` with `${VAR}` + `expand: true` | Same pattern | ✓ | — | [customizing-agents.md](https://github.com/fullsend-ai/fullsend/blob/58cc443/docs/guides/user/customizing-agents.md) |
| GCP creds via host_files | `${GOOGLE_APPLICATION_CREDENTIALS}` mounted | Same | ✓ | — | [running-agents-locally.md](https://github.com/fullsend-ai/fullsend/blob/58cc443/docs/guides/user/running-agents-locally.md) |
| Security scanning | `security: enabled: true` (default) | Same | ✓ | — | [runtimes.md](https://github.com/fullsend-ai/fullsend/blob/58cc443/docs/runtimes.md) |
| Skills loading | `skills:` field — uploaded from host at runtime | Baked into image via marketplace cache | Diverges | **Interim**: custom image bakes plugin into marketplace cache. `plugins:` field is for Claude Code marketplace plugins (not just LSP). **Target**: plugin referenced via URL in harness once fullsend adds URL support for `plugins:` field in `ResolveHarness()`. Tracked in [fullsend#2113](https://github.com/fullsend-ai/fullsend/issues/2113). | [customizing-with-skills.md](https://github.com/fullsend-ai/fullsend/blob/58cc443/docs/guides/user/customizing-with-skills.md), [runtimes.md](https://github.com/fullsend-ai/fullsend/blob/58cc443/docs/runtimes.md), [ADR-0038](https://github.com/fullsend-ai/fullsend/blob/58cc443/docs/ADRs/0038-universal-harness-access.md) |
| Plugin loading | `plugins:` field — marketplace cache created at runtime | Baked into image at build time | Diverges | **Interim**: same root cause as skills loading — `plugins:` field does not support URL references today, so build-time baking is the only option without duplication. **Target**: converges with skills loading when [fullsend#2113](https://github.com/fullsend-ai/fullsend/issues/2113) is resolved. | [customizing-agents.md](https://github.com/fullsend-ai/fullsend/blob/58cc443/docs/guides/user/customizing-agents.md), [ADR-0038](https://github.com/fullsend-ai/fullsend/blob/58cc443/docs/ADRs/0038-universal-harness-access.md) |
| Pre/post scripts | `pre_script` + `post_script` for split-trust | `post_script` executes structured JSON actions from sandbox output | ✓ | **Converged**: sandbox produces `agent-result.json` with ordered actions. `post_script` resolves `{{ref.key}}` placeholders and executes writes (Jira sub-tasks, PR replies, report posting). `validation_loop` validates output against JSON schema before post_script runs. | [architecture.md](https://github.com/fullsend-ai/fullsend/blob/58cc443/docs/architecture.md), [security-threat-model.md](https://github.com/fullsend-ai/fullsend/blob/58cc443/docs/problems/security-threat-model.md) |
| Validation loop | `validation_loop:` with script + `max_iterations` | `validation_loop` validates `agent-result.json` against `verify-pr-result.schema.json` | ✓ | **Converged**: uses fullsend's standard `validate-output-schema.sh` with the verify-pr JSON schema. Up to 2 iterations if first output fails validation. | [customizing-agents.md](https://github.com/fullsend-ai/fullsend/blob/58cc443/docs/guides/user/customizing-agents.md), [architecture.md](https://github.com/fullsend-ai/fullsend/blob/58cc443/docs/architecture.md) |
| Config directory | Dedicated `.fullsend` repo per org | Two modes: local (`--fullsend-dir plugins/sdlc-workflow`) and remote (per-repo `.fullsend/` with URL refs) | Diverges | **Local mode**: plugin dir as `--fullsend-dir` for sdlc-plugins developers. **Remote mode**: per-repo `.fullsend/` with URL-referenced agent/policy + custom image on GHCR. Hashes and image tag bumped by Renovate/Dependabot. **Target**: standard `fullsend-code` image + plugin via URL when [fullsend#2113](https://github.com/fullsend-ai/fullsend/issues/2113) is resolved. | [ADR-0003](https://github.com/fullsend-ai/fullsend/blob/58cc443/docs/ADRs/0003-org-config-repo-convention.md), [ADR-0035](https://github.com/fullsend-ai/fullsend/blob/58cc443/docs/ADRs/0035-layered-content-resolution.md), [ADR-0038](https://github.com/fullsend-ai/fullsend/blob/58cc443/docs/ADRs/0038-universal-harness-access.md) |
| Layered resolution | Three-tier: upstream < org < per-repo | Single layer — no overrides | Diverges | **Keep**: per-repo `.fullsend/` with URL refs is the correct tier for external skills consumed across multiple orgs. Org-level `.fullsend` repo with `customized/` is possible but requires copying files on each release — Renovate on per-repo URL refs is lower maintenance. | [ADR-0035](https://github.com/fullsend-ai/fullsend/blob/58cc443/docs/ADRs/0035-layered-content-resolution.md) |
| AGENTS.md | Auto-loaded from target repo | Not shipped | Diverges | **Converge now**: recommend target repos create symlink `AGENTS.md → CLAUDE.md`. Verified that fullsend preserves symlinks through upload/download cycle (`UploadDir` uses `tar` without `--dereference`, `sanitizeDownload` allows relative in-repo symlinks, `hasAgentsMD` detects symlink as existing file). Document in fullsend.md. | [customizing-with-agents-md.md](https://github.com/fullsend-ai/fullsend/blob/58cc443/docs/guides/user/customizing-with-agents-md.md), [ADR-0020](https://github.com/fullsend-ai/fullsend/blob/58cc443/docs/ADRs/0020-composable-single-responsibility-agents-with-individual-sandboxes.md) |
| `.agents/skills/` convention | Skills in `.agents/skills/` + symlink to `.claude/skills/` | Skills in `skills/` (Claude Code plugin format) | Different convention | **Keep**: Claude Code plugin format (`plugin.json` + `skills/`) predates `.agents/skills/`. Both are valid for different discovery mechanisms. No benefit converting — Claude Code discovers plugins via marketplace cache, not `.agents/skills/`. | [customizing-with-skills.md](https://github.com/fullsend-ai/fullsend/blob/58cc443/docs/guides/user/customizing-with-skills.md) |
| Output schemas | `schemas/` directory for JSON validation | `schemas/verify-pr-result.schema.json` | ✓ | **Converged**: JSON Schema defines action types, cross-reference format, and report structure. Validated by `validation_loop` before post_script runs. | [architecture.md](https://github.com/fullsend-ai/fullsend/blob/58cc443/docs/architecture.md) |

## Known issues

- **fullsend deletes the target repo directory** after each run
  ([#2075](https://github.com/fullsend-ai/fullsend/issues/2075)). Always use
  a disposable clone as `--target-repo`, never your working directory.
- **macOS AppleDouble file corruption** in `.git/objects/pack/` after fullsend
  runs ([#2032](https://github.com/fullsend-ai/fullsend/issues/2032)). Fixed
  in fullsend by adding `COPYFILE_DISABLE=1` to the tar command.

## Available skills

| Skill | Harness | Status |
|---|---|---|
| verify-pr | `harness/verify-pr.yaml` | Working |
| implement-task | — | Not yet added |
| plan-feature | — | Not yet added |
| define-feature | — | Not yet added |
