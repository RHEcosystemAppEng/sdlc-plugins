# Step 1.5 — External CVE Data Enrichment

## CVE-2026-48901 (h2)

The Jira description for TC-8030 provides imprecise version data:
- **Affected versions**: "versions prior to the fix" (no specific threshold)
- **Fixed version**: "see advisory" (no specific version number)

External CVE databases were queried to obtain structured, machine-readable version constraints.

## 1. MITRE CVE API

**Endpoint**: `https://cveawg.mitre.org/api/cve/CVE-2026-48901`

**Response (parsed)**:

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-48901 |
| Product | h2 |
| Vendor | hyperium |
| Affected range | lessThan 0.4.8 (semver) |
| Status | affected |

The MITRE CVE record specifies `lessThan: "0.4.8"` with `versionType: "semver"`, meaning all versions of h2 strictly less than 0.4.8 are affected. The fix threshold is **0.4.8**.

## 2. OSV.dev API

**Endpoint**: `https://api.osv.dev/v1/vulns/CVE-2026-48901`

**Response (parsed)**:

| Field | Value |
|-------|-------|
| OSV ID | RUSTSEC-2026-0089 |
| Aliases | CVE-2026-48901 |
| Package | h2 (crates.io) |
| Range type | SEMVER |
| Introduced | 0 (all versions from start) |
| Fixed | 0.4.8 |

The OSV.dev record specifies the vulnerability was introduced at version 0 and fixed at 0.4.8. The fix threshold is **0.4.8**.

## 3. Cross-Validation

| Source | Affected range | Fixed version | Precision |
|--------|---------------|---------------|-----------|
| Jira description | "versions prior to the fix" | "see advisory" | Imprecise (no version threshold) |
| MITRE CVE API | < 0.4.8 (semver) | 0.4.8 | Precise (machine-readable) |
| OSV.dev | introduced 0, fixed 0.4.8 | 0.4.8 | Precise (machine-readable) |

### Assessment

- **MITRE and OSV.dev agree**: both report the fix threshold as **0.4.8**
- **Jira description is imprecise**: provides no specific version threshold, only prose references to "versions prior to the fix" and "see advisory"
- **No disagreement**: all sources are consistent; external data enriches the imprecise Jira description

### Enriched Fix Threshold

**0.4.8** — sourced from MITRE CVE API and OSV.dev (cross-validated agreement). All h2 versions strictly less than 0.4.8 are vulnerable. Version 0.4.8 is the first fixed version.

This enriched threshold will be used in Step 2.3 for version impact comparisons instead of the imprecise Jira description data.
