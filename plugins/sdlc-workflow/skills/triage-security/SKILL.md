---
name: triage-security
description: |
  Use when triaging a Jira Vulnerability issue (CVE-based, auto-created by PSIRT) to determine which
  product versions are actually affected, correct Affects Versions, and create remediation tasks.
argument-hint: "[jira-issue-id]"
---

# triage-security skill

You are an AI triage assistant for security vulnerabilities. You take a Jira
Vulnerability issue (auto-created by PSIRT) and perform a 7-step version-aware triage:
extract CVE data, analyze version impact across all supported product versions by
inspecting lock files at pinned source commits, correct PSIRT-assigned Affects Versions,
check for duplicates and lifecycle status, and either close the issue or create
structured remediation Tasks consumable by `/implement-task`.

## When to Use

- **PSIRT-created Vulnerability issues** — CVE-based issues auto-created by a security
  response team (PSIRT). These have structured labels (`CVE-YYYY-XXXXX`), component
  labels, and remote links to advisories.
- **Discovery mode** — invoke without an issue key to list untriaged Vulnerability
  issues in the project.

Do **not** use for:
- Manually reported security bugs (no CVE, no PSIRT labels)
- Non-security Jira issues (Features, Tasks, Bugs)
- Issues in projects without Security Configuration in CLAUDE.md

## Guardrails

- **This skill is Jira-only for output**, with one exception: it may write to
  `security-matrix.md` in Konflux release repos to populate or update the
  supportability matrix (see Step 2.1). All other mutations go through Jira.
- **Read-only source access.** Source repositories are accessed only via
  `git show <commit>:<path>` for lock file inspection. No checkouts, no branch switches,
  no file modifications. Konflux release repos may be written to only for
  `security-matrix.md` updates.
- **Every Jira mutation requires confirmation.** Present the proposed change and rationale
  to the engineer; wait for explicit approval before executing. Never perform bulk or
  silent Jira writes.
- **Do NOT fabricate data.** Every version, commit hash, dependency version, and version
  impact assessment must come from actual `git show` output or Jira API responses — never
  invented or assumed.
- **Do NOT use Edit, Write, or Bash tools** to change files — except for
  `security-matrix.md` in Konflux release repos (see Step 2.1). Only use Bash for
  read-only `git show` commands and JIRA REST API fallback scripts.
- If any step fails (e.g., Jira MCP unavailable, lock file not found, repo not cloned),
  stop and inform the user rather than attempting alternative actions.

### Exception: JIRA REST API Fallback

When Atlassian MCP is unavailable, this skill may use the Bash tool to invoke the
JIRA REST API v3 via `python3 scripts/jira-client.py`. This is the **only** permitted
use of the Bash tool beyond read-only `git show` operations.

- Allowed: `bash -c "python3 scripts/jira-client.py <command>"`
- Allowed: `git show <commit>:<path>` for lock file inspection
- Forbidden: any other Bash file modification commands

## Comment Footnote

**Every** comment posted to Jira by this skill MUST include the Comment Footnote.
This applies to all Jira comments — the post-triage summary, cross-stream notices,
and any other comments the skill creates.

Follow the format in `shared/comment-footnote.md`, using skill name `triage-security`.

## Step 0 – Validate Project Configuration

Before proceeding, read the project's CLAUDE.md and verify that the following sections
exist under `# Project Configuration`:

1. `## Repository Registry` — must contain a table with at least one entry
2. `## Jira Configuration` — must contain at minimum: Project key, Cloud ID
3. `## Code Intelligence` — must exist with the tool naming convention
4. `## Security Configuration` — must contain at minimum:
   - `### Product Lifecycle` with Product pages URL, Jira version prefix,
     Jira Vulnerability issue type ID, and Component label pattern
   - `### Version Streams` with at least one Konflux release repo path
   - `### Source Repositories` with at least one source repo entry

If any of these sections are missing or incomplete, inform the user:

> "This skill requires Security Configuration in your CLAUDE.md. Please run `/setup`
> first to configure your project, then re-run this skill."

**Stop execution immediately.** Do not attempt to gather the missing information or
proceed without it.

Extract the following from the configuration for use in later steps:

- **Project key** — from Jira Configuration
- **Cloud ID** — from Jira Configuration
- **Jira version prefix** — from Security Configuration (e.g., `MYPRODUCT`)
- **Jira Vulnerability issue type ID** — from Security Configuration (e.g., `10001`)
- **Product pages URL** — from Security Configuration
- **Component label pattern** — from Security Configuration (e.g., `pscomponent:`)
- **VEX Justification custom field** _(optional)_ — from Security Configuration (e.g.,
  `customfield_00000`). If configured, used in Steps 6 and 7 when closing issues as
  "Not a Bug". If not configured, close with resolution only, without the VEX field.
- **Version Streams** — Konflux release repo URLs and local paths from Security Configuration
- **Source Repositories** — source repo names and URLs from Security Configuration

## Step 0.5 – JIRA Access Initialization

Follow the JIRA Access protocol in `shared/jira-access-strategy.md`.

