# Step 1.5 -- External CVE Data Enrichment

## CVE-2026-48901 (h2)

### MITRE CVE API Response

Source: `https://cveawg.mitre.org/api/cve/CVE-2026-48901`

Parsed data:
- Product: h2
- Vendor: hyperium
- Affected versions: lessThan **0.4.8** (semver)
- Status: affected
- Fix threshold: **0.4.8**

### OSV.dev API Response

Source: `https://api.osv.dev/v1/vulns/CVE-2026-48901`

Parsed data:
- ID: RUSTSEC-2026-0089
- Aliases: CVE-2026-48901
- Package: h2 (ecosystem: crates.io)
- Affected range: introduced **0**, fixed **0.4.8** (SEMVER)
- Fix threshold: **0.4.8**

### Cross-Validation Table

| Source | Affected range | Fixed version | Precision |
|--------|---------------|---------------|-----------|
| Jira description | "versions prior to the fix" | "see advisory" | Imprecise -- no specific version threshold |
| MITRE CVE API | < 0.4.8 (semver) | 0.4.8 | Precise -- structured lessThan constraint |
| OSV.dev | introduced 0, fixed 0.4.8 | 0.4.8 | Precise -- structured semver range with fixed event |

### Cross-Validation Result

**Agreement**: MITRE CVE API and OSV.dev both report the fix threshold as **0.4.8**. The Jira description was imprecise ("versions prior to the fix" / "see advisory") but is consistent with the external data -- it simply lacked specificity.

Both external sources provide machine-readable, structured version constraints that agree:
- MITRE: `lessThan: "0.4.8"` with `versionType: "semver"`
- OSV.dev: `events: [{"introduced": "0"}, {"fixed": "0.4.8"}]`

### Enriched Fix Threshold

**Fix threshold for Step 2.3: h2 >= 0.4.8**

All versions of h2 prior to 0.4.8 are vulnerable. Versions 0.4.8 and later include the fix.

This enriched threshold supersedes the imprecise Jira description data and will be used for all version impact comparisons in Step 2.3.
