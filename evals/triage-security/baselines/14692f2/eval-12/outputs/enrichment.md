# Step 1.5 -- External CVE Data Enrichment

## Motivation

The Jira description for TC-8030 contains imprecise version data:
- **Affected versions**: "versions prior to the fix" (no threshold)
- **Fixed version**: "see advisory" (no version number)

External CVE databases are queried to obtain structured, machine-readable
version constraints.

## 1. MITRE CVE API

**Source**: `https://cveawg.mitre.org/api/cve/CVE-2026-48901`

Extracted data from the MITRE CVE record:

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-48901 |
| Product | h2 |
| Vendor | hyperium |
| Version status | affected |
| Version constraint | **lessThan: 0.4.8** |
| Version type | semver |

**Interpretation**: All versions of h2 prior to 0.4.8 are affected. The fix
threshold is **0.4.8** (first non-vulnerable version).

## 2. OSV.dev API

**Source**: `https://api.osv.dev/v1/vulns/CVE-2026-48901`

Extracted data from the OSV.dev record:

| Field | Value |
|-------|-------|
| OSV ID | RUSTSEC-2026-0089 |
| Aliases | CVE-2026-48901 |
| Package | h2 |
| Ecosystem | crates.io |
| Range type | SEMVER |
| Introduced | 0 (all versions from inception) |
| Fixed | **0.4.8** |

**Interpretation**: The vulnerability was introduced at version 0 (i.e., all
versions) and fixed at version **0.4.8**. Versions < 0.4.8 are affected.

## 3. Cross-Validation

### Cross-Validation Table

| Source | Affected Range | Fix Threshold | Status |
|--------|---------------|---------------|--------|
| Jira description | "versions prior to the fix" (imprecise) | "see advisory" (imprecise) | Imprecise -- no usable threshold |
| MITRE CVE API | lessThan 0.4.8 (semver) | **0.4.8** | Precise |
| OSV.dev | introduced 0, fixed 0.4.8 (SEMVER) | **0.4.8** | Precise |

### Validation Result: **AGREEMENT**

Both external sources (MITRE CVE API and OSV.dev) agree on the fix threshold:
**0.4.8**. The Jira description is imprecise but not contradictory -- it simply
lacks specificity.

### Enriched Fix Threshold

**Fix threshold: 0.4.8** (from cross-validated external sources)

- Versions < 0.4.8 are **AFFECTED**
- Versions >= 0.4.8 are **NOT AFFECTED**

This enriched threshold replaces the imprecise Jira description data and will
be used for all version impact comparisons in Step 2.3.
