# Step 1.5 – External CVE Data Enrichment: CVE-2026-48901 (h2)

External sources are always queried (not a fallback). For this eval, the mock responses embedded
in the fixture were used instead of live WebFetch calls.

## 1. MITRE CVE API

- URL: https://cveawg.mitre.org/api/cve/CVE-2026-48901
- Status: available (mock)
- `containers.cna.affected[0]`: vendor `hyperium`, product `h2`
- `versions[0]`: `status: affected`, `lessThan: "0.4.8"`, `versionType: semver`
- Parsed: affected range **< 0.4.8**, fixed version **0.4.8**

## 2. OSV.dev API

- URL: https://api.osv.dev/v1/vulns/CVE-2026-48901
- Status: available (mock)
- ID: RUSTSEC-2026-0089 (alias CVE-2026-48901)
- Package: ecosystem `crates.io`, name `h2`
- Range (SEMVER) events: `introduced: 0`, `fixed: 0.4.8`
- Parsed: affected range **>= 0, < 0.4.8**, fixed version **0.4.8**

## 3. Cross-validation

| Source | Affected range | Fixed version | Precision |
|--------|----------------|---------------|-----------|
| Jira description | "versions prior to the fix" | "see advisory" | Imprecise prose — no numeric threshold |
| MITRE CVE API | < 0.4.8 | 0.4.8 | Machine-readable (semver `lessThan`) |
| OSV.dev | >= 0, < 0.4.8 | 0.4.8 | Machine-readable (SEMVER events) |

### Result: Agreement (no conflict)

- MITRE and OSV.dev agree exactly: fixed in **0.4.8**, all versions below are affected.
- The Jira description does not state a numeric threshold, so it neither contradicts nor confirms
  the external data — it is consistent with it ("prior to the fix" = < 0.4.8). There is no
  disagreement to escalate to the engineer.
- Per the precedence rule, the structured external data is authoritative for Step 2.3 comparisons.

### Enriched fix threshold passed to Step 2

- **Affected: h2 < 0.4.8**
- **Fixed: h2 >= 0.4.8**
- Confidence: high (two independent structured sources agree; Jira prose lacked a threshold).

Note: without this enrichment, the Jira description alone would have been insufficient to perform
version impact analysis (critical field "affected range" missing).

## Step 1.7 – Embargo Check

CVSS 7.5 meets the >= 7.0 threshold, but no Embargo policy URL is configured in Security
Configuration → step skipped silently per the skill.
