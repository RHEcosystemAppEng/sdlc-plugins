# Step 1.5 -- External CVE Data Enrichment

## Problem

The Jira description for CVE-2026-48901 lacks a precise affected version threshold. The description states:
- **Affected versions**: "versions prior to the fix" (no specific version boundary)
- **Fixed version**: "see advisory" (no specific version number)

This imprecise data cannot be used for version impact comparisons in Step 2.3. External CVE databases are queried to obtain structured version range data.

## 1. MITRE CVE API

**Query**: `https://cveawg.mitre.org/api/cve/CVE-2026-48901`

**Response** (parsed):

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
- Product: h2 (by hyperium)
- Affected range: versions < 0.4.8 (semver comparison)
- Fix threshold: **0.4.8** (from `lessThan` field)

## 2. OSV.dev API

**Query**: `https://api.osv.dev/v1/vulns/CVE-2026-48901`

**Response** (parsed):

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
- Introduced: 0 (all versions from the start)
- Fixed: **0.4.8** (from `affected[].ranges[].events[].fixed` field)

## 3. Cross-Validation Table

| Source | Product | Affected Range | Fix Threshold |
|--------|---------|----------------|---------------|
| Jira description | h2 | "versions prior to the fix" (imprecise) | "see advisory" (imprecise) |
| MITRE CVE API | h2 (hyperium) | < 0.4.8 (semver) | **0.4.8** |
| OSV.dev | h2 (crates.io) | introduced: 0, fixed: 0.4.8 | **0.4.8** |

### Cross-Validation Result: AGREEMENT

Both external sources (MITRE CVE API and OSV.dev) agree on the fix threshold: **0.4.8**. The Jira description did not provide a precise threshold, so the external data fills the gap rather than contradicting it.

## Enriched Fix Threshold

**Authoritative fix threshold: 0.4.8**

- Source: MITRE CVE API (`lessThan: 0.4.8`) and OSV.dev (`fixed: 0.4.8`) -- cross-validated
- Versions < 0.4.8 are affected; versions >= 0.4.8 are NOT affected
- This enriched threshold replaces the imprecise Jira description data for Step 2.3 version impact comparisons

The enriched fix threshold (0.4.8) will be used as the authoritative value for version impact comparisons in Step 2.3.
