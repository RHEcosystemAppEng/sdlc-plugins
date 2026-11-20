# Step 1.5 – External CVE Data Enrichment: CVE-2026-48901 (h2)

External sources are always queried to cross-check the Jira description. In this eval, the
mock responses embedded in the fixture stand in for the WebFetch calls. No network access was used.

## 1. MITRE CVE API (`https://cveawg.mitre.org/api/cve/CVE-2026-48901`)

- Vendor/product: hyperium / h2
- `versions[0]`: `status: affected`, `lessThan: "0.4.8"`, `versionType: semver`
- Affected range: **< 0.4.8**. The fixed version is **0.4.8**, because `lessThan` is exclusive and 0.4.8 is not affected.

## 2. OSV.dev API (`https://api.osv.dev/v1/vulns/CVE-2026-48901`)

- ID: RUSTSEC-2026-0089 (alias CVE-2026-48901)
- Package: crates.io / h2
- Range type SEMVER, events: `introduced: 0`, `fixed: 0.4.8`
- Affected range: **>= 0, < 0.4.8**. Fixed version: **0.4.8**.

## 3. Cross-validation

Fix threshold comparison for CVE-2026-48901 (h2):

| Source           | Affected range                    | Fixed version  | Machine-readable? |
|------------------|-----------------------------------|----------------|-------------------|
| Jira description | "versions prior to the fix" (imprecise) | "see advisory" (not stated) | No |
| MITRE CVE API    | < 0.4.8 (`lessThan`)              | 0.4.8          | Yes |
| OSV.dev          | >= 0, < 0.4.8 (`introduced 0` / `fixed 0.4.8`) | 0.4.8 | Yes |

### Result: **Agreement**. External data is authoritative.

- MITRE and OSV.dev agree exactly: affected `< 0.4.8`, fixed in `0.4.8`.
- The Jira description does not contradict them. "Versions prior to the fix" is
  consistent with `< 0.4.8`, and "see advisory" defers to the advisory data. It just has no
  numeric threshold to compare. So this is not a disagreement, and the engineer does not need
  to pick between conflicting thresholds.
- Following Step 1.5, the structured external data takes precedence over prose-parsed ranges.
  It also fills the critical "affected range" gap left by Step 1.
- Neither external API was unavailable, so confidence is not degraded.

### Enriched fix threshold passed to Step 2.3

> **h2 affected if version < 0.4.8; fixed version = 0.4.8 (inclusive boundary: 0.4.8 is NOT affected).**

Note: the boundary matters here. Several pinned builds ship exactly h2 0.4.8 (see
`version-impact.md`). Under `lessThan: 0.4.8` / `fixed: 0.4.8`, those builds are **not affected**.
If the imprecise Jira prose had been used, those versions could not have been classified with confidence.

## Step 1.7 – Embargo Check

No Embargo policy URL is configured in Security Configuration, so this step is skipped silently.
(CVSS is 7.5, which would otherwise meet the >= 7.0 trigger threshold.)
