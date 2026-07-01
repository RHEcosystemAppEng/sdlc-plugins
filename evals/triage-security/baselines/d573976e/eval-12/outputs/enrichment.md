# Step 1.5 -- External CVE Data Enrichment

## Context

The Jira description for TC-8030 provides imprecise version information:
- **Affected versions**: "versions prior to the fix" (no specific version threshold)
- **Fixed version**: "see advisory" (no specific version stated)

These values are insufficient for version impact analysis in Step 2.3. External CVE databases are queried to obtain precise, machine-readable fix thresholds.

## 1. MITRE CVE API

**Query**: `https://cveawg.mitre.org/api/cve/CVE-2026-48901`

**Response** (from mock data embedded in fixture):

```json
{
  "cveMetadata": {"cveId": "CVE-2026-48901"},
  "containers": {
    "cna": {
      "affected": [{
        "product": "h2",
        "vendor": "hyperium",
        "versions": [{
          "status": "affected",
          "lessThan": "0.4.8",
          "versionType": "semver"
        }]
      }]
    }
  }
}
```

**Extracted data**:
- Product: h2 (vendor: hyperium)
- Affected range: versions < 0.4.8 (semver, `lessThan` field)
- Fix threshold: **0.4.8**

## 2. OSV.dev API

**Query**: `https://api.osv.dev/v1/vulns/CVE-2026-48901`

**Response** (from mock data embedded in fixture):

```json
{
  "id": "RUSTSEC-2026-0089",
  "aliases": ["CVE-2026-48901"],
  "affected": [{
    "package": {"ecosystem": "crates.io", "name": "h2"},
    "ranges": [{
      "type": "SEMVER",
      "events": [
        {"introduced": "0"},
        {"fixed": "0.4.8"}
      ]
    }]
  }]
}
```

**Extracted data**:
- Package: h2 (ecosystem: crates.io)
- Introduced: version 0 (all versions from the start)
- Fixed version: **0.4.8** (from `events[].fixed`)
- Affected range: versions >= 0 and < 0.4.8

## 3. Cross-validation

Fix threshold comparison for CVE-2026-48901 (h2):

| Source | Affected range | Fixed version |
|--------|----------------|---------------|
| Jira description | "versions prior to the fix" (imprecise) | "see advisory" (imprecise) |
| MITRE CVE API | < 0.4.8 | 0.4.8 |
| OSV.dev | >= 0, < 0.4.8 | 0.4.8 |

**Result**: MITRE CVE API and OSV.dev **agree** -- both report the fix threshold as **0.4.8**. The Jira description provides no specific version data, making the external sources essential rather than supplementary for this issue.

**Enriched fix threshold**: **0.4.8** (authoritative, from cross-validated external sources)

This enriched threshold (0.4.8) supersedes the imprecise Jira description data and will be used in Step 2.3 for all version impact comparisons. Any h2 version < 0.4.8 is affected; any h2 version >= 0.4.8 is not affected.
