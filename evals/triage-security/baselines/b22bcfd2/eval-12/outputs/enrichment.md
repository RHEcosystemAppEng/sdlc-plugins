# Step 1.5 -- External CVE Data Enrichment

## Motivation

The Jira description for TC-8030 (CVE-2026-48901) lacks a precise fix threshold:

- **Affected versions (from Jira)**: "versions prior to the fix" -- no specific version number
- **Fixed version (from Jira)**: "see advisory" -- no explicit version number

External CVE databases are queried to obtain structured, machine-readable version constraints.

## 1. MITRE CVE API

**Query**: `https://cveawg.mitre.org/api/cve/CVE-2026-48901`

**Extracted data**:

| Field | Value |
|-------|-------|
| Product | h2 |
| Vendor | hyperium |
| Version constraint | `lessThan: 0.4.8` |
| Version type | semver |

The MITRE CVE API reports that h2 versions **less than 0.4.8** are affected. This gives a precise fix threshold of **0.4.8**.

## 2. OSV.dev API

**Query**: `https://api.osv.dev/v1/vulns/CVE-2026-48901`

**Extracted data**:

| Field | Value |
|-------|-------|
| Package | h2 |
| Ecosystem | crates.io |
| Introduced | 0 (all prior versions) |
| Fixed | 0.4.8 |
| OSV ID | RUSTSEC-2026-0089 |

The OSV.dev database reports that h2 is fixed at version **0.4.8**, meaning all versions prior to 0.4.8 are affected.

## 3. Cross-Validation

| Source | Affected Range | Fixed Version |
|--------|---------------|---------------|
| Jira description | "versions prior to the fix" (imprecise) | "see advisory" (imprecise) |
| MITRE CVE API | < 0.4.8 | 0.4.8 |
| OSV.dev | introduced: 0, fixed: 0.4.8 | 0.4.8 |

**Result: Agreement.** Both external sources (MITRE and OSV.dev) agree on the fix threshold of **0.4.8**. The Jira description provides no precise threshold to compare against, but the external data is consistent.

### Enriched Fix Threshold

The enriched fix threshold from external CVE data is **0.4.8**. This value replaces the imprecise Jira description data and will be used as the authoritative threshold for version impact comparisons in Step 2.3.

| Parameter | Value |
|-----------|-------|
| Enriched fix threshold | **0.4.8** |
| Affected range | h2 < 0.4.8 |
| Source confidence | High (MITRE and OSV.dev agree) |
