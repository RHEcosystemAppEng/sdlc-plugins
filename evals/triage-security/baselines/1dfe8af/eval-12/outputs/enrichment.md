# Step 1.5 -- External CVE Data Enrichment

## 1. MITRE CVE API

Source: `https://cveawg.mitre.org/api/cve/CVE-2026-48901`

Parsed data from the MITRE CVE record:

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-48901 |
| Product | h2 |
| Vendor | hyperium |
| Affected range | lessThan 0.4.8 (semver) |
| Version type | semver |

The `containers.cna.affected[0].versions[0]` entry specifies:
- `status`: affected
- `lessThan`: **0.4.8**
- `versionType`: semver

This means all versions of h2 prior to 0.4.8 are affected. Version 0.4.8 is the fix.

## 2. OSV.dev API

Source: `https://api.osv.dev/v1/vulns/CVE-2026-48901`

Parsed data from the OSV.dev record:

| Field | Value |
|-------|-------|
| OSV ID | RUSTSEC-2026-0089 |
| Aliases | CVE-2026-48901 |
| Package | h2 |
| Ecosystem | crates.io |
| Range type | SEMVER |
| Introduced | 0 (all versions from the start) |
| Fixed | **0.4.8** |

The `affected[0].ranges[0].events` array shows:
- `introduced`: 0 (vulnerability present from the beginning)
- `fixed`: 0.4.8 (vulnerability resolved in this version)

## 3. Cross-Validation

Fix threshold comparison for CVE-2026-48901 (h2):

| Source | Affected range | Fixed version |
|--------|----------------|---------------|
| Jira description | "versions prior to the fix" (IMPRECISE) | "see advisory" (IMPRECISE) |
| MITRE CVE API | < 0.4.8 (semver) | 0.4.8 |
| OSV.dev | introduced 0, fixed 0.4.8 | 0.4.8 |

### Assessment

- **MITRE and OSV.dev agree**: both report the fix threshold as **0.4.8**
- **Jira description is imprecise**: it says "versions prior to the fix" with no specific version number, and defers to the advisory for the fixed version
- The external sources provide structured, machine-readable version constraints that supersede the prose-based Jira description

### Enriched Fix Threshold

**0.4.8** (from cross-validated MITRE CVE API and OSV.dev data)

This enriched threshold will be used in Step 2.3 for version impact comparisons. Versions shipping h2 < 0.4.8 are AFFECTED; versions shipping h2 >= 0.4.8 are NOT AFFECTED.
