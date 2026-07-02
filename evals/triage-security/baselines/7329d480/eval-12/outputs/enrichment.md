# Step 1.5 -- External CVE Data Enrichment

## CVE-2026-48901 (h2)

The Jira description provides only imprecise version information:
- **Affected versions**: "versions prior to the fix" (no numeric threshold)
- **Fixed version**: "see advisory" (no specific version)

External CVE databases were queried to obtain structured, machine-readable version data.

### 1. MITRE CVE API

**Source**: https://cveawg.mitre.org/api/cve/CVE-2026-48901

Parsed fields from the MITRE CVE record:

| Field | Value |
|-------|-------|
| Product | h2 |
| Vendor | hyperium |
| Affected range | lessThan 0.4.8 (semver) |
| Version type | semver |

The MITRE record provides a structured `lessThan` constraint: all h2 versions below 0.4.8 are affected. Version 0.4.8 is the first fixed version.

### 2. OSV.dev API

**Source**: https://api.osv.dev/v1/vulns/CVE-2026-48901

Parsed fields from the OSV.dev record:

| Field | Value |
|-------|-------|
| ID | RUSTSEC-2026-0089 |
| Aliases | CVE-2026-48901 |
| Package | h2 |
| Ecosystem | crates.io |
| Introduced | 0 (all versions from the start) |
| Fixed | 0.4.8 |
| Range type | SEMVER |

The OSV.dev record confirms that the vulnerability was introduced from the initial release and is fixed in version 0.4.8.

### 3. Cross-Validation

Fix threshold comparison for CVE-2026-48901 (h2):

| Source | Affected range | Fixed version | Precision |
|--------|---------------|---------------|-----------|
| Jira description | "versions prior to the fix" | "see advisory" | Imprecise -- no numeric threshold |
| MITRE CVE API | < 0.4.8 (semver) | 0.4.8 | Precise -- structured lessThan constraint |
| OSV.dev | introduced 0, fixed 0.4.8 | 0.4.8 | Precise -- structured SEMVER range |

**Result**: MITRE and OSV.dev **agree** on the fix threshold: **0.4.8**. The Jira description is imprecise but not contradictory -- "versions prior to the fix" is consistent with the external data, it simply lacks the specific version number.

### Enriched Fix Threshold

| Field | Value | Source |
|-------|-------|--------|
| Fix threshold | **0.4.8** | MITRE CVE API + OSV.dev (cross-validated) |
| Affected range | **< 0.4.8** | h2 versions below 0.4.8 are vulnerable |
| Confidence | **High** | Two independent external sources agree |

The enriched fix threshold of **0.4.8** will be used in Step 2.3 for version impact comparisons. This threshold supersedes the imprecise Jira description data because it provides a machine-readable version constraint from authoritative sources.