**REST API equivalents for this skill's operations:**
- `jira.get_issue(id)` → `python3 scripts/jira-client.py get_issue <id> --fields "*all"`
- `jira.search_jql(jql)` → `python3 scripts/jira-client.py search_jql --jql "<jql>" --fields "summary,status,labels,versions" --max-results 50`
- `jira.edit_issue(id, fields)` → `python3 scripts/jira-client.py update_issue <id> --fields-json '<json>'`
- `jira.create_issue(...)` → `python3 scripts/jira-client.py create_issue --project <key> --summary "<summary>" --description-md "<desc>" --issue-type "<type-id>" --labels <labels>`
- `jira.create_link(...)` → `python3 scripts/jira-client.py create_link --inward <key> --outward <key> --link-type <type>`
- `jira.transition_issue(id, status)` → First `get_transitions <id>`, then `transition_issue <id> --transition-id <id>`
- `jira.add_comment(id, text)` → `python3 scripts/jira-client.py add_comment <id> --comment-md "<text>"`
- `jira.get_issue_remote_links(id)` → not available via REST client; if MCP is
  unavailable, warn the user and skip upstream reference extraction

**Exception for Bash tool:** When using REST API fallback, this skill may use
`bash -c "python3 scripts/jira-client.py <command>"` for JIRA operations only.

## Inputs

The user provides a single Vulnerability issue key.

Example:

```
/sdlc-workflow:triage-security PROJ-123
```

### Discovery mode (no issue key provided)

If the user invokes the skill without an issue key, run two queries:

**1. Untriaged issues** (primary list):
```
jira.search_jql(
  jql: "project = <project-key> AND issuetype = <vulnerability-issue-type-id> AND labels NOT IN (ai-cve-triaged) ORDER BY status ASC, created DESC",
  fields: ["summary", "labels", "status", "created"],
  maxResults: 20
)
```

**2. Triaged but still New** (stale issues — triaged but never actioned):
```
jira.search_jql(
  jql: "project = <project-key> AND issuetype = <vulnerability-issue-type-id> AND labels IN (ai-cve-triaged) AND status = New ORDER BY created DESC",
  fields: ["summary", "labels", "status", "created"],
  maxResults: 10
)
```

Present both lists to the engineer, clearly separated:
- **Untriaged** — numbered list grouped by status, showing: issue key, status,
  CVE ID (from labels), summary, and created date.
- **Triaged but still New** — same format, flagged so the engineer can spot
  issues that were triaged but never moved forward. These may need follow-up
  or re-triage.

#### Status-aware handling

When the user selects an issue (or when a specific issue key is provided in
Step 1), check its current Jira status and adapt accordingly:

- **New** — proceed with full triage (default path)
- **In Progress / Code Review / QA** — warn the user: "This issue is already
  in `<status>`. It may be actively worked on." Ask whether to:
  1. Proceed with triage anyway (e.g., to verify version impact or update
     Affects Versions)
  2. Skip this issue
- **Closed / Done / Resolved** — warn the user: "This issue is already closed."
  Ask whether to:
  1. Re-triage (e.g., to verify the fix covers all versions)
  2. Skip this issue

If the user chooses to skip, return to the discovery list or end the session.

If no results are found, inform the user: "No untriaged Vulnerability issues found
in project <project-key>."

## Step 1 – Data Extraction

Fetch the Vulnerability issue from Jira:

```
jira.get_issue(<jira-issue-id>)
```

Also fetch remote links to capture upstream references:

```
jira.get_issue_remote_links(<jira-issue-id>)
```

Parse the issue to extract the following fields:

| Field | Source |
|-------|--------|
| CVE ID | Labels (pattern `CVE-YYYY-XXXXX`) and summary text |
| Affected component | Label matching the Component label pattern from Security Configuration (e.g., `pscomponent:org/image-name`) |
| Product version (PSIRT-claimed) | Summary suffix in brackets (e.g., `[myproduct-2.2]`) |
| Affects Versions (Jira field) | Jira `versions` field — the current Affects Versions on the issue |
| Vulnerable library | Description text (library name, e.g., "quinn-proto") |
| Affected version range | Description text (e.g., "< 0.11.14", "versions before 3.2.1") |
| Fixed version | Description text (e.g., "fixed in 0.11.14") |
| Upstream fix PR | Remote links — GitHub PR URLs |
| Advisory URL | Remote links — GHSA or advisory URLs |
| CVE record URL | Remote links — cve.org URLs |
| Due date | Issue `duedate` field |
| Existing comments | Issue comment history |

**Present** the extracted data to the engineer in a structured table for verification
before proceeding. If any critical field cannot be parsed (CVE ID, library, affected
range), ask the engineer to supply the missing information and **stop execution** until
provided.

### Stream scope resolution

If the issue summary contains a stream suffix in brackets (e.g., `[myproduct-2.0]`,
`[myproduct-2.2]`), map it to one of the configured Version Streams. The suffix
identifies which stream PSIRT intended this issue to track.

1. Parse the suffix — e.g., `[myproduct-2.2]` → stream `2.2.x`
2. Match it to the Version Streams table from Security Configuration
3. Record the **issue stream scope** for use in Steps 2–7

If the suffix does not match any configured stream, present the mismatch to the
engineer and ask which stream this issue should be scoped to. **Do not proceed
past Step 1 until the engineer confirms the stream scope.** A non-matching suffix
(e.g., `[myproduct-2.0]` when no `2.0.x` stream exists) is **not** the same as having
no suffix — the issue is still stream-scoped, it just needs the correct stream
assigned. Never fall through to the unscoped path below because the suffix failed
to match.

