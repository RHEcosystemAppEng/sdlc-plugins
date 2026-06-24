# Step 1.5 -- External CVE Data Enrichment

## Context

The Jira description for TC-8030 lacks a precise fix threshold. The affected range is described as "versions prior to the fix" and the fixed version is "see advisory" -- neither provides a machine-readable version constraint suitable for Step 2.3 comparisons. External CVE databases are queried to obtain structured version range data.

## 1. MITRE CVE API

**Query**: `https://cveawg.mitre.org/api/cve/CVE-2026-48901`

**Parsed response**:

From `containers.cna.affected[0]`:

| Field | Value |
|-------|-------|
| Product | h2 |
| Vendor | hyperium |
| Version status | affected |
| Version constraint | lessThan 0.4.8 |
| Version type | semver |

**Extracted fix threshold**: **0.4.8** (all versions less than 0.4.8 are affected)

## 2. OSV.dev API

**Query**: `https://api.osv.dev/v1/vulns/CVE-2026-48901`

**Parsed response**:

From `affected[0]`:

| Field | Value |
|-------|-------|
| Package ecosystem | crates.io |
| Package name | h2 |
| Range type | SEMVER |
| Introduced | 0 (all versions from the beginning) |
| Fixed | 0.4.8 |
| OSV ID | RUSTSEC-2026-0089 |
| Aliases | CVE-2026-48901 |

**Extracted fix threshold**: **0.4.8** (fixed at version 0.4.8)

## 3. Cross-Validation

Fix threshold comparison for CVE-2026-48901 (h2):

| Source | Affected range | Fixed version |
|--------|----------------|---------------|
| Jira description | "versions prior to the fix" (imprecise) | "see advisory" (imprecise) |
| MITRE CVE API | < 0.4.8 (lessThan, semver) | 0.4.8 |
| OSV.dev | introduced at 0, fixed at 0.4.8 | 0.4.8 |

**Agreement**: MITRE CVE API and OSV.dev both report the fix threshold as **0.4.8**. The two external sources are in full agreement. The Jira description is imprecise but does not contradict the external data -- it simply lacks specificity.

**Enriched fix threshold**: **0.4.8** (from cross-validated external sources)

This enriched fix threshold (< 0.4.8 affected, >= 0.4.8 fixed) is passed to Step 2.3 for use in version impact comparisons. The external data takes precedence because it provides machine-readable version constraints rather than the prose-parsed ranges from the Jira description.
