# Triage Outcome: TC-8011 (CVE-2026-45678, webpack, [rhtpa-2.2])

## Decision

**Do not close. The cross-CVE overlap does not cover this CVE, so new remediation is required.** Version impact for npm cannot be confirmed automatically and needs manual assessment before tasks are finalized.

## Rationale

1. **The cross-CVE overlap does not cover this CVE (Step 4.3).** The only related CVE on the same component, PS component, and stream is TC-8012 (CVE-2026-43210). Its remediation task, TC-8013, bumped webpack to **5.96.1**. CVE-2026-45678 needs **>= 5.98.0**. Because 5.96.1 < 5.98.0, TC-8013 leaves rhtpa-ui on a vulnerable webpack. That rules out closing as covered, and no Related or Depend links to TC-8012 or TC-8013 are created, since those belong only to the covering branch.
2. **No duplicates or preemptive tasks (Steps 4.1, 4.2, 4.4).** No sibling Vulnerability issues carry CVE-2026-45678, and no `security-preemptive` task exists for it.
3. **Version impact (Step 2) is blocked for npm.** webpack is an npm package, but the 2.2.x security matrix's Ecosystem Mappings table lists only Cargo and RPM. rhtpa-ui is also missing from Source Repositories. The skill's rule applies: *"Unsupported ecosystem: npm is not yet supported for automated triage. Manual assessment is required."* No lock-file evidence exists for webpack, so no version-impact table can be built and Affects Versions cannot be verified.
   - Indirect evidence: TC-8013's description says rhtpa-ui went from webpack 5.95.0 to 5.96.1 on the 2.2 stream. Both versions are below 5.98.0, so the 2.2.x stream is very likely affected. Under the "do not fabricate data" rule this is a hint, not lock-file evidence.
4. **Step 3 Affects Versions:** RHTPA 2.2.0 (PSIRT-assigned) stays unchanged until a lock-file check confirms which 2.2.x releases (2.2.0–2.2.4) ship webpack < 5.98.0.
5. **Step 5 lifecycle and Step 6 already-fixed:** neither applies.
   - The lifecycle check was not performed because external calls are not allowed.
   - No resolved sibling for this CVE exists, and TC-8012 is a different CVE whose fix falls short.
6. **Step 7 concurrent triage:** no other open webpack CVE is under active triage. TC-8012 is Closed.
7. **Step 7.5.3 dedup:** TC-8013 must **not** be treated as covering. It matches on component but is below the threshold and is Closed, so the stream is not dedup'd.

## Proposed Step 8 action (Case B, needs engineer confirmation and manual npm impact check)

The issue is scoped to 2.2.x. Two tasks for the 2.2.x stream fit the source-dependency (npm) category:

1. **Dependency bump task:** "Bump webpack to >= 5.98.0 in rhtpa-ui [rhtpa-2.2]". Use the bump variant if the rhtpa-ui 2.2 upstream branch can take 5.98.0; otherwise use an upstream backport. Labels: `CVE-2026-45678`, plus a `dev-dependency` label and Normal priority if webpack is confirmed to be build-only. Link: TC-8011 Depend this task.
2. **Downstream propagation task:** propagate the fixed rhtpa-ui into the rhtpa-release.0.4.z Konflux repo. The bump task blocks this one, and TC-8011 Depend this task.
3. Link both tasks to the RHTPA 2.2.x release Task (Blocks), and link TC-8011 to the release Task (Related), if Step 7.5 finds or creates one.

Case A cross-stream check: no data shows whether the 2.1.x stream ships rhtpa-ui or webpack. Manual assessment is needed before preemptive tasks for 2.1.x are considered.

## Prerequisites and warnings to resolve

- Security matrix is **152 days stale** (Last-Updated 2026-06-28). Refresh it.
- Add an **npm ecosystem mapping** (rhtpa-ui, `package-lock.json`) to the stream matrices, and add **rhtpa-ui** to Source Repositories. Automated version impact needs both.
- Add the Upstream Affected Component, PS Component, and Stream custom fields (`customfield_10632`, `customfield_10669`, `customfield_10832`) to the Security Configuration. Step 4.3 and Step 7 depend on them.
- Fix threshold confidence is reduced because the external CVE databases (MITRE and OSV) were not consulted.
- The due date of 2026-08-15 has passed.

## Post-triage (proposed, not executed)
- Add the `ai-cve-triaged` label to TC-8011.
- Post a summary comment covering four items, ending with an @mention of the reporter and the Comment Footnote:
  - the overlap finding (TC-8013 at 5.96.1 does not cover 5.98.0)
  - the npm manual-assessment note
  - the proposed remediation tasks
  - the release Jira references

No Jira mutations, git commands, or external calls were executed in this eval run.
