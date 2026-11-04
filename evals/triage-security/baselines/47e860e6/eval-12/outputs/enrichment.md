# Step 1.5 – External CVE Data Enrichment: CVE-2026-48901 (h2)

External sources are always queried (not just as a fallback). In this eval the
mock responses embedded in the fixture were used in place of WebFetch.

## 1. MITRE CVE API

Source: `https://cveawg.mitre.org/api/cve/CVE-2026-48901` (mock response)

| Field | Value |
|---|---|
| Vendor / product | hyperium / h2 |
| status | affected |
| versionType | semver |
| `lessThan` | **0.4.8** |
| `lessThanOrEqual` | — (not present) |
| Derived affected range | `< 0.4.8` (exclusive upper bound) |
| Derived fixed version | **0.4.8** |

## 2. OSV.dev API

Source: `https://api.osv.dev/v1/vulns/CVE-2026-48901` (mock response)

| Field | Value |
|---|---|
| OSV ID | RUSTSEC-2026-0089 (alias CVE-2026-48901) |
| Ecosystem / package | crates.io / h2 |
| Range type | SEMVER |
| `introduced` | 0 |
| `fixed` | **0.4.8** |
| `last_affected` | — (not present) |
| Derived affected range | `>= 0, < 0.4.8` |
| Derived fixed version | **0.4.8** |

## 3. Cross-validation

Fix threshold comparison for CVE-2026-48901 (h2):

| Source | Affected range | Fixed version | Machine-readable? |
|---|---|---|---|
| Jira description | "versions prior to the fix" | "see advisory" | No — imprecise prose, no numeric threshold |
| MITRE CVE API | < 0.4.8 | 0.4.8 | Yes (`lessThan`) |
| OSV.dev | >= 0, < 0.4.8 | 0.4.8 | Yes (`introduced`/`fixed`) |

### Result: Agreement (no conflict)

- MITRE and OSV.dev agree exactly: affected `< 0.4.8`, fixed in `0.4.8`.
- The Jira description does not contradict them — it simply provides no numeric
  threshold ("prior to the fix" is consistent with `< 0.4.8`). There is therefore
  no disagreement to escalate, and no engineer comparison prompt is required.
- Per Step 1.5 precedence rules, the structured external data is authoritative
  because it gives machine-readable constraints rather than prose.

### Enriched fix threshold (passed to Step 2.3)

- **Affected: h2 < 0.4.8**
- **Fixed: h2 >= 0.4.8**
- Boundary semantics: `lessThan` / `fixed` are exclusive — **h2 0.4.8 itself is
  NOT affected**.
- Confidence: high (two independent structured sources agree).

### Note on the Jira data

Without enrichment, Step 2 could not have produced any YES/NO determination (no
threshold to compare against) and Step 1 would have had to stop and ask the
engineer. Recommend noting in the post-triage summary that the description's
affected range was imprecise and was resolved from MITRE/OSV.

## Step 1.7 – Embargo Check

CVSS 7.5 meets the >= 7.0 threshold, but no Embargo policy URL is configured in
Security Configuration → step skipped silently per skill rules.
