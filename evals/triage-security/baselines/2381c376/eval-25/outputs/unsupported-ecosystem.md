# Unsupported Ecosystem Notification

## Issue: TC-8040 -- CVE-2026-31812 quinn-proto

**Unsupported ecosystem**: Go modules is not yet supported for automated triage. Manual assessment is required.

### Details

- **CVE**: CVE-2026-31812
- **Vulnerable library**: quinn-proto
- **Detected ecosystem**: Go modules
- **Stream scope**: 2.2.x (from summary suffix `[rhtpa-2.2]`)

### Supported Ecosystems for Stream 2.2.x

| Ecosystem | Category | Remediation Tasks per Stream |
|-----------|----------|------------------------------|
| Cargo | Source dependency | 2 (upstream backport/dependency bump + downstream propagation) |
| RPM | System package | 1 (Konflux release repo fix only) |

### Supported Ecosystems for Stream 2.1.x

| Ecosystem | Category | Remediation Tasks per Stream |
|-----------|----------|------------------------------|
| Cargo | Source dependency | 2 (upstream backport/dependency bump + downstream propagation) |
| RPM | System package | 1 (Konflux release repo fix only) |

### Why Triage Stopped

The triage-security skill reads available ecosystems from each stream's `security-matrix.md` Ecosystem Mappings table rather than assuming a fixed set. The detected ecosystem "Go modules" does not appear in the Ecosystem Mappings table for any configured version stream (2.1.x or 2.2.x). Without a matching ecosystem entry, the skill cannot determine:

1. Which **lock file** to inspect (e.g., `go.sum`, `go.mod`)
2. Which **check command** to use for extracting dependency versions
3. Which **upstream branch** to check for fix status
4. Which **remediation category** applies (source dependency vs. system package)

These values are required for Step 2 (Version Impact Analysis) and Step 8 (Remediation Task Creation).

### Required Action

To enable automated triage for Go modules:

1. **Add an Ecosystem Mappings row** to each stream's `security-matrix.md` with the Go modules configuration:

   | Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
   |-----------|------------|-----------|---------------|-----------------|
   | Go modules | backend | `go.sum` | `git show <tag>:go.sum` | `release/0.4.z` |

2. **Update the ecosystem classification table** in the skill to define Go modules' category (likely "Source dependency" -- producing 2 remediation tasks per stream: upstream backport/dependency bump + downstream propagation).

3. **Re-run triage** for TC-8040 after the ecosystem mapping is in place.

### Proposed Jira Actions (not executed)

No Jira mutations were proposed or executed. Automated triage halted at Step 1 (Ecosystem Detection) before any version impact analysis, Affects Versions correction, or remediation task creation could proceed.

The issue TC-8040 remains in its current state:
- **Status**: New
- **Affects Versions**: RHTPA 2.0.0 (PSIRT-assigned, not yet verified)
- **Assignee**: Unassigned