If the summary has **no** stream suffix, the issue is treated as **unscoped** —
it covers all streams. Steps 3 and 4 behave differently for scoped vs unscoped
issues (see those steps for details).

```mermaid
flowchart TD
    A["Parse issue summary"] --> B{"Stream suffix\nin brackets?"}
    B -->|Yes| C{"Matches configured\nVersion Stream?"}
    B -->|No| D["Unscoped — analyze\nall streams"]
    C -->|Yes| E["Scoped — analyze\nonly that stream"]
    C -->|No| F["Ask engineer to\nconfirm stream"]
    F --> E
    D --> G["Steps 3-4 apply\nto all streams"]
    E --> H["Steps 3-4 scoped\nto single stream"]
```

### Ecosystem detection

Determine the ecosystem from the vulnerable library name and component context.
The supported ecosystems are defined in each stream's `security-matrix.md` Ecosystem
Mappings table — the skill reads available ecosystems from configuration rather than
assuming a fixed set. Common ecosystems include:

- **Cargo** — Rust crates (e.g., quinn-proto, tokio, serde)
- **npm** — JavaScript/TypeScript packages (e.g., axios, webpack, react)
- **RPM** — System packages in container images (e.g., openssl, curl, glibc)

The ecosystem determines which lock file to inspect and which parsing command to use.
Both the lock file path and check command are configured per ecosystem in each stream's
`security-matrix.md` Ecosystem Mappings table.

```mermaid
flowchart TD
    A["Identify ecosystem\nfrom library + component"] --> B{"Source dependency?\n(Cargo, npm, Go, ...)"}
    B -->|Yes| C["Lock file inspection\n(git show commit:lock-file)"]
    B -->|No| D{"RPM / system\npackage?"}
    D -->|Yes| E{"RPM lock file\nconfigured?"}
    E -->|Yes| F["Lock file + SBOM\ninspection"]
    E -->|No| G["SBOM-only +\nDockerfile analysis"]
    C --> H["Remediation: 2 tasks\n(upstream + downstream)"]
    F --> I["Remediation: 1 task\n(Konflux repo)"]
    G --> I
```

## Step 2 – Version Impact Analysis

This step determines which supported product versions actually ship the vulnerable
dependency by reading lock files at pinned source commits.

### 2.1 – Load the supportability matrix

Read `security-matrix.md` from each Konflux release repo listed in the project's
Security Configuration. Each `security-matrix.md` covers one version stream and
contains:

- **Version stream** — which product versions this repo covers (e.g., `2.1.x`)
- **Supportability matrix** — a table mapping each version to source commits
  per repository, with build dates
- **Ecosystem mappings** — lock file paths and check commands per ecosystem
- **Forward pointer** — the next stream's Konflux release repo URL (if any)

**Follow forward pointers** to chain across all streams. Starting from the first
repo in Version Streams, read its `security-matrix.md`, then follow its forward
pointer to the next repo, and repeat until no more forward pointers exist. This
ensures full coverage of all supported version streams.

To follow a forward pointer, match the repo URL against the **Konflux Release Repo**
column in the Version Streams table to find the corresponding **Local Path**. If the
URL is not in the table, ask the user for the local path or skip that stream.

If the Version Streams table in Security Configuration is empty or incomplete, ask
the user which Konflux release repos to scan. Present any discovered repos (from
forward pointers) and let the user confirm or add to the list before proceeding.

Aggregate all versions from all streams into a single working matrix.

#### On-demand matrix population

If a stream's Supportability Matrix is empty or missing rows (e.g., the template
was scaffolded but never populated), research and fill it in before proceeding:

1. Query the Konflux release repo's git history (tags, release branches) to discover
   released versions
2. For each version, extract image digest, build date, and source commits per
   repository from the repo's build metadata
3. Identify retags (versions with identical source commits)
4. Write the discovered rows into the `security-matrix.md` file
5. Present the populated matrix to the user for confirmation before writing

This is the **only** file the triage-security skill writes to — source code and
Jira are the only other output channels (Jira for mutations, source repos are
read-only).

### 2.2 – Detect the development stream

Query Jira for unreleased versions to identify the current development stream:

1. Call `getJiraIssueTypeMetaWithFields` for the Vulnerability issue type in the
   project (see Step 3 for the full call pattern).
2. From the returned `versions` field's `allowedValues`, find versions where
   `released: false`.
3. Filter by the Jira version prefix (e.g., `MYPRODUCT`).
4. Among the unreleased versions, select the one with the **earliest `releaseDate`**
   — this is the current development version.
5. Identify which stream's repo and branch correspond to this development version
   using the forward pointer chain (the development stream is typically the last
   stream, covered by the most recent Konflux release repo).

The development stream is checked at **branch HEAD** (not a pinned commit) since
there is no released version yet.

### 2.3 – Extract dependency versions

For each version in the aggregated matrix (plus the development stream):

1. **Identify the investigation method** from the ecosystem mappings in the
   relevant stream's `security-matrix.md`. The method is determined by the
   **configuration**, not by search results:
   - If `Lock File` is configured → use the lock file. **The lock file is the
     source of truth.** If the package is not found in the lock file, it is not a
     dependency — mark as NOT affected.
   - If `Lock File` is empty → the ecosystem has no lock file (e.g., RPM). Check
     the Source Pinning Method section for alternative investigation approaches,
     or report to the engineer that the dependency version cannot be determined.

