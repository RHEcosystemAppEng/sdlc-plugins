# Step 1.5 -- External CVE Data Enrichment

## 1. MITRE CVE API

**Query**: `https://cveawg.mitre.org/api/cve/CVE-2026-48901`

**Response** (parsed):

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-48901 |
| Product | h2 |
| Vendor | hyperium |
| Affected range | lessThan 0.4.8 (semver) |
| Version type | semver |

The MITRE CVE record provides a structured `lessThan` constraint: versions below 0.4.8 are affected. The fix threshold is **0.4.8**.

## 2. OSV.dev API

**Query**: `https://api.osv.dev/v1/vulns/CVE-2026-48901`

**Response** (parsed):

| Field | Value |
|-------|-------|
| OSV ID | RUSTSEC-2026-0089 |
| Aliases | CVE-2026-48901 |
| Package | h2 |
| Ecosystem | crates.io |
| Introduced | 0 (all versions from the start) |
| Fixed | 0.4.8 |

The OSV.dev record confirms the fix version is **0.4.8**, with all prior versions affected.

## 3. Cross-Validation

| Source | Affected range | Fixed version |
|--------|----------------|---------------|
| Jira description | "versions prior to the fix" (imprecise) | "see advisory" (imprecise) |
| MITRE CVE API | < 0.4.8 | 0.4.8 |
| OSV.dev | introduced 0, fixed 0.4.8 | 0.4.8 |

**Result: Agreement** -- MITRE and OSV.dev both report the fix threshold as **0.4.8**. The Jira description is imprecise ("versions prior to the fix", "see advisory") and does not provide a specific version number, but does not contradict the external sources.

## Enriched Fix Threshold

The enriched fix threshold from external CVE databases is **0.4.8**. This value is authoritative for Step 2.3 version impact comparisons:

- **Affected**: h2 versions < 0.4.8
- **Not affected**: h2 versions >= 0.4.8

The external data takes precedence over the imprecise Jira description because it provides machine-readable version constraints rather than prose-parsed ranges.
