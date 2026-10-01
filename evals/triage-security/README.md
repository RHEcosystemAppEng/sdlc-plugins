# triage-security Evals

Evaluations for the `triage-security` skill. See the
[framework README](../README.md) for how evals work and how to run them.

## Test cases

| ID | Name | Purpose |
|----|------|---------|
| 1 | Standard triage | Standard Vulnerability issue with wrong Affects Versions. Tests the full triage flow: data extraction, version impact analysis, Affects Versions correction, and remediation task creation for Cargo ecosystem. |
| 2 | Already fixed | CVE where all supported versions ship a patched dependency. Tests the "close as Not a Bug" path (Step 7 Case C) with VEX Justification. |
| 3 | Duplicate detection | Vulnerability issue that duplicates an existing sibling issue for the same CVE and stream. Tests same-stream duplicate detection (Step 4.1) and early closure. |
| 4 | Issue splitting | Unscoped CVE affecting only some streams — 2.1.x affected, 2.2.x already fixed. Tests mixed version impact, scoped Affects Versions correction, and stream-targeted remediation. |

## Fixture files

Files in `files/` simulate Jira issue data, security matrix content, and
project configuration that the skill would read during a real invocation.
The eval prompt instructs the agent to write its analysis to output files
instead of calling Jira MCP or git.

### Vulnerability issue fixtures (`vuln-issue-*.md`)

Mock Jira Vulnerability issues in Markdown. Each contains issue metadata
and a PSIRT-style description with CVE details, affected packages, and
version ranges.

- **vuln-issue-standard.md** — standard CVE with wrong PSIRT-assigned
  Affects Versions; requires full triage and remediation task creation
- **vuln-issue-already-fixed.md** — CVE where all versions ship patched
  dependency; triggers close as Not a Bug
- **vuln-issue-duplicate.md** — CVE with an existing sibling issue
  tracking the same CVE for the same stream; triggers duplicate closure
- **vuln-issue-split.md** — unscoped CVE with mixed impact across
  streams; requires scoped remediation for affected streams only

### Security matrix (`security-matrix-mock.md`)

Mock `security-matrix.md` with two version streams (2.1.x and 2.2.x),
each with a supportability matrix mapping versions to source commits,
ecosystem mappings for Cargo and RPM lock files, and forward pointers
between streams.

### Project configuration (`claude-md-security-config.md`)

Mock CLAUDE.md with Repository Registry, Jira Configuration, Code
Intelligence, and Security Configuration sections — the full
configuration that `triage-security` validates in Step 0.

## Key constraints tested

| Constraint | Eval IDs |
|------------|----------|
| §1.37 — Jira-only output | 1, 2, 3, 4 |
| §1.38 — read-only source access | 1, 4 |
| §1.39 — every mutation requires confirmation | 1, 2, 3, 4 |
| §1.42 — dynamic version discovery | 1, 4 |
| §1.43 — post-triage summary comment | 1, 2, 3 |
| §1.44 — remediation follows template | 1, 4 |
| §1.45 — do not fabricate data | 1, 4 |
| §1.46 — one task per stream | 1, 4 |
| §1.47 — retag handling | 1, 4 |
| §1.48 — ecosystem detection | 1 |
| §1.49 — step order | 1, 2, 3, 4 |

## Running

```
/sdlc-workflow:run-evals Run evals for triage-security.
Evals path: evals/triage-security/evals.json
Workspace: /tmp/triage-security-eval
```
