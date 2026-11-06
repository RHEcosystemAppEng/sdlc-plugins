# Step 1.5 – External CVE Data Enrichment: CVE-2026-48901 (h2)

External sources are always queried to supplement and cross-validate the Jira description. For this eval, the mock API responses embedded in the fixture stand in for live WebFetch calls.

## 1. MITRE CVE API

- URL: `https://cveawg.mitre.org/api/cve/CVE-2026-48901`
- Status: available (mock response)
- `containers.cna.affected[0]`: vendor `hyperium`, product `h2`
- `versions[0]`: `status: affected`, `lessThan: "0.4.8"`, `versionType: semver`
- **Parsed:** affected `< 0.4.8`. The fixed version is implied as `0.4.8`, since `lessThan` is exclusive.

## 2. OSV.dev API

- URL: `https://api.osv.dev/v1/vulns/CVE-2026-48901`
- Status: available (mock response)
- ID `RUSTSEC-2026-0089`, alias `CVE-2026-48901`
- Package: ecosystem `crates.io`, name `h2`
- Range type `SEMVER`, events: `introduced: "0"`, `fixed: "0.4.8"`
- **Parsed:** affected `>= 0, < 0.4.8`, fixed `0.4.8`. The ecosystem (crates.io) matches the Cargo detection from Step 1.

## 3. Cross-validation

Fix threshold comparison for CVE-2026-48901 (h2):

| Source           | Affected range                     | Fixed version  | Precision |
|------------------|------------------------------------|----------------|-----------|
| Jira description | "versions prior to the fix"        | "see advisory" | Imprecise / unparseable |
| MITRE CVE API    | < 0.4.8 (`lessThan`, semver)       | 0.4.8          | Structured |
| OSV.dev          | >= 0, < 0.4.8 (`introduced`/`fixed`) | 0.4.8        | Structured |

### Outcome

- **MITRE and OSV.dev agree exactly.** Both give affected `< 0.4.8` and fixed `0.4.8`.
- **The Jira description does not contradict them.** It gives no numeric threshold at all ("versions prior to the fix" / "see advisory"), so this is not a disagreement case. The external data fills a gap in the description.
- Per the skill rules, structured external data takes precedence over prose-parsed ranges when sources agree. Here it is the **only** precise source available.
- No external source was unavailable, so there is no degraded-confidence warning.

### Enriched fix threshold (passed to Step 2.3)

> **h2 affected: `< 0.4.8`. Fixed in: `0.4.8`.**
>
> Comparison rule: a lock-file version `v` is AFFECTED when `v < 0.4.8` (semver). `0.4.8` itself is **NOT** affected.

Engineer confirmation point: the Jira description had no threshold, so the skill presents this enriched threshold for confirmation before running version impact analysis. For this eval, the threshold is accepted.

## Step 1.7 – Embargo Check

CVSS is 7.5 (High), which meets the >= 7.0 trigger. However, **no Embargo policy URL is configured** in Security Configuration, so the step is skipped silently.
