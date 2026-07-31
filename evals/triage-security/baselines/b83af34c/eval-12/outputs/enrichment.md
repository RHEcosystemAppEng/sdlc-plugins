# Step 1.5 -- External CVE Data Enrichment

## CVE-2026-48901 (h2)

### 1. MITRE CVE API

**Source**: https://cveawg.mitre.org/api/cve/CVE-2026-48901

Parsed from `affected[].versions[]`:

| Field | Value |
|-------|-------|
| Product | h2 |
| Vendor | hyperium |
| Status | affected |
| Version constraint | lessThan **0.4.8** |
| Version type | semver |

The MITRE CVE record provides a precise, machine-readable fix threshold via the `affected[].versions[].lessThan` field: versions less than **0.4.8** are affected.

### 2. OSV.dev API

**Source**: https://api.osv.dev/v1/vulns/CVE-2026-48901

Parsed from `affected[].ranges[].events`:

| Field | Value |
|-------|-------|
| OSV ID | RUSTSEC-2026-0089 |
| Package | h2 |
| Ecosystem | crates.io |
| Range type | SEMVER |
| Introduced | 0 (all versions from the beginning) |
| Fixed | **0.4.8** |

The OSV.dev record provides structured version range data via `affected[].ranges[].events`: the vulnerability was introduced at version 0 and fixed at version **0.4.8**.

### 3. Cross-Validation

| Source | Affected range | Fixed version |
|--------|----------------|---------------|
| Jira description | "versions prior to the fix" (imprecise) | "see advisory" (imprecise) |
| MITRE CVE API | < 0.4.8 (lessThan field) | 0.4.8 |
| OSV.dev | introduced: 0, fixed: 0.4.8 | 0.4.8 |

**Agreement**: MITRE CVE API and OSV.dev both report the fix threshold as **0.4.8**. The two external sources are in full agreement.

**Jira description comparison**: The Jira description provides no specific version threshold ("versions prior to the fix" / "see advisory"), so there is no conflict -- only absence of data. The external sources fill the gap with precise, machine-readable version constraints.

**Enriched fix threshold**: **0.4.8** (cross-validated by both MITRE and OSV.dev)

This enriched fix threshold (0.4.8) is the authoritative value passed to Step 2.3 for version impact comparisons. The external data takes precedence because it provides machine-readable version constraints rather than the imprecise prose from the Jira description.
