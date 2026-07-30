# Unsupported Ecosystem Notification

## Triage Halted: Unsupported Ecosystem

**Issue**: TC-8001 -- CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2]
**Detected ecosystem**: Go modules
**Stream**: 2.2.x (rhtpa-release.0.4.z)

---

**Unsupported ecosystem**: Go modules is not yet supported for automated triage. Manual assessment is required.

The Ecosystem Mappings table for the 2.2.x stream only contains the following ecosystems:

| Ecosystem | Category | Lock File |
|-----------|----------|-----------|
| Cargo | Source dependency | `Cargo.lock` |
| RPM | System package | `rpms.lock.yaml` |

"Go modules" does not appear in any configured stream's Ecosystem Mappings table.

## What This Means

Automated version impact analysis (Step 2) cannot proceed because:

1. There is no lock file mapping for Go modules -- the skill does not know which lock file (e.g., `go.sum`) to inspect or what parsing command to use.
2. There is no ecosystem classification (source dependency vs. system package) -- the skill cannot determine the correct remediation task structure.
3. There is no upstream branch mapping -- the skill cannot check for upstream fix status.

## Recommended Actions

1. **Manual assessment**: An engineer should manually determine which product versions ship the vulnerable Go module and at what version, using the appropriate Go dependency tooling (`go.sum`, `go list -m all`, etc.).
2. **Update ecosystem configuration**: If Go modules will be a recurring ecosystem for this product, add it to each stream's `security-matrix.md` Ecosystem Mappings table during the next `/setup` run:

   | Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
   |-----------|------------|-----------|---------------|-----------------|
   | Go modules | backend | `go.sum` | `git show <tag>:go.sum` | `release/0.4.z` |

3. **Re-run triage**: After adding Go modules to the Ecosystem Mappings table with the appropriate lock file, check command, and upstream branch, re-run `/sdlc-workflow:triage-security TC-8001` for automated version impact analysis.

## Triage Status

- Steps completed: 0 (Validate Configuration), 0.3 (Matrix Staleness Check), 1 (Data Extraction -- partial)
- Steps not executed: 1.5 through 8 (blocked by unsupported ecosystem)
- No Jira mutations were performed
- No remediation tasks were created
