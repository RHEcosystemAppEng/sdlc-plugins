# Step 1.5 -- External CVE Data Enrichment: CVE-2026-48901

## 1. MITRE CVE API

**Query**: `https://cveawg.mitre.org/api/cve/CVE-2026-48901`

**Parsed data**:
- Product: h2
- Vendor: hyperium
- Affected versions: `lessThan` **0.4.8** (semver)
- Version type: semver
- Status: affected

The MITRE CVE record provides a structured `lessThan` constraint: all versions below 0.4.8 are affected. This means version **0.4.8** is the fix threshold (first non-affected version).

## 2. OSV.dev API

**Query**: `https://api.osv.dev/v1/vulns/CVE-2026-48901`

**Parsed data**:
- OSV ID: RUSTSEC-2026-0089
- Aliases: CVE-2026-48901
- Package: h2 (ecosystem: crates.io)
- Range type: SEMVER
- Introduced: 0 (all versions from the beginning)
- Fixed: **0.4.8**

The OSV.dev record confirms that version 0.4.8 is the fix point. All versions from 0 up to (but not including) 0.4.8 are affected.

## 3. Cross-Validation

| Source | Affected range | Fixed version |
|--------|----------------|---------------|
| Jira description | "versions prior to the fix" (imprecise) | "see advisory" (imprecise) |
| MITRE CVE API | < 0.4.8 (lessThan, semver) | 0.4.8 |
| OSV.dev | introduced 0, fixed 0.4.8 | 0.4.8 |

**Assessment**: The MITRE CVE API and OSV.dev **agree** on the fix threshold: **0.4.8**. The Jira description provides no precise version constraint -- it only states "versions prior to the fix" and "see advisory", which are imprecise and unactionable for version impact comparison.

The external sources provide machine-readable, structured version constraints that supersede the imprecise prose from the Jira description.

**Enriched fix threshold**: **0.4.8**

This enriched threshold will be used in Step 2.3 for version impact comparisons. Versions shipping h2 < 0.4.8 are affected; versions shipping h2 >= 0.4.8 are not affected.