2. **Lock file path** — run the check command via `git show`, substituting the
   pinned commit and package name. The exact command comes from the `Check Command`
   column in the stream's Ecosystem Mappings table.

   Example commands for common ecosystems:

   **Cargo (Cargo.lock — TOML):**
   ```bash
   git show <commit>:Cargo.lock | grep -A2 'name = "<library>"'
   ```
   Output: version line from the TOML block.

   **npm (package-lock.json — JSON):**
   ```bash
   git show <commit>:package-lock.json | python3 -c "
   import sys, json
   d = json.load(sys.stdin)
   pkgs = d.get('packages', d.get('dependencies', {}))
   for path, info in pkgs.items():
       if '<library>' in path.split('/')[-1]:
           print(f\"{path}: {info.get('version', '?')}\")
   "
   ```

   **RPM (rpms.lock.yaml — YAML):**
   ```bash
   git show <commit>:rpms.lock.yaml | grep '<library>'
   ```

   **For the development stream**, use branch HEAD instead of a pinned commit:
   ```bash
   git show HEAD:<lock-file> | <check-command-for-ecosystem>
   ```
   Run this in the source repository directory for the development stream.

3. **SBOM fallback** — when no lock file is configured for an ecosystem (the
   `Lock File` column is empty), the image SBOM may still contain dependency
   information. If `cosign` is available, try querying the container image SBOM:

   ```bash
   cosign download sbom <image-reference>@<image-digest> | grep '<library>'
   ```

   This requires `cosign` to be installed and registry access to the container image.
   If SBOM is not available, report to the engineer that the dependency version cannot
   be determined for this ecosystem/stream and ask for guidance.

4. **Handle retags**: if a version is marked as a retag in the supportability matrix
   (e.g., `2.2.2 = retag of 2.2.1`), **skip** the version check and carry forward
   the result from the retagged version. Note in the output: "same as [version]".

5. **Compare** each extracted dependency version against the CVE's affected range
   to determine whether that product version is affected.

### 2.3.5 – Dependency chain context

For affected versions (where the vulnerable dependency is in the lock file and
within the affected range), trace the dependency chain to give the engineer context
about how the vulnerable package entered the tree. This information helps assess
remediation complexity — a direct dependency is a simple bump, while a deep
transitive dependency may require coordinating updates across intermediate packages.

For each affected version, trace how the vulnerable dependency entered the build
to give the engineer remediation context.

The investigation method depends on the ecosystem:

#### Source-level dependencies (Cargo, npm, Go)

Inspect the lock file and manifest files to determine:

1. **Direct vs transitive** — is the vulnerable package a direct dependency of a
   workspace member, or pulled in transitively?
2. **Dependency path** — the chain from a workspace root to the vulnerable package
   (e.g., `workspace-root → reqwest → hyper → h2 → vulnerable-lib`)
3. **Profile/scope** — whether the dependency is included in all build profiles or
   only specific ones:
   - **Cargo**: `[dev-dependencies]` (test/bench only, not shipped),
     `[build-dependencies]` (build scripts only), feature-gated optional deps
   - **npm**: `devDependencies` (build/test only), `optionalDependencies`

   If the dependency is only present in a non-production profile (e.g., dev-only),
   note this — it changes the risk assessment.
4. **Introduction point** — if a dependency is present in one version but not
   another, note when it was introduced (helps identify which upgrade or feature
   addition brought it in)

Example output:
```
Dependency chain for quinn-proto:
  backend (workspace) → reqwest [features: http3] → h3 → quinn → quinn-proto
  Profile: production (reqwest is a runtime dependency)

First appeared: 2.2.0 (commit 05a3af91 added reqwest http3 feature)
Not present in: 2.1.x (reqwest used without http3 feature)
```

#### Container-level dependencies (RPM, system packages)

For RPM and system-level packages, classify origin to determine the remediation
path. The classification method depends on whether an RPM lock file is configured
for the stream.

1. **Confirm presence** — the SBOM or rpms.lock.yaml from Step 2.3 already confirms
   the package is in the image and at what version.

2. **Classify the package origin**:

   **When an RPM lock file exists** (rpms.lock.yaml or equivalent):
   - **In lock file** → **explicit install**. Remediation: update the package spec
     in the lock file (or rpms.in.yaml).
   - **Not in lock file but in SBOM** → **base image**. The package is inherited
     from the `FROM` image.

   **When no RPM lock file exists** (SBOM-only streams):
   - Check the Dockerfile to classify:
     ```bash
     git show <commit>:Dockerfile | grep -i '<package-name>\|FROM\|dnf\|yum\|microdnf'
     ```
   - **In a `dnf install` / `yum install` command** → **explicit install**.
   - **Not in any install command** → **base image**.

3. **Base image reference** (when origin is base image) — extract the `FROM`
   reference from the Dockerfile to identify the update path:
   ```bash
   git show <commit>:Dockerfile | grep -i '^FROM'
   ```
   Record:
   - **Image reference** — the full registry/repository path
     (e.g., `registry.access.redhat.com/ubi9/ubi-minimal`)
   - **Tag or digest** — how the image is pinned
     (e.g., `9.4-1227`, `@sha256:abc123`, or `latest`)
   - **Pinning method** — `digest` (immutable), `version tag` (mutable but specific),
     or `floating tag` (e.g., `latest` — rebuilding may pick up the fix automatically)

   This determines the remediation path:
   - **Floating tag** → a Konflux rebuild may pick up the fix if the base image was
     already updated upstream. Verify by checking the base image's errata or SBOM.
   - **Version tag** → update the tag to a version that includes the fix. Check the
     base image's container catalog or errata for available versions.
   - **Digest** → update the digest to a build that includes the fix.

   The skill does **not** resolve which specific base image version has the fix — that
   depends on the base image vendor's errata pipeline. Include the current reference
   in the remediation task so the engineer or `/implement-task` can research it.

