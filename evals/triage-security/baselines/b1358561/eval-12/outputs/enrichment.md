# Step 1.5 – External CVE Data Enrichment: CVE-2026-48901 (h2)

External sources are always queried. This step is not just a fallback. In this eval the fixture's mock responses stand in for the WebFetch calls. No network calls were made.

## 1. MITRE CVE API

Source: `https://cveawg.mitre.org/api/cve/CVE-2026-48901` (mock response)

| Field | Value |
|---|---|
| Vendor / product | hyperium / h2 |
| Status | affected |
| `lessThan` | **0.4.8** |
| `lessThanOrEqual` | (not present) |
| versionType | semver |
| Derived affected range | `< 0.4.8` |
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
| `last_affected` | (not present) |
| Derived affected range | `>= 0, < 0.4.8` |

The OSV ID matches the RustSec advisory listed in the Jira description references (RUSTSEC-2026-0089). The ecosystem (crates.io) matches the Cargo detection from Step 1.

## 3. Cross-Validation

Fix threshold comparison for CVE-2026-48901 (h2):

| Source | Affected range | Fixed version | Precision |
|---|---|---|---|
| Jira description | "versions prior to the fix" | "see advisory" | Imprecise prose, no numeric threshold |
| MITRE CVE API | < 0.4.8 | 0.4.8 | Structured (`lessThan`) |
| OSV.dev | >= 0, < 0.4.8 | 0.4.8 | Structured (`introduced`/`fixed`) |

### Result: Agreement (external sources concur; Jira has no conflicting value)

- MITRE and OSV.dev agree exactly: affected `< 0.4.8`, fixed in `0.4.8`.
- The Jira description has no numeric threshold, so it does **not contradict** the external data. "Versions prior to the fix" is consistent with `< 0.4.8`. Because nothing conflicts, the disagreement gate (asking the engineer to pick a source) does not trigger.
- Per the precedence rule, the structured external data is **authoritative**. It gives machine-readable version constraints where the Jira text is prose.
- Neither external API was unavailable, so confidence is not degraded.

## Enriched Fix Threshold (passed to Step 2.3)

| Item | Value |
|---|---|
| Library | h2 (crates.io) |
| Affected range | **< 0.4.8** (introduced 0) |
| Fixed version | **0.4.8** |
| Boundary semantics | `lessThan` is exclusive, so h2 **0.4.8 itself is NOT affected** |
| Threshold source | MITRE CVE API + OSV.dev (cross-validated) |
| Confidence | High |

Without this enrichment, the Step 2 comparison could not be done, because the Jira text gives no threshold to compare lock-file versions against. The enriched threshold matters here: build v0.4.5 (RHTPA 2.2.0) ships h2 exactly 0.4.8, which sits on the fix boundary.

## Step 1.7 – Embargo Check

No Embargo policy URL is configured in Security Configuration, so this step is **skipped silently**, even though CVSS 7.5 (High) would meet the >= 7.0 trigger threshold.
