# TC-8001 — Step 2 Version Impact Analysis

The matrix came from security-matrix-mock.md, covering streams 2.1.x and 2.2.x. Lock-file values
are the simulated `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'` output listed in
the mock.

## Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14)

| Version | Stream | backend tag | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | outside issue scope (cross-stream) |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | outside issue scope (cross-stream) |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | v0.4.8 | — | YES | backend retag of 2.2.1, same as 2.2.1 (lock check skipped) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | fixed version |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | fixed version |
| dev stream | — | branch HEAD | not determined | — | No unreleased Jira version data was available (Step 2.2 needs `getJiraIssueTypeMetaWithFields`, not called in this eval). The dev stream must be checked at branch HEAD in a live run. |

### Dependency chain (Step 2.3.5)
The mock does not include Cargo.toml or the full Cargo.lock dependency graph, so the
direct-or-transitive classification **cannot be confirmed**. quinn-proto is usually transitive
(backend → [reqwest/h3/quinn] → quinn → quinn-proto) and is a production runtime dependency. No
evidence suggests it is dev-only or feature-gated. The engineer must verify the chain before tasks
are created. The task templates below include both remediation approaches.

- Introduction point: present in every tag inspected (v0.3.8 onward). The fix arrived between v0.4.8 (0.11.12) and v0.4.11 (0.11.14).

## Upstream fix status (Step 2.5)

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.2.x | Cargo | release/0.4.z | >= 0.11.14 (inferred: released tags v0.4.11 and v0.4.12 on this branch ship 0.11.14; HEAD not read in this eval) | YES (inferred) |
| 2.1.x | Cargo | release/0.3.z | 0.11.9 at latest release tag v0.3.12; HEAD not read in this eval | NO (as of last release) |

## Summary
- **In scope (2.2.x):** 2.2.0, 2.2.1, and 2.2.2 are affected. 2.2.3 and 2.2.4 already ship the fix.
- **Cross-stream (2.1.x):** 2.1.0 and 2.1.1 are affected. This triggers Case A (cross-stream comment plus preemptive tasks if no 2.1.x sibling CVE Jira exists).

## Step 3 preview — Affects Versions correction (proposed, requires confirmation)
- Current: `RHTPA 2.0.0`. This is wrong: no 2.0.x stream is supported and nothing shows it ships quinn-proto in this matrix.
- Proposed (scoped to 2.2.x): `RHTPA 2.2.0`, `RHTPA 2.2.1`, `RHTPA 2.2.2`. Version IDs would be discovered dynamically.
- 2.1.0 and 2.1.1 are not added to this issue because they belong to another stream. They go in the Case A cross-stream comment instead.