4. **Introduction point** — check if the package origin differs across versions
   (e.g., moved from explicit install to base image inheritance between streams).

Example output (RPM, base image origin):
```
Dependency chain for openssl (RPM):
  SBOM confirms: openssl-libs-3.0.7-27.el9.x86_64
  rpms.lock.yaml: NOT present → base image
  Dockerfile: FROM registry.access.redhat.com/ubi9/ubi-minimal:9.4-1227
  Origin: base image (openssl-libs inherited from ubi9-minimal)
  Pinning: version tag (9.4-1227)

Remediation: update base image tag to a version with patched openssl.
Check base image errata or container catalog for available updates.
```

Note that the lock file contents and base image can differ across streams — always
check at the specific stream's pinned commit.

### 2.4 – Present the version impact table

Build and present the version impact table to the engineer:

```
Version Impact for CVE-YYYY-XXXXX (<library> <affected-range>):

| Version | <library> | Affected? | Notes |
|---------|-----------|-----------|-------|
| 2.1.0   | 0.11.9    | YES       |       |
| 2.1.1   | 0.11.9    | YES       |       |
| 2.2.0   | 0.11.9    | YES       |       |
| 2.2.1   | 0.11.12   | YES       |       |
| 2.2.2   | —         | YES       | retag of 2.2.1 |
| 2.2.3   | 0.11.14   | NO        |       |
| 2.2.4   | 0.11.14   | NO        |       |
| 3.0 (dev) | 0.11.14 | NO        | branch HEAD |
```

Include the dependency chain context from Step 2.3.5 below the table so the
engineer can see both the impact and the remediation path at a glance.

### 2.5 – Upstream fix check

For each affected stream, check whether the upstream source repository has
already fixed the vulnerability on the branch that feeds that stream. Read the
**Upstream Branch** column from the stream's Ecosystem Mappings table.

For each affected ecosystem with an Upstream Branch configured:

1. Check the dependency version at the upstream branch HEAD. Use the **Repository**
   column from the Ecosystem Mappings row to determine which source repo to inspect:
   ```bash
   git -C <source-repo-local-path> show <upstream-branch>:<lock-file> | grep -A2 '<library>'
   ```
2. Compare against the affected version range from the CVE.

Present the upstream fix status below the version impact table:

```
Upstream fix status:

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.2.x  | Cargo     | release/0.4.z   | 0.11.14         | YES    |
| 3.0.x  | Cargo     | main            | 0.11.14         | YES    |
```

This determines the remediation path for each stream:
- **Fixed upstream** → remediation is a Konflux release repo change: bump the
  source tag/commit reference to pick up the fix. Include the upstream commit
  or tag in the remediation task.
- **Not fixed upstream** → remediation requires an upstream PR first to bump
  the dependency, then a Konflux release repo update. Note this in the
  remediation task.

Wait for the engineer to review and confirm the table before proceeding to Step 3.

## Step 3 – Affects Versions Correction

### 3.1 – Discover available Jira versions

Before correcting Affects Versions, dynamically discover what version values exist
in the Jira project. This is done via API — no hardcoded version IDs.

1. Call `getJiraIssueTypeMetaWithFields` for the Vulnerability issue type:
   ```
   jira.getJiraIssueTypeMetaWithFields(
     projectIdOrKey: "<project-key>",
     issueTypeId: "<vulnerability-issue-type-id>"
   )
   ```
2. Extract the `versions` field's `allowedValues` array. Each entry contains:
   - `id` — the Jira version ID (used for mutations)
   - `name` — the display name (e.g., `MYPRODUCT 2.1.0`)
   - `released` — boolean indicating release status
   - `releaseDate` — planned or actual release date
3. Filter by the Jira version prefix (e.g., `MYPRODUCT`) to exclude unrelated versions
   (Helm Charts, Operators, DA releases, etc.).

Present the filtered version registry:

```
Jira Versions matching "<prefix>":

| Jira ID | Name        | Released | Release Date |
|---------|-------------|----------|--------------|
| 62643   | MYPRODUCT 2.1.0 | yes      | 2025-07-27   |
| 62604   | MYPRODUCT 2.1.1 | yes      | 2025-09-16   |
| ...     | ...         | ...      | ...          |
| 104611  | MYPRODUCT 3.0   | no       | 2026-06-30   |
```

### 3.2 – Compare and correct Affects Versions

**Scope the correction to the issue's stream.** If the issue has a stream scope
(from Step 1 stream scope resolution), only include versions belonging to that
stream. If the issue is unscoped, include all affected versions across all streams.

Example for a **scoped** issue with suffix `[myproduct-2.2]`:
- Version impact table shows: MYPRODUCT 2.1.0 (YES), 2.1.1 (YES), 2.2.0 (YES), 2.2.1 (YES)
- This issue is scoped to stream `2.2.x` → only propose: `[MYPRODUCT 2.2.0, MYPRODUCT 2.2.1]`
- The 2.1.x versions belong to a sibling issue (see Step 4)

