# Unsupported Ecosystem Notification: TC-8040

> "**Unsupported ecosystem**: Go modules is not yet supported for automated triage.
> Manual assessment is required."

## Details

| Item | Value |
|------|-------|
| Issue | TC-8040 |
| CVE | CVE-2026-31812 |
| Vulnerable library | quinn-proto (affected < 0.11.14, fixed in 0.11.14) |
| Component | `pscomponent:org/rhtpa-server` |
| Issue stream scope | 2.2.x (from summary suffix `[rhtpa-2.2]`) |
| Detected ecosystem | Go modules |
| Supported ecosystems (2.2.x Ecosystem Mappings) | Cargo, RPM |
| Supported ecosystems (2.1.x Ecosystem Mappings) | Cargo, RPM |

Go modules does not appear in the Ecosystem Mappings table of any configured stream's
`security-matrix.md`. It also has no category in the skill's ecosystem classification
table. So there is no lock file path, check command, or upstream branch to inspect, and
no defined remediation task structure.

## What happens now

Automated triage for this issue **stops at Step 1**. These were not run:

- External CVE data enrichment (Step 1.5)
- Version impact analysis / lock file inspection (Step 2)
- Affects Versions correction (Step 3). The current value is `RHTPA 2.0.0`, which does not
  match the 2.2.x scope.
- Duplicate/sibling, lifecycle, already-fixed, and concurrent triage checks (Steps 4–7)
- Release Jira orchestration and remediation task creation (Steps 7.5–8)

No Jira changes were proposed or made. The `ai-cve-triaged` label was **not** added, so
the issue stays visible in discovery mode as untriaged.

## Recommended manual next steps

1. Check the ecosystem. The library (quinn-proto) and the RUSTSEC-2026-0042 reference
   suggest a Rust/Cargo crate. If the Go modules classification is wrong, fix the
   ecosystem and re-run `/sdlc-workflow:triage-security TC-8040`.
2. If the component really ships Go modules, check each supported 2.2.x version
   (2.2.0–2.2.4) by hand against `go.sum` / `go.mod` at the pinned source commits.
3. To support Go modules in future runs, add a `Go modules` row (repository, lock file
   such as `go.sum`, check command, upstream branch) to each stream's
   `security-matrix.md` Ecosystem Mappings table. Also give it a category in the skill's
   ecosystem classification table.
4. Separately, the security matrix was last updated 2026-06-28 (more than 14 days ago).
   Consider refreshing it with `/setup` before re-running triage.
