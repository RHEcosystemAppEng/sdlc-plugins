# Step 1.5 — External CVE Data Enrichment

The Jira description for TC-8030 provides imprecise version data:
- **Affected versions**: "versions prior to the fix" (no specific version threshold)
- **Fixed version**: "see advisory" (no specific version)

External CVE databases are queried to obtain structured, machine-readable version constraints.

## 1. MITRE CVE API

**Query**: `https://cveawg.mitre.org/api/cve/CVE-2026-48901`

**Extracted data**:
- Product: h2 (vendor: hyperium)
- Affected version range: `lessThan: "0.4.8"` (versionType: semver)
- Status: affected
- **Fix threshold**: `0.4.8` (versions < 0.4.8 are affected)

The MITRE CVE record provides a precise, machine-readable `lessThan` field in the `affected[].versions[]` array, indicating all semver versions below 0.4.8 are vulnerable.

## 2. OSV.dev API

**Query**: `https://api.osv.dev/v1/vulns/CVE-2026-48901`

**Extracted data**:
- Package: h2 (ecosystem: crates.io)
- Alias: RUSTSEC-2026-0089
- Range type: SEMVER
- Events:
  - `introduced: "0"` (all versions from 0 onward)
  - `fixed: "0.4.8"` (fixed in version 0.4.8)
- **Fix threshold**: `0.4.8` (versions introduced at 0 and fixed at 0.4.8)

The OSV.dev record provides ecosystem-specific version range data via the `affected[].ranges[].events` array, confirming the fix boundary at 0.4.8.

## 3. Cross-Validation

| Source | Affected range | Fixed version |
|--------|---------------|---------------|
| Jira description | "versions prior to the fix" (imprecise) | "see advisory" (imprecise) |
| MITRE CVE API | < 0.4.8 (lessThan, semver) | 0.4.8 |
| OSV.dev | introduced 0, fixed 0.4.8 | 0.4.8 |

**Result: Agreement.** Both MITRE CVE API and OSV.dev report the same fix threshold: **0.4.8**. The two external sources are consistent with each other.

The Jira description is imprecise and does not provide a specific version threshold. The external sources provide the authoritative, machine-readable constraint.

**Enriched fix threshold**: **0.4.8** (from MITRE and OSV.dev, in agreement)

This enriched threshold will be used as the authoritative value for Step 2.3 version impact comparisons, replacing the imprecise Jira description data. Versions shipping h2 < 0.4.8 are affected; versions shipping h2 >= 0.4.8 are not affected.
