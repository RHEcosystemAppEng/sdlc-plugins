# Step 1 -- Data Extraction: TC-8002

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-28940 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | serde_json |
| Affected version range | versions before 1.0.135 |
| Fixed version | 1.0.135 |
| CVSS | 5.3 (Medium) |
| Upstream fix PR | Not provided |
| Advisory URL | https://github.com/advisories/GHSA-2026-j9r2-m5vk |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-28940 |
| Due date | 2026-07-30 |
| Existing comments | None |

## Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream (Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`).

This issue is **stream-scoped** to 2.2.x. Steps 3-4 will apply only to versions in the 2.2.x stream.

However, per Step 2, all streams are analyzed for version impact to detect cross-stream impact (Case B).

## Ecosystem Detection

The vulnerable library is **serde_json**, a Rust crate. The ecosystem is **Cargo**.

From the security-matrix.md Ecosystem Mappings for both streams:

| Stream | Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|--------|-----------|------------|-----------|---------------|-----------------|
| 2.1.x | Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.3.z` |
| 2.2.x | Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` |

## Deployment Context

The affected repository `rhtpa-backend` is found in the Source Repositories table. No Deployment Context column is present (backward compatibility), so the default context is `upstream`.

## Step 0.3 -- Matrix Staleness Check

The security-matrix.md has `Last-Updated: 2026-06-28T10:00:00Z`, which is 4 days ago (current date: 2026-07-02). This is within the 14-day threshold -- matrix is fresh.

## Step 1.7 -- Embargo Check

No Embargo policy URL is configured in Security Configuration. Step 1.7 is skipped.
