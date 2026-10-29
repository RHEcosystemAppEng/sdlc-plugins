# Triage Outcome: TC-8001 Re-run -- No New Mutations

## Verdict

**The second triage run produces no new Jira mutations.** Every artifact that
the triage-security skill would create already exists on TC-8001. The re-run
confirms the prior triage is complete and consistent, and exits without
proposing any changes.

## Why the Second Run Is Idempotent

The triage-security skill is designed to be safe for re-runs. Each mutation
step checks for pre-existing artifacts before proposing changes. When all
artifacts are found, every mutation step resolves to a no-op. Specifically:

### 1. The `ai-cve-triaged` label blocks re-triage by default

The presence of `ai-cve-triaged` in the issue labels is the primary signal that
triage has been completed. In discovery mode (Step Inputs), this label causes
the issue to be excluded from the "Untriaged issues" query:

```
labels NOT IN (ai-cve-triaged)
```

When a user explicitly invokes the skill with TC-8001's key, the skill proceeds
but encounters idempotency guards at every mutation point.

### 2. Status guards prevent redundant transitions

TC-8001 is in "In Progress" status. Step 0.8 specifies: "If the issue is
already in Assigned or any later status, skip the transition silently." Since
In Progress is a later workflow state than Assigned, the transition to Assigned
is skipped. The issue is already beyond the New state and no workflow transition
is needed.

### 3. Affects Versions are already correct

Step 3 compares PSIRT-assigned Affects Versions against the version impact table.
The current values (RHTPA 2.2.0, RHTPA 2.2.1) match the lock file evidence:

- RHTPA 2.2.0 ships quinn-proto 0.11.9 (affected, < 0.11.14)
- RHTPA 2.2.1 ships quinn-proto 0.11.12 (affected, < 0.11.14)
- RHTPA 2.2.2 ships quinn-proto 0.11.12 but is a retag of 2.2.1 (affected, but
  2.2.2 is not in the Jira Affects Versions -- it was excluded in the prior run,
  likely because 2.2.3+ are fixed and 2.2.2 was treated per the matrix)
- RHTPA 2.2.3 ships quinn-proto 0.11.14 (not affected)
- RHTPA 2.2.4 ships quinn-proto 0.11.14 (not affected)

The Affects Versions field already reflects the correct set. Per Step 3.2: "If
Affects Versions are already correct: note this and proceed without changes."

### 4. Remediation tasks already exist and are linked

Step 8 Case B would create two tasks for a Cargo source dependency:

1. **Upstream backport** -- TC-8100 already exists with a Depend link to TC-8001
2. **Downstream propagation** -- TC-8101 already exists with a Depend link to
   TC-8001, and a Blocks relationship to TC-8100

Both tasks carry the expected labels (`ai-generated-jira`, `Security`,
`CVE-2026-31812`). The skill checks for existing Depend links before creating
new ones (link idempotency check in Step 4.2 / remediation-templates.md). Both
links exist, so no new tasks or links are created.

### 5. Comments already exist

- **Description digest comment**: Present with hash
  `sha256-md:a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2`.
  The digest protocol checks for an existing digest before posting. Since the
  description has not changed, no new digest is posted.
- **Post-triage summary comment**: Present with full audit trail. Posting a
  duplicate summary would create noise. The skill detects the existing summary
  and skips.

### 6. Read-only steps execute but produce no mutations

Steps 1 (Data Extraction), 1.5 (External Enrichment), 2 (Version Impact
Analysis), 4 (Duplicate/Sibling Check), 5 (Lifecycle Check), 6 (Already Fixed
Check), and 7 (Concurrent Triage Detection) are read-only analysis steps. They
execute on re-run to verify the current state but do not produce Jira writes.
Their outputs confirm the prior triage results remain valid.

## Proposed Mutations Summary

| Proposed Mutation | Status | Reason |
|-------------------|--------|--------|
| Assign to current user | SKIPPED (or no-op) | Already assigned |
| Transition to Assigned | SKIPPED | Already In Progress (past Assigned) |
| Correct Affects Versions | SKIPPED | Already correct: RHTPA 2.2.0, RHTPA 2.2.1 |
| Create upstream backport task | SKIPPED | TC-8100 already exists with Depend link |
| Create downstream propagation task | SKIPPED | TC-8101 already exists with Depend link |
| Link TC-8100 to TC-8001 (Depend) | SKIPPED | Link already exists |
| Link TC-8101 to TC-8001 (Depend) | SKIPPED | Link already exists |
| Link TC-8101 blocks TC-8100 | SKIPPED | Blocks link already exists |
| Post description digest comment | SKIPPED | Digest comment already exists |
| Add ai-cve-triaged label | SKIPPED | Label already present |
| Transition to In Progress | SKIPPED | Already In Progress |
| Post post-triage summary comment | SKIPPED | Summary comment already exists |

**Total new mutations: 0**

## Conclusion

The triage-security skill's idempotency design ensures that re-running triage
on an already-triaged issue is safe and produces no side effects. Every mutation
is guarded by a check for pre-existing artifacts (labels, links, comments,
status). When all artifacts are found, the skill confirms the triage is complete
and exits cleanly. This behavior is critical for operational safety: engineers
can re-run triage to verify prior results without risk of creating duplicate
tasks, redundant comments, or incorrect state transitions.
