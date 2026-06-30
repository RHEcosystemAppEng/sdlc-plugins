# Step 1 -- Data Extraction

## Issue: TC-8030

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-48901 | Labels, summary |
| Affected component | pscomponent:org/rhtpa-server | Labels (pattern `pscomponent:`) |
| Product version (PSIRT-claimed) | [rhtpa-2.2] | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.2.0 | Jira `versions` field |
| Vulnerable library | h2 | Description text |
| Affected version range | "versions prior to the fix" (imprecise -- no specific version threshold) | Description text |
| Fixed version | "see advisory" (imprecise -- no specific version given) | Description text |
| CVSS | 7.5 (High) | Description text |
| Upstream fix PR | https://github.com/hyperium/h2/pull/800 | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-r7f2-kk9p | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-48901 | Remote links |
| Due date | 2026-08-01 | Issue `duedate` field |
| Existing comments | None | Issue comment history |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped to configured Version Stream: **2.2.x**
- Konflux Release Repo: git.example.com/rhtpa/rhtpa-release.0.4.z
- Local Path: /home/dev/repos/rhtpa-release.0.4.z
- Issue stream scope: **2.2.x only** (scoped issue)

## Ecosystem Detection

- Library: h2 (Rust crate)
- Ecosystem: **Cargo**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Repository: backend
- Upstream branch: `release/0.4.z`

## Data Quality Notes

The Jira description provides imprecise version information:
- Affected versions: "versions prior to the fix" -- no specific version threshold
- Fixed version: "see advisory" -- no specific version given

These imprecise values necessitate external CVE data enrichment (Step 1.5) to obtain a machine-readable fix threshold for version impact analysis.
