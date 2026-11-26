# Step 1.5 – External CVE Data Enrichment: CVE-2026-48901 (h2)

External sources are always queried to supplement and cross-validate the Jira
description. In this eval, the mock API responses embedded in the fixture were used
in place of live WebFetch calls.

## 1. MITRE CVE API

- URL: `https://cveawg.mitre.org/api/cve/CVE-2026-48901`
- Status: available (mock response)
- `containers.cna.affected[0]`: vendor `hyperium`, product `h2`
- `versions[0]`: `status: affected`, `lessThan: "0.4.8"`, `versionType: semver`
- **Parsed:** affected range `< 0.4.8`, fixed version `0.4.8`

## 2. OSV.dev API

- URL: `https://api.osv.dev/v1/vulns/CVE-2026-48901`
- Status: available (mock response)
- ID `RUSTSEC-2026-0089`, aliases `CVE-2026-48901`
- Package: ecosystem `crates.io`, name `h2`
- Range type `SEMVER`, events: `introduced: 0`, `fixed: 0.4.8`
- **Parsed:** affected range `>= 0, < 0.4.8`, fixed version `0.4.8`

## 3. Cross-validation

Fix threshold comparison for CVE-2026-48901 (h2):

| Source           | Affected range                 | Fixed version  | Precision |
|------------------|--------------------------------|----------------|-----------|
| Jira description | "versions prior to the fix"    | "see advisory" | Imprecise — no numeric threshold |
| MITRE CVE API    | < 0.4.8                        | 0.4.8          | Structured (semver `lessThan`) |
| OSV.dev          | >= 0 (introduced 0), < 0.4.8   | 0.4.8          | Structured (SEMVER events) |

### Analysis

- **MITRE and OSV.dev agree exactly**: affected `< 0.4.8`, fixed in `0.4.8`.
- **Jira description does not contradict them** — it says "versions prior to the fix"
  with the fix deferred to the advisory. It supplies no competing numeric threshold, so
  this is not a disagreement requiring engineer arbitration; the external data fills
  the gap the prose leaves open.
- Outcome category: **Agreement** → structured external data is used as the
  authoritative fix threshold for Step 2.3 comparisons (external data takes precedence
  because it is machine-readable rather than prose-parsed).
- Neither external source is unavailable → no degraded-confidence warning needed.

## Enriched fix threshold (passed to Step 2.3)

| Item | Value |
|------|-------|
| Library | h2 (crates.io) |
| Affected | **h2 < 0.4.8** (introduced 0) |
| Fixed | **h2 >= 0.4.8** |
| Boundary rule | A version exactly equal to `0.4.8` is **NOT affected** (MITRE uses `lessThan`, OSV uses `fixed`, both exclusive of 0.4.8) |
| Confidence | High (two independent structured sources agree) |

## Step 1.7 – Embargo Check

CVSS 7.5 (High) meets the >= 7.0 threshold, but no Embargo policy URL is configured
in Security Configuration → step skipped silently per skill rules.
