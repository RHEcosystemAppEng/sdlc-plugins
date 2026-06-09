# Running sdlc-workflow skills with fullsend

Run sdlc-workflow skills inside secure sandboxes via [fullsend](https://github.com/fullsend-ai/fullsend). Each skill runs in an isolated container with least-privilege network and filesystem policies.

## Prerequisites

- [fullsend](https://github.com/fullsend-ai/fullsend) CLI installed
- [OpenShell](https://github.com/NVIDIA/OpenShell) gateway running — fullsend uses OpenShell as its sandbox runtime; the gateway manages container lifecycle
- GCP credentials for Vertex AI (or Anthropic API key) — Claude Code needs LLM API access from inside the sandbox
- Jira API token — skills read/write Jira issues via REST API (MCP is not available inside the sandbox)
- GitHub token — skills read PRs and post comments via `gh` CLI

## Quick start

```bash
fullsend run verify-pr \
  --fullsend-dir plugins/sdlc-workflow \
  --target-repo /tmp/my-repo-clone \
  --env-file secrets.env \
  --no-post-script
```

The `--fullsend-dir` points to the plugin directory itself — it doubles as the
fullsend config directory, so the same skill files serve both Claude Code plugin
users and fullsend users with zero duplication.

The `--target-repo` must be a disposable clone, not your working directory —
fullsend deletes and re-creates this directory after each run
([fullsend#2075](https://github.com/fullsend-ai/fullsend/issues/2075)).

The `--no-post-script` skips post-processing scripts (push, PR creation) since
sdlc-workflow skills handle their own Jira/GitHub side effects.

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
  --env-file task.env \
  --no-post-script
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
| `harness/verify-pr.yaml` | Fullsend harness config for the verify-pr skill | Declares the image, policy, env file mounts, and timeout. Fullsend reads this to know how to create the sandbox, what credentials to inject, and how long the agent can run. |
| `agents/verify-pr.md` | Agent prompt with YAML frontmatter | Fullsend launches Claude Code with `--agent verify-pr` which loads this file as the system prompt. The YAML frontmatter is required — without it Claude Code treats the file as a generic prompt and ignores the instructions. The agent reads `JIRA_ISSUE_ID` from the environment and invokes the skill. |
| `policies/verify-pr.yaml` | Sandbox network/filesystem policy | Controls which endpoints the sandbox can reach and whether the filesystem is read-only or read-write. Each network policy entry requires a `name:` field (OpenShell supervisor crashes without it), prefix wildcards only (`*.googleapis.com`, not `*-pattern.domain`), and `**/binary` double-star globs for binary paths. These constraints were discovered by testing against OpenShell and verified against fullsend's production policies. |
| `env/gcp-vertex.env` | Vertex AI env var template | Expanded at runtime from the secrets file via fullsend's `host_files` with `expand: true`. Sets `CLAUDE_CODE_USE_VERTEX=1` and points `GOOGLE_APPLICATION_CREDENTIALS` to the uploaded credential file at `/tmp/gcp-creds.json`. |
| `env/jira.env` | Jira REST API env var template | MCP servers are not available inside the sandbox, so skills fall back to the Jira REST API using these env vars. Also carries `JIRA_ISSUE_ID` which the agent prompt reads to know which task to verify. |
| `env/github.env` | GitHub token env var template | The `GH_TOKEN` must be explicitly injected — it is not automatically inherited from the host environment. Without it, skills cannot post PR comments or read review feedback. |

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
