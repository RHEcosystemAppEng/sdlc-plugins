# Unsupported Ecosystem Notification: TC-8040

> "**Unsupported ecosystem**: Go modules is not yet supported for automated triage.
> Manual assessment is required."

## Details

| Item | Value |
|------|-------|
| Issue | TC-8040 |
| CVE | CVE-2026-31812 |
| Vulnerable library | quinn-proto (affected `< 0.11.14`, fixed in `0.11.14`) |
| Issue stream scope | 2.2.x (from summary suffix `[rhtpa-2.2]`) |
| Detected ecosystem | Go modules |
| Supported ecosystems (Ecosystem Mappings, both streams 2.1.x and 2.2.x) | Cargo, RPM |

Go modules has no row in either stream's `security-matrix.md` Ecosystem Mappings table.
That means no lock file (such as `go.sum`) and no check command are configured, so the
skill cannot determine which dependency version is pinned at each release tag. It also
has no category in the ecosystem classification table, so the number of remediation
tasks per stream cannot be decided. **Automated triage stopped after Step 1 for this
ecosystem.** No version impact analysis was done, no Affects Versions were changed, no
remediation tasks were created, no labels or comments were added, and Jira was not modified.

## What This Means for TC-8040

- The PSIRT-assigned Affects Versions (`RHTPA 2.0.0`) is **unverified** and still on the
  issue. It also looks wrong: the summary scopes the issue to 2.2.x, and no 2.0.x stream
  is configured. Fix it during manual assessment.
- Due date 2026-07-15 has already passed (today is 2026-11-20). Prioritize the manual
  assessment.

## Suggested Next Steps (manual)

1. **Confirm the ecosystem.** quinn-proto looks like a Rust crate (RUSTSEC advisory
   RUSTSEC-2026-0042). If it is really Cargo, re-run `/triage-security TC-8040` with the
   corrected ecosystem. Cargo is supported, with `Cargo.lock` mapped in both streams.
2. **If the dependency really is a Go module**, check the pinned version by hand for each
   supported version in the 2.2.x stream (backend tags `v0.4.5`, `v0.4.8`, `v0.4.11`,
   `v0.4.12`; 2.2.2 is a retag of `v0.4.8`). For example:
   `git show <tag>:go.sum | grep quinn-proto`. Compare each result against the fixed
   version 0.11.14.
3. **Update Affects Versions** by hand to the versions you confirm are affected, and add
   a comment that records the evidence.
4. **To enable automated triage for Go modules later**, add a `Go modules` row to each
   stream's `security-matrix.md` Ecosystem Mappings table (Repository, Lock File such as
   `go.sum`, Check Command, Upstream Branch). Also add Go modules to the skill's ecosystem
   classification table, probably as a source dependency (2 tasks per stream).

Would you like to continue with manual assessment, re-run triage with a different
ecosystem, or skip this issue?
