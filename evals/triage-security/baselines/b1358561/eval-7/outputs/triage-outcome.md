# Triage Outcome: How Step 4.2 Handled the Pre-existing Related Link (TC-8006)

## Summary

TC-8006 (`[rhtpa-2.1]`, stream 2.1.x) has one sibling for CVE-2026-31812: TC-8001
(`[rhtpa-2.2]`, stream 2.2.x, In Progress). The two issues are in different streams, so
TC-8001 is a **cross-stream companion tracker** and not a duplicate. Step 4.2 therefore
applies.

## Idempotent link handling

Step 4.2 says to **check for an existing link before creating one**, using the
`issuelinks` array already fetched in Step 1 (no extra Jira call). TC-8006 already has:

- Link ID **1990401**, type **Related**, outward direction (TC-8006 → TC-8001)

The check matches when `type.name` is `"Related"` **and** either `inwardIssue.key`
**or** `outwardIssue.key` equals the sibling key. Direction does not matter. Here
`outwardIssue.key = TC-8001`, so the condition holds.

**Action taken:** link creation was skipped and this was logged:

> "Related link to TC-8001 already exists — skipping"

`jira.create_link(TC-8006, TC-8001, "Related")` was **not** issued. Re-running triage
on an issue that PSIRT or an earlier triage pass already linked therefore does not create a
duplicate Related link. The operation is idempotent. No engineer confirmation was needed,
because no mutation was proposed for the link.

## Other Step 4.2 checks

- **Affects Versions overlap:** none. TC-8006 has 2.1.x versions only (RHTPA 2.1.0, with RHTPA
  2.1.1 proposed in Step 3). TC-8001 has 2.2.x versions only (RHTPA 2.2.0, RHTPA 2.2.1).
- **Sibling landscape** was shown to the engineer (see `sibling-check.md`).
- **4.1 Duplicate closure:** not applicable, because there is no same-stream sibling.
- **4.3:** skipped, because the Upstream Affected Component field is not configured.
- **4.4:** no matching `security-preemptive` task.

## Downstream implications

- TC-8006 stays open and is the scoped tracker for 2.1.x. Both 2.1.0 and 2.1.1 ship
  quinn-proto 0.11.9, which is below 0.11.14, so they are affected.
- The 2.2.x stream is also affected (2.2.0–2.2.2). Under Step 8 Case A, a cross-stream impact
  comment would point at TC-8001 as the 2.2.x tracker. The existing Related link already
  connects the two issues, so no new link is needed for that.
- Remediation for 2.1.x (Case B, Cargo source dependency, 2 tasks: upstream backport or bump on
  `release/0.3.z` plus downstream propagation to rhtpa-release.0.3.z) would follow after
  confirmation. That is outside the scope of this Step 4.2 assessment.

## Jira writes performed in this eval

None. Per the eval instructions, no Jira MCP, git, or external calls were made. The only
link-related decision was a **skip**, so no write would have been needed even in a live
run.
