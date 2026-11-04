# Unsupported Ecosystem Notification – TC-8040

> **Unsupported ecosystem**: Go modules is not yet supported for automated triage.
> Manual assessment is required.

## Details

| Item | Value |
|---|---|
| Issue | TC-8040 |
| CVE | CVE-2026-31812 |
| Library | quinn-proto (affected < 0.11.14, fixed in 0.11.14) |
| Component | `pscomponent:org/rhtpa-server` |
| Issue stream scope | 2.2.x (`[rhtpa-2.2]`) |
| Detected ecosystem | **Go modules** |
| Ecosystems configured in the Ecosystem Mappings tables | 2.1.x: Cargo, RPM. 2.2.x: Cargo, RPM |

Go modules has no entry in the `security-matrix.md` Ecosystem Mappings table for stream 2.2.x, or for any other configured stream. That leaves no configured lock file, check command, or upstream branch for this ecosystem. Go modules also has no category in the ecosystem classification table, so the number and type of remediation tasks cannot be determined. Version impact analysis would require dependency versions that cannot be backed by `git show` evidence. The skill does not guess them or borrow another ecosystem's mapping, so **automated triage stops at Step 1**.

## What was NOT done

- No external CVE enrichment (Step 1.5), version impact analysis (Step 2), or upstream fix check (Step 2.5)
- No Affects Versions correction (Step 3). The PSIRT value `RHTPA 2.0.0` is still unverified and does not match the 2.2.x scope
- No duplicate, lifecycle, already-fixed, concurrent-triage, or release Jira steps (Steps 4–7.5)
- No remediation tasks created and no close recommendation (Step 8)
- No `ai-cve-triaged` label and no Jira comments or other mutations

## Recommended next steps

1. **Assess manually.** For each supported version in stream 2.2.x (2.2.0, 2.2.1, 2.2.2 (retag of 2.2.1), 2.2.3, 2.2.4) and the development stream, inspect the Go dependency manifests (`go.mod` / `go.sum`) at the pinned source commits, and decide whether the vulnerable version is shipped.
2. **Double-check the ecosystem.** quinn-proto is normally a Rust crate (RUSTSEC advisory), and the configured mappings include Cargo. If the Go modules classification is wrong, correct it and re-run `/sdlc-workflow:triage-security TC-8040`. It would then go through the Cargo path.
3. **Add Go modules support (optional).** To enable automated triage for Go modules later, add a row to each stream's `security-matrix.md` Ecosystem Mappings table (repository, lock file such as `go.sum`, check command, upstream branch). Also add a Go modules category to the skill's ecosystem classification table (likely "Source dependency").
4. **Separately**, the security matrix (`Last-Updated: 2026-06-28`) is 129 days old. Consider refreshing it through `/setup` before the next triage.
