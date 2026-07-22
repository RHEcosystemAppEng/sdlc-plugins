# Step 1.5 -- External CVE Data Enrichment

## CVE-2026-48901 (h2)

### 1. MITRE CVE API

**Source**: https://cveawg.mitre.org/api/cve/CVE-2026-48901

Parsed data from the MITRE CVE record:

| Field | Value |
|-------|-------|
| Product | h2 |
| Vendor | hyperium |
| Version constraint | lessThan 0.4.8 |
| Version type | semver |
| Status | affected |

**Interpretation**: All versions of h2 prior to 0.4.8 are affected. The fix threshold is **0.4.8**.

### 2. OSV.dev API

**Source**: https://api.osv.dev/v1/vulns/CVE-2026-48901

Parsed data from the OSV.dev record:

| Field | Value |
|-------|-------|
| OSV ID | RUSTSEC-2026-0089 |
| Package | h2 |
| Ecosystem | crates.io |
| Introduced | 0 (all versions) |
| Fixed | 0.4.8 |

**Interpretation**: The vulnerability was introduced from the beginning of the package and is fixed in version **0.4.8**.

### 3. Cross-Validation

Fix threshold comparison for CVE-2026-48901 (h2):

| Source | Affected range | Fixed version |
|--------|----------------|---------------|
| Jira description | "versions prior to the fix" (imprecise) | "see advisory" (imprecise) |
| MITRE CVE API | < 0.4.8 (semver lessThan) | 0.4.8 |
| OSV.dev | introduced 0, fixed 0.4.8 | 0.4.8 |

**Assessment**: The Jira description provides no concrete version threshold -- it says only "versions prior to the fix" and "see advisory." Both external sources (MITRE CVE API and OSV.dev) **agree** on the fix threshold: **0.4.8**. The Jira description does not contradict this -- it is simply imprecise.

**Enriched fix threshold**: **0.4.8** (from cross-validated MITRE and OSV.dev data)

This enriched threshold will be used in Step 2.3 for version impact comparisons. Versions of h2 < 0.4.8 are affected; versions >= 0.4.8 are not affected.

### Enrichment Value

Without external CVE data enrichment, the Jira description alone would not provide a usable fix threshold for automated version impact analysis. The enrichment step resolved the imprecise "versions prior to the fix" / "see advisory" language into the concrete, machine-comparable threshold of **h2 < 0.4.8**.