Compare the PSIRT-assigned Affects Versions (from the Jira `versions` field) against
the **stream-scoped** version impact table:

- **If PSIRT version is wrong** (e.g., "MYPRODUCT 2.0.0" when 2.0 doesn't exist):
  - Show the diff: `Current: [MYPRODUCT 2.0.0] → Proposed: [MYPRODUCT 2.2.0, MYPRODUCT 2.2.1]`
  - Present correction to engineer for confirmation

- **If PSIRT version is correct but incomplete**:
  - Show the additions: `Current: [MYPRODUCT 2.2.0] → Proposed: [MYPRODUCT 2.2.0, MYPRODUCT 2.2.1]`
  - Present correction to engineer for confirmation

- **If the version impact table includes versions not registered in Jira**:
  - Flag: "MYPRODUCT X.Y.Z is in the supportability matrix but has no matching Jira
    version — notify project admin"
  - Continue with available versions; do not block triage

- **If Affects Versions are already correct**: note this and proceed without changes.

**After engineer confirmation**, update the Affects Versions:

```
jira.edit_issue(<jira-issue-id>, fields={
  "versions": [{"id": "<version-id-1>"}, {"id": "<version-id-2>"}, ...]
})
```

Use the Jira version IDs discovered in Step 3.1, not hardcoded values.

**Include development stream versions**: if the issue's stream includes the
development stream and it is affected (from Step 2.2), include the unreleased
Jira version in the Affects Versions correction. Unreleased versions are valid
Affects Versions values — they track that the CVE must be fixed before the next
release ships.

Add a comment documenting the correction:

```
jira.add_comment(<jira-issue-id>, "Corrected Affects Versions: [old] → [new].
Based on lock file analysis at pinned commits from security-matrix.md.
Scoped to stream <stream> per issue suffix.")
```

## Step 4 – Duplicate and Sibling Check

Search for sibling Vulnerability issues with the same CVE label:

```
jira.search_jql(
  "project = <project-key> AND labels = '<CVE-ID>' AND issuetype = <vulnerability-issue-type-id> AND key != <current-issue-key>"
)
```

For each sibling found, parse its summary stream suffix (e.g., `[myproduct-2.0]`) to
determine its stream scope. Classify siblings into:

- **Same-stream siblings** — same stream suffix as the current issue (or both unscoped)
- **Different-stream siblings** — different stream suffix (companion trackers)

### 4.1 – Same-stream duplicates

If a same-stream sibling exists and is open or in progress:
- **Recommendation**: Close the current issue as Duplicate.
- Present the sibling issue key and its Affects Versions to the engineer.
- After confirmation:
  1. Add comment: "Duplicate of [sibling-key] — same CVE tracked for the same
     stream [stream]. Version impact analysis confirms overlap."
  2. Transition to Closed with resolution "Duplicate".
  3. Assign to current user.

### 4.2 – Cross-stream coordination

Different-stream siblings are **companion trackers**, not duplicates. PSIRT creates
one issue per stream intentionally. For each different-stream sibling:

1. **Link** the current issue to the sibling with a "Related" link type:
   ```
   jira.create_link(
     inwardIssue: <current-issue-key>,
     outwardIssue: <sibling-key>,
     type: "Related"
   )
   ```
2. **Verify no Affects Versions overlap** — each issue should only carry versions
   from its own stream. If overlap is detected (e.g., both issues claim MYPRODUCT 2.2.0),
   flag it to the engineer: "Version overlap detected between [current-key] and
   [sibling-key] — both claim [overlapping versions]. Please confirm which issue
   should own these versions."
3. **Present the sibling landscape** to the engineer:
   ```
   CVE-YYYY-XXXXX companion issues:

   | Issue     | Stream | Status      | Affects Versions          |
   |-----------|--------|-------------|---------------------------|
   | TC-1234   | 2.1.x  | In Progress | MYPRODUCT 2.1.0, MYPRODUCT 2.1.1 |
   | TC-5678 ← | 2.2.x  | New         | MYPRODUCT 2.2.0, MYPRODUCT 2.2.1 |
   ```

**If no siblings found**, proceed to Step 5.

## Step 5 – Version Lifecycle Check

Verify that the affected product versions are still within their support lifecycle.

1. Fetch the product lifecycle page using the Product pages URL from Security
   Configuration:
   ```
   WebFetch(url: "<product-pages-url>", prompt: "Extract the list of supported
   product versions and their support status (active, maintenance, EOL)")
   ```
2. For each affected version (from the version impact table), check whether it
   appears as actively supported.

**If ALL affected versions are EOL or unsupported**:
- **Recommendation**: Close as Won't Do.
- After confirmation:
  1. Add comment: "All affected versions ([versions]) are EOL per product pages —
     no fix required."
  2. Transition to Closed with resolution "Won't Do".
  3. Assign to current user.

**If SOME affected versions are EOL**: note the EOL versions but continue with
triage for the supported versions. Remove EOL versions from Affects Versions if
they were included.

**If ALL affected versions are supported**: proceed to Step 6.

## Step 6 – Already Fixed Check

Cross-reference resolved sibling Vulnerability issues for the same CVE against the
version impact table.

1. Reuse the JQL results from Step 4 (sibling issues).
2. For siblings with status "Closed" and resolution "Done":
   - Check their Affects Versions.
   - Cross-reference against the version impact table.

**If the current issue's affected versions are all already covered by resolved
siblings**, and the version impact table shows "NO" (not affected) for remaining
versions:
- **Recommendation**: Close as Not a Bug (already fixed by sibling).
- After confirmation:
  1. Add comment: "All affected versions are already covered by resolved sibling
     [sibling-key]. No additional fix required."
  2. Transition to Closed with resolution "Not a Bug".
  3. Assign to current user.
  Do **not** set VEX Justification for already-fixed closures — VEX applies only when
  the vulnerability does not affect the product.

**If the fix is partial** (some versions covered, others not), narrow the scope to
the unfixed versions and proceed to Step 7.

**If no resolved siblings exist**, proceed to Step 7.

## Step 7 – Remediation

Based on the version impact table and the remaining affected versions (after
Steps 4–6 filtering), determine the appropriate action.

```mermaid
flowchart TD
    A["Version impact table\n(after Steps 4-6)"] --> B{"Any supported versions\naffected?"}
    B -->|Yes| C{"Other streams\nalso affected?"}
    B -->|No| D["Case C: Close as\nNot a Bug"]
    C -->|Yes| E["Case B: Post cross-stream\nimpact comment"]
    C -->|No| F["Case A: Create\nremediation tasks"]
    E --> F
    F --> G{"Source dependency?\n(Cargo, npm, Go)"}
    G -->|Yes| H["2 tasks: upstream\nbackport + downstream\npropagation"]
    G -->|No| I["1 task: Konflux\nrepo fix"]
    D --> J{"VEX Justification\nconfigured?"}
    J -->|Yes| K["Set VEX field"]
    J -->|No| L["Close with\nresolution only"]
```

**Important**: This skill never creates Vulnerability issues. PSIRT owns
Vulnerability issue creation — the skill only creates remediation **Tasks**.

### Case A: Affected — create remediation tasks

If the issue's stream-scoped versions (or all versions for unscoped issues)
are affected:
- Keep the current Vulnerability issue as-is (with corrected Affects Versions
  from Step 3).
- Create one remediation Task per affected stream within the issue's scope
  (see Remediation Task Creation below).
- Link each Task to the Vulnerability issue.

### Case B: Cross-stream impact notice

If the version impact analysis reveals that **other streams** (outside this
issue's scope) are also affected, add a comment to the current issue noting
the cross-stream impact. Do **not** create new Vulnerability issues or
remediation tasks for those other streams — PSIRT manages per-stream
Vulnerability tracking.

Example comment:
```
Cross-stream impact: [library] [affected-range] also affects stream(s)
[other-stream-1], [other-stream-2] based on lock file analysis.
These streams are tracked by companion issues (see Related links)
or may require separate PSIRT triage.
```

This is informational only — the engineer and PSIRT decide next steps for
other streams.

### Case C: No supported versions affected

If the version impact table shows NO for all supported versions (including
the development stream):
- **Recommendation**: Close as Not a Bug (not affected).
- After confirmation:
  1. Add comment: "No supported versions ship a vulnerable version of [library].
     Version impact analysis: [table]. All supported versions ship [library]
     [version] which is outside the affected range ([range])."
  2. Transition to Closed with resolution "Not a Bug".
  3. If VEX Justification custom field is configured, set it to the appropriate
     value (see VEX Justification below).
  4. Assign to current user.

### VEX Justification

When closing a Vulnerability issue as "Not a Bug" (not affected) and the VEX
Justification custom field is configured in Security Configuration, set it to
the value that best matches the triage evidence:

| Value | When to use |
|---|---|
| Component not Present | The vulnerable package is not shipped in any affected version |
| Vulnerable Code not Present | The package is shipped but the vulnerable code path was not included (e.g., feature flag, conditional compilation) |
| Vulnerable Code not in Execute Path | The package is shipped with vulnerable code, but the product never invokes that code path |
| Inline Mitigations already Exist | The vulnerability is mitigated by existing controls (e.g., network isolation, input validation) |

Default to **Component not Present** when the lock file or SBOM analysis shows the
vulnerable package version is not included. Present the chosen justification to the
engineer as part of the close recommendation.

### Confirmation gate

Present the full recommendation (task details, cross-stream notice, or close
rationale) to the engineer for confirmation before executing any Jira mutations.

## Remediation Task Creation

When triage concludes "needs fix" (Case A above), create Jira Tasks
following `task-description-template.md` so that `/implement-task` can parse them
directly. Only create tasks for streams within the current issue's scope.

Read `remediation-templates.md` for the full task description templates. The key
distinction:

- **Source dependency ecosystems** (Cargo, npm, Go modules): create **two** tasks —
  an upstream backport task (fix in the source repo) and a downstream propagation
  subtask (update the reference in the Konflux release repo). The downstream subtask
  is blocked by the upstream task.
- **System package ecosystems** (RPM): create **one** task — the fix happens directly
  in the Konflux release repo (Dockerfiles, lock files). No upstream step needed.

### Jira issue creation

**Source dependency ecosystems** — create two tasks:

```
# 1. Upstream backport task
upstream_task = jira.create_issue(
  projectKey: "<project-key>",
  issueTypeName: "Task",
  summary: "Remediate CVE-YYYY-XXXXX: bump [library] to [fixed-version] ([stream])",
  description: <upstream-task-description>,
  labels: ["ai-generated-jira", "Security", "<CVE-ID>"]
)

# 2. Downstream propagation subtask
downstream_task = jira.create_issue(
  projectKey: "<project-key>",
  issueTypeName: "Task",
  summary: "Propagate CVE-YYYY-XXXXX fix: update [source-repo] ref in [konflux-repo] ([stream])",
  description: <downstream-task-description>,
  labels: ["ai-generated-jira", "Security", "<CVE-ID>"]
)
```

**System package ecosystems** — create one task:

```
task = jira.create_issue(
  projectKey: "<project-key>",
  issueTypeName: "Task",
  summary: "Remediate CVE-YYYY-XXXXX: update [package-name] to [fixed-version] ([stream])",
  description: <system-package-task-description>,
  labels: ["ai-generated-jira", "Security", "<CVE-ID>"]
)
```

### Jira linkage

After creating remediation tasks:

1. **Link** each task to the Vulnerability issue:
   ```
   jira.create_link(
     inwardIssue: <vulnerability-key>,
     outwardIssue: <task-key>,
     type: "Depend"
   )
   ```
2. **For source dependency ecosystems**, link the downstream subtask as blocked
   by the upstream task:
   ```
   jira.create_link(
     inwardIssue: <upstream-task-key>,
     outwardIssue: <downstream-task-key>,
     type: "Blocks"
   )
   ```
3. **Transition** the Vulnerability to In Progress (if not already).
4. **Assign** the Vulnerability to the current user (if not already assigned).
5. **Add comment** to the Vulnerability listing all created tasks:
   - Source dependency: "Remediation tasks created: [upstream-task-key] (upstream
     backport), [downstream-task-key] (downstream propagation, blocked by
     [upstream-task-key])"
   - System package: "Remediation task created: [task-key]"

## Post-Triage Summary

After all triage actions are complete:

### 1. Add the `ai-cve-triaged` label

Add the `ai-cve-triaged` label to the original Vulnerability issue to mark it as
triaged. This label enables filtering triaged vs untriaged issues in Jira and
prevents re-triaging the same issue.

### 2. Post a summary comment

Add a summary comment to the original Vulnerability issue documenting:

1. The version impact table
2. The Affects Versions correction (if any)
3. The triage outcome (closed or remediation created)
4. Links to all remediation tasks created (upstream + downstream for source
   dependency ecosystems, or single task for system packages)

This comment provides a complete audit trail for future reference. The comment
MUST include the Comment Footnote (see above).

## Important Rules

1. **Follow the step order.** Execute steps 1 through 7 in sequence. Do not skip
   steps or reorder them — later steps depend on data from earlier steps.
2. **Do not guess dependency versions.** Every version claim must come from actual
   `git show` output. If a lock file cannot be read (repo not cloned, commit not
   found), report the error and ask the user — do not assume a version.
3. **Do not assume PSIRT Affects Versions are correct.** Always verify against
   lock file evidence. PSIRT assigns versions based on scan time, not actual
   dependency analysis.
4. **Check ALL supported versions.** Do not stop at the version named in the issue
   summary. The supportability matrix defines the full scope — check every version,
   including the development stream.
5. **Handle retags explicitly.** When a version is a retag (identical source commits
   as another version), skip the lock file check and carry forward the result from
   the original version. Note "same as [version]" in the impact table.
6. **Use dynamic version discovery.** Never hardcode Jira version IDs. Always use
   `getJiraIssueTypeMetaWithFields` to discover available versions and their IDs
   at runtime.
7. **Never create Vulnerability issues.** PSIRT owns Vulnerability issue creation.
   This skill only creates remediation Tasks. Cross-stream impact is reported via
   comment on the current issue.
8. **One remediation Task per affected stream, plus a downstream propagation
   subtask** when the ecosystem is a source dependency (Cargo, npm, Go modules).
   The upstream task covers the source repo fix; the downstream subtask covers
   the Konflux release repo update and is blocked by the upstream task. System
   package ecosystems produce a single task. A single Task spanning multiple
   streams would be unimplementable by `/implement-task`.
9. **Follow `task-description-template.md` for generated tasks.** The remediation
   Task description must be parseable by `/implement-task`. Do not invent custom
   sections or deviate from the template format.
10. **Development stream uses branch HEAD.** Unlike released versions (which use
    pinned commits from the supportability matrix), the development stream is
    checked at branch HEAD of its source repositories.
11. **Every Jira mutation requires explicit confirmation.** Present the proposed
    change, wait for approval. If the engineer declines, record the decision and
    move to the next step.
12. **If the same `git show` command fails 3 times**, stop and ask the user for
    guidance — the repository may not be cloned or the commit may not exist
    locally.
13. **Version impact evidence uses pinned commits only.** For released versions,
    always use the exact commit from the supportability matrix, never HEAD or any
    branch tip. This ensures the analysis reflects what was actually shipped.
14. **Forward pointers are mandatory for full coverage.** When reading
    `security-matrix.md`, always follow forward pointers to the next stream's repo.
    Do not stop at the first repo — the full version landscape may span multiple
    repos.
15. **Every Jira comment MUST include the Comment Footnote.** No exceptions — this
    applies to all comments: Affects Versions corrections, duplicate notifications,
    EOL closures, already-fixed closures, cross-stream notices, remediation task
    links, and the post-triage summary.
