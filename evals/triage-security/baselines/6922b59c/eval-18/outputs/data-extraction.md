# Step 1 -- Data Extraction: TC-8001

## Step 0.8 -- Assignment and Transition

TC-8001 is currently in **In Progress** status and already assigned to engineer-a@example.com. Since the issue is already past the Assigned state, the assignment update and transition to Assigned are **skipped** -- the issue has already progressed beyond this step in a prior triage run.

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0, RHTPA 2.2.1 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 (< 0.11.14) |
| Fixed version | 0.11.14 |
| Upstream fix PR | quinn-rs/quinn#2048 (https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | GHSA-2026-qp73-x4mq (https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| CVSS | 7.5 (High) |
| Due date | 2026-07-15 |
| Assignee | engineer-a@example.com |
| Existing comments | 2 (description digest + post-triage summary from prior run) |

## Custom Fields

| Field | Value |
|-------|-------|
| Upstream Affected Component (customfield_10632) | quinn-proto |
| PS Component (customfield_10669) | pscomponent:org/rhtpa-server |
| Stream (customfield_10832) | rhtpa-2.2 |

## Stream Scope Resolution

- Issue summary suffix: `[rhtpa-2.2]`
- Mapped to configured Version Stream: **2.2.x** (Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`)
- Issue is **stream-scoped** to 2.2.x only

## Ecosystem Detection

- Vulnerable library: quinn-proto (Rust crate)
- Ecosystem: **Cargo**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch: `release/0.4.z`
- Source repository: rhtpa-backend

## Remote Links

| Type | URL |
|------|-----|
| GitHub Advisory | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE Record | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |

## Existing Issue Links

| Link Type | Target | Summary | Status |
|-----------|--------|---------|--------|
| Depend | TC-8100 | Backport quinn-proto fix to >= 0.11.14 on release/0.4.z [rhtpa-2.2] | In Progress |
| Depend | TC-8101 | Propagate quinn-proto bump to rhtpa-server release branch [rhtpa-2.2] | Open |

## Existing Comments

| # | Comment | Author | Created |
|---|---------|--------|---------|
| 1 | Description digest: sha256-md:a1b2c3d4e5f6... | sdlc-workflow/triage-security | 2026-07-01T10:00:00Z |
| 2 | Post-triage summary (CVE-2026-31812 triage complete) | sdlc-workflow/triage-security | 2026-07-01T10:01:00Z |

## Pre-existing Triage Indicators

The following artifacts indicate this issue was already triaged in a prior run:

- **Label**: `ai-cve-triaged` is present
- **Status**: In Progress (post-triage state)
- **Remediation tasks**: TC-8100 and TC-8101 linked via Depend
- **Description digest comment**: exists (comment #1)
- **Post-triage summary comment**: exists (comment #2)
