# Step 1.5 -- External CVE Data Enrichment

The Jira description for TC-8030 contains imprecise version data:
- **Affected versions**: "versions prior to the fix" (no semver threshold)
- **Fixed version**: "see advisory" (no concrete version)

External CVE databases are queried to obtain precise, machine-readable version constraints.

## 1. MITRE CVE API

**Query**: `https://cveawg.mitre.org/api/cve/CVE-2026-48901`

**Parsed response**:

The MITRE CVE record contains the following affected product entry:

```
containers.cna.affected[0]:
  product: h2
  vendor: hyperium
  versions[0]:
    status: affected
    lessThan: "0.4.8"
    versionType: semver
```

**Extracted fix threshold**: All versions with semver **< 0.4.8** are affected. The fix threshold (first non-affected version) is **0.4.8**.

## 2. OSV.dev API

**Query**: `https://api.osv.dev/v1/vulns/CVE-2026-48901`

**Parsed response**:

The OSV.dev record (aliased as RUSTSEC-2026-0089) contains the following affected entry:

```
affected[0]:
  package:
    ecosystem: crates.io
    name: h2
  ranges[0]:
    type: SEMVER
    events:
      - introduced: "0"
      - fixed: "0.4.8"
```

**Extracted fix threshold**: The vulnerability was introduced at version 0 and **fixed at 0.4.8**. All versions in the range [0, 0.4.8) are affected.

## 3. Cross-Validation

| Source | Affected Range | Fixed Version |
|--------|----------------|---------------|
| Jira description | "versions prior to the fix" (imprecise) | "see advisory" (imprecise) |
| MITRE CVE API | < 0.4.8 (lessThan, semver) | 0.4.8 |
| OSV.dev | introduced 0, fixed 0.4.8 (SEMVER) | 0.4.8 |

**Result**: **Agreement** -- both MITRE CVE API and OSV.dev report the same fix threshold: **0.4.8**.

The Jira description data is imprecise ("versions prior to the fix" / "see advisory") and does not provide a usable semver threshold. The external sources agree and provide structured, machine-readable version constraints.

### Enriched Fix Threshold

**Authoritative fix threshold for Step 2.3: 0.4.8**

This value is derived from the cross-validated external CVE data (MITRE + OSV.dev agreement). It replaces the imprecise Jira description data as the basis for version impact comparisons. The external data takes precedence because it provides machine-readable version constraints rather than prose-parsed ranges.
