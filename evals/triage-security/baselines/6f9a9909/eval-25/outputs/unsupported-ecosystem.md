# Unsupported Ecosystem Notification

## Issue: TC-8040

**CVE**: CVE-2026-31812
**Library**: quinn-proto
**Detected Ecosystem**: Go modules

---

**Unsupported ecosystem**: Go modules is not yet supported for automated triage. Manual assessment is required.

---

## Context

The triage-security skill detected the ecosystem as **Go modules** for the vulnerable library `quinn-proto` in issue TC-8040. However, the Ecosystem Mappings tables in the configured version streams only support the following ecosystems:

- **Cargo** -- Rust crates, with lock file `Cargo.lock`
- **RPM** -- System packages, with lock file `rpms.lock.yaml`

Go modules does not appear in the Ecosystem Mappings table for any configured stream (2.1.x or 2.2.x). Without an ecosystem mapping, the skill cannot determine:

1. Which lock file to inspect (e.g., `go.sum`, `go.mod`)
2. Which check command to use for dependency version extraction
3. Which upstream branch to verify fix status against
4. The ecosystem classification (source dependency vs. system package) for remediation task structure

## Recommended Actions

1. **Manual assessment** -- Manually inspect the affected versions to determine if the vulnerable library is present and at what version.
2. **Add Go modules ecosystem support** -- If Go modules dependencies are part of the product, update the `security-matrix.md` files for each version stream to add a Go modules row to the Ecosystem Mappings table:

   | Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
   |-----------|------------|-----------|---------------|-----------------|
   | Go modules | \<repository\> | `go.sum` | `git show <tag>:go.sum \| grep <library>` | \<branch\> |

3. **Re-run triage** -- After adding the ecosystem mapping, re-run `/sdlc-workflow:triage-security TC-8040` to complete automated triage.

## Triage Status

Automated triage **stopped** at Step 1 (Ecosystem Detection). Steps 2 through 8 were not executed. The following completed steps produced results:

- Step 0: Configuration validated (see `data-extraction.md`)
- Step 0.3: Matrix staleness check -- matrix is stale (100 days old)
- Step 1: Data extraction completed (see `data-extraction.md`)
- Step 1 Ecosystem Detection: **Blocked** -- unsupported ecosystem

No Jira mutations were performed.
