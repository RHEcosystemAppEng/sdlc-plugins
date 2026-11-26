# Unsupported Ecosystem Notification – TC-8040

> "**Unsupported ecosystem**: Go modules is not yet supported for automated triage.
> Manual assessment is required."

## Details

| Item | Value |
|------|-------|
| Issue | TC-8040 |
| CVE | CVE-2026-31812 |
| Vulnerable library | quinn-proto (affected `< 0.11.14`, fixed in `0.11.14`) |
| Component | `pscomponent:org/rhtpa-server` |
| Issue stream scope | 2.2.x (`[rhtpa-2.2]`) |
| Detected ecosystem | Go modules |
| Supported ecosystems (Ecosystem Mappings, 2.2.x) | Cargo, RPM |
| Supported ecosystems (Ecosystem Mappings, 2.1.x) | Cargo, RPM |

## Why automated triage stopped

- Go modules has no row in any stream's `security-matrix.md` Ecosystem Mappings table, so
  there is no configured lock file or check command for `git show` inspection.
- Go modules is not in the skill's ecosystem classification table, so the remediation task
  structure (2 tasks for source dependencies, 1 for system packages) is undefined.
- The skill does not fabricate data and does not guess dependency versions, so a version
  impact analysis cannot be produced.

Automated triage stopped at Step 1 (Ecosystem detection). Steps 1.5 through 8 were not run.

## Jira state

- No Jira mutations were proposed or made. Affects Versions (currently `RHTPA 2.0.0`),
  links, comments, and status are unchanged.
- The `ai-cve-triaged` label was **not** added, so the issue stays in the untriaged
  discovery list for manual follow-up.

## Recommended manual next steps

1. **Confirm the ecosystem.** quinn-proto is a Rust crate with a RUSTSEC advisory, which
   would normally mean Cargo (supported). If the Go modules result is wrong, re-run
   `/sdlc-workflow:triage-security TC-8040` once the ecosystem is corrected.
2. **If Go modules is correct**, assess manually. For each supported version (2.1.0, 2.1.1,
   2.2.0, 2.2.1, 2.2.2 (retag of 2.2.1), 2.2.3, 2.2.4) and the development stream, inspect
   `go.mod`/`go.sum` at the pinned commit and compare the dependency version against `< 0.11.14`.
3. **Correct Affects Versions manually.** `RHTPA 2.0.0` is not in any configured stream.
4. **To enable automated triage for Go modules later**, add a Go modules row (repository,
   lock file such as `go.sum`, check command, upstream branch) to each stream's
   `security-matrix.md` Ecosystem Mappings table. Also add Go modules to the skill's ecosystem
   classification table (probably as a source dependency).
5. **Separate warning:** the security matrix is stale (last updated 2026-06-28, 151 days
   ago). Consider refreshing it via `/setup` (Step 10.6) before any re-triage.
