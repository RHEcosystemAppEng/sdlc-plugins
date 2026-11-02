# Step 1.5 — External CVE Data Enrichment for CVE-2026-48901

## Motivation

The Jira description for TC-8030 provides only imprecise version information:
- **Affected versions**: "versions prior to the fix" — no specific version threshold
- **Fixed version**: "see advisory" — no specific version number

External CVE databases are queried to obtain structured, machine-readable version ranges.

## 1. MITRE CVE API

**Query**: `https://cveawg.mitre.org/api/cve/CVE-2026-48901`

**Extracted data** from `affected[].versions[]`:

| Field | Value |
|-------|-------|
| Product | h2 |
| Vendor | hyperium |
| Status | affected |
| Version constraint | lessThan: **0.4.8** |
| Version type | semver |

**Fix threshold from MITRE**: **0.4.8** (versions < 0.4.8 are affected)

## 2. OSV.dev API

**Query**: `https://api.osv.dev/v1/vulns/CVE-2026-48901`

**Extracted data** from `affected[].ranges[].events`:

| Field | Value |
|-------|-------|
| Package | h2 |
| Ecosystem | crates.io |
| Introduced | 0 (all versions from inception) |
| Fixed | **0.4.8** |

**Fix threshold from OSV.dev**: **0.4.8** (fixed in version 0.4.8)

## 3. Cross-Validation

| Source | Affected range | Fixed version |
|--------|----------------|---------------|
| Jira description | "versions prior to the fix" (imprecise) | "see advisory" (imprecise) |
| MITRE CVE API | < 0.4.8 | 0.4.8 |
| OSV.dev | introduced: 0, fixed: 0.4.8 | 0.4.8 |

**Result: AGREEMENT** — MITRE and OSV.dev both report the fix threshold as **0.4.8**. The Jira description is imprecise but does not contradict the external sources.

## Enriched Fix Threshold

The enriched fix threshold from external CVE data is **0.4.8**. This value is used as the authoritative fix threshold for Step 2.3 version impact comparisons, replacing the imprecise Jira description data.

- Versions shipping h2 **< 0.4.8** are **AFFECTED**
- Versions shipping h2 **>= 0.4.8** are **NOT AFFECTED**
