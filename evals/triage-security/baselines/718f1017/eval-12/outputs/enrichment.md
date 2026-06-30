# Step 1.5 -- External CVE Data Enrichment

## CVE-2026-48901 (h2)

### 1. MITRE CVE API

**Source**: https://cveawg.mitre.org/api/cve/CVE-2026-48901

Parsed data from the MITRE CVE record:

| Field | Value |
|-------|-------|
| Product | h2 |
| Vendor | hyperium |
| Version status | affected |
| Affected range | lessThan 0.4.8 |
| Version type | semver |

The `affected[].versions[].lessThan` field provides a precise fix threshold: versions below 0.4.8 are affected.

### 2. OSV.dev API

**Source**: https://api.osv.dev/v1/vulns/CVE-2026-48901

Parsed data from the OSV record:

| Field | Value |
|-------|-------|
| OSV ID | RUSTSEC-2026-0089 |
| Aliases | CVE-2026-48901 |
| Package ecosystem | crates.io |
| Package name | h2 |
| Range type | SEMVER |
| Introduced | 0 (all versions from inception) |
| Fixed | 0.4.8 |

The `affected[].ranges[].events` field confirms: introduced at version 0, fixed at 0.4.8.

### 3. Cross-Validation

Fix threshold comparison for CVE-2026-48901 (h2):

| Source | Affected range | Fixed version |
|--------|----------------|---------------|
| Jira description | "versions prior to the fix" (imprecise) | "see advisory" (imprecise) |
| MITRE CVE API | < 0.4.8 (lessThan, semver) | 0.4.8 |
| OSV.dev | introduced 0, fixed 0.4.8 | 0.4.8 |

**Cross-validation result: Agreement.**

Both external sources (MITRE CVE API and OSV.dev) agree on the fix threshold: **< 0.4.8**. The Jira description is imprecise ("versions prior to the fix" / "see advisory") and does not provide a machine-readable version constraint.

The structured external data is used as the authoritative fix threshold because:
1. Both external sources independently agree on the same threshold (< 0.4.8)
2. The external data provides machine-readable version constraints (semver `lessThan` from MITRE, semver range events from OSV.dev)
3. The Jira description only contains prose ("versions prior to the fix") with no parseable version range

**Enriched fix threshold for Step 2.3**: h2 < 0.4.8 is affected; h2 >= 0.4.8 is not affected.
