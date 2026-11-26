# Triage Outcome: TC-8011 (CVE-2026-45678, webpack, [rhtpa-2.2])

## Decision

**Remediation needed (Case B). Do not close as covered by cross-CVE overlap.**

The only related same-component, same-stream CVE is TC-8012 (CVE-2026-43210). Its remediation task TC-8013 bumped webpack to **5.96.1**. This CVE's fix threshold is **5.98.0**. Since 5.96.1 < 5.98.0, the existing remediation does not cover CVE-2026-45678. A new remediation is needed to bring webpack to >= 5.98.0 in rhtpa-ui for the 2.2.x stream.

## Step-by-step summary

| Step | Result |
|---|---|
| 0 Config | Pass. Gaps: the custom fields (10632/10669/10832) are not declared in Security Configuration, and no ProdSec ID or embargo URL is configured |
| 0.3 Staleness | Matrix is 151 days old (> 14). A real run would warn and ask Refresh / Proceed / Stop |
| 0.8 Assign | Would assign TC-8011 to the current user and transition New -> Assigned (not executed) |
| 1 Extraction | CVE-2026-45678, webpack, < 5.98.0, fixed in 5.98.0, CVSS 7.8, scoped to 2.2.x |
| 1.5 Enrichment | Not run (eval). Using the Jira value 5.98.0 with reduced confidence |
| 1.7 Embargo | Skipped (no policy URL configured) |
| 2 Version impact | **Blocked for evidence.** npm/rhtpa-ui is not in the 2.2.x Ecosystem Mappings, and the mock has no webpack lock data. No per-version table can be produced without fabricating data. Manual assessment, or adding npm/rhtpa-ui to the matrix, is required |
| 3 Affects Versions | Not changed. PSIRT's RHTPA 2.2.0 is unverified, so there is no evidence-backed correction |
| 4.1/4.2 Siblings | None |
| 4.3 Cross-CVE overlap | TC-8012 -> TC-8013 bumps to 5.96.1, **below** 5.98.0, so **not covered** |
| 4.4 Preemptive | None |
| 5 Lifecycle | Not fetched (eval). Must confirm 2.2.x is supported |
| 6 Already fixed | No same-CVE resolved siblings. TC-8012 is a different CVE and its fix is insufficient |
| 7 Concurrent triage | No In Progress / Code Review webpack CVEs in the provided data |
| 7.5 Release Jira | Find or create the RHTPA 2.2.x release Epic and "CVE triage" Task. Proposed default version is 2.2.5 (latest matrix release 2.2.4 + 1, needs confirmation). **7.5.3 dedup must not match TC-8013**: a component-only match would be a false positive, and TC-8013 is Closed |
| 8 Remediation | Case B for 2.2.x. Case A (cross-stream) cannot be assessed without npm lock evidence for 2.1.x |

## Proposed remediation (pending engineer confirmation)

The ecosystem is npm, a source dependency, so **2 tasks** are created for stream 2.2.x:

1. **Upstream task.** If Step 2.5 confirms the rhtpa-ui release branch already ships webpack >= 5.98.0, this is a dependency bump. Otherwise it is an upstream backport. Summary: "Bump webpack to >= 5.98.0 in rhtpa-ui [rhtpa-2.2]" for CVE-2026-45678. Labels: CVE-2026-45678 plus the standard remediation labels. Link: Depend from TC-8011. Implementation Notes: upgrade from 5.96.1 (after TC-8013) to >= 5.98.0. If webpack is build-only/dev-only, add the `dev-dependency` label and set priority to Normal. Include upstream coordination guidance (default deployment context).
2. **Downstream propagation task** in the Konflux release repo rhtpa-release.0.4.z. It is blocked by task 1 (Blocks) and linked Depend from TC-8011.

Then link both tasks to the release Task (Blocks) and link TC-8011 to the release Task (Related).

Optional, for traceability: a Related link TC-8011 <-> TC-8012 (same upstream component). Step 4.3 does not require it because no overlap was confirmed.

## Post-triage (after confirmation)

- Add the `ai-cve-triaged` label to TC-8011.
- Post a summary comment with: the version impact status (blocked, needs manual npm evidence), the Step 4.3 finding (TC-8013 at 5.96.1 does not cover the 5.98.0 threshold), the remediation task keys, and the release Jira keys. Include an @mention of the issue reporter and the triage-security Comment Footnote.

## Open items before any Jira mutation

1. Add npm / rhtpa-ui to the 2.2.x (and 2.1.x) Ecosystem Mappings and Source Repositories, or do a manual lock-file check, to confirm the shipped webpack versions per release.
2. Refresh the stale security matrix.
3. Declare the Upstream Affected Component, PS Component and Stream fields in Security Configuration.
4. Cross-check 5.98.0 against MITRE and OSV.
5. Note the due date (2026-08-15) has already passed.

No Jira, git or external calls were made. All actions above are proposals.
