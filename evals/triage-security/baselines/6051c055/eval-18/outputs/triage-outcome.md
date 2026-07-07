# Triage Outcome: TC-8001 (Re-Run) -- No New Mutations

## Conclusion

The second run of triage-security on TC-8001 produces **zero new mutations**.
Every triage artifact that the skill would normally create already exists on
the issue from the first triage run. The skill detects each artifact and skips
the corresponding write operation.

## Why the Second Run Is a No-Op

### 1. The `ai-cve-triaged` label gates re-triage awareness

The presence of the `ai-cve-triaged` label on TC-8001 is the primary signal
that this issue has already been triaged. In discovery mode, this label causes
the issue to be excluded from the "Untriaged issues" query (which filters
`labels NOT IN (ai-cve-triaged)`). When invoked directly with the issue key
(as in this re-run), the skill proceeds through Step 1 data extraction but
detects the label and all other artifacts during subsequent steps.

### 2. Status-aware handling triggers an early warning

Per the SKILL.md status-aware handling rules, when the issue is in `In Progress`
status, the skill warns: "This issue is already in In Progress. It may be
actively worked on." The engineer is asked whether to proceed with triage
anyway or skip. If proceeding, the skill continues but with the understanding
that this is a verification pass, not a first triage.

### 3. Step-by-step idempotency analysis

| Step | Normal Action | Re-Run Behavior | Reason |
|------|--------------|-----------------|--------|
| 0.7 (Assign + Transition) | Assign to current user, transition to Assigned | Skip transition (already past Assigned); assignment may update but is idempotent | Status is In Progress, which is later than Assigned |
| 1 (Data Extraction) | Parse CVE data from issue | Executes normally -- data extraction is read-only | No mutation; reads always succeed |
| 1.5 (External Enrichment) | Query MITRE/OSV APIs | Executes normally -- external queries are read-only | No mutation; enrichment is additive context |
| 2 (Version Impact) | Analyze lock files at pinned commits | Executes normally -- git show commands are read-only | No mutation; produces the same version impact table |
| 3 (Affects Versions) | Correct Affects Versions if wrong | Skip -- Affects Versions already correct (RHTPA 2.2.0, 2.2.1) | First run already corrected them |
| 4 (Duplicates/Siblings) | Search for siblings, create links | Skip link creation -- any sibling links from first run already exist | Idempotent link check (Step 4.2 pattern) |
| 4.3 (Cross-CVE Overlap) | Search for overlapping CVEs | Executes search (read-only); any links already created | Idempotent link check before creation |
| 4.4 (Preemptive Reconciliation) | Search for preemptive tasks | Executes search (read-only); no preemptive tasks expected | No mutation path triggered |
| 5 (Lifecycle Check) | Verify versions are supported | Executes normally -- read-only lifecycle page fetch | No mutation; informational check |
| 6 (Already Fixed) | Check resolved siblings | Executes normally -- read-only JQL reuse | No mutation; informational check |
| 7 (Concurrent Triage) | Check for concurrent triages | Executes normally -- read-only JQL search | No mutation; informational check |
| 8 (Remediation) | Create remediation tasks + links | Skip -- TC-8100 and TC-8101 already exist and are linked via Depend | Existing Depend links detected in issuelinks |
| Post-Triage: Label | Add ai-cve-triaged | Skip -- label already present | Detected in labels array |
| Post-Triage: Digest | Post description digest comment | Skip -- digest comment already exists (comment #1) | Detected by matching comment pattern |
| Post-Triage: Summary | Post post-triage summary comment | Skip -- summary comment already exists (comment #2) | Detected by matching comment pattern |

### 4. Root cause: the skill's idempotency design

The triage-security skill achieves idempotency through several mechanisms:

1. **Label-based triage marker**: The `ai-cve-triaged` label serves as a
   durable marker that the issue has been triaged. Discovery mode filters
   it out; direct invocation detects it during post-triage.

2. **Issue link existence checks**: Before creating any link (Depend, Related),
   the skill checks the issue's existing `issuelinks` array for a matching
   link with the same type and target key. This is explicitly documented in
   Steps 4.2, 4.3, and the remediation templates.

3. **Comment pattern matching**: The description digest and post-triage summary
   comments follow recognizable patterns (prefix `[sdlc-workflow] Description
   digest:` and the comment footnote format). The re-run detects these existing
   comments and skips posting duplicates.

4. **Status-aware gating**: The status field (In Progress) signals that triage
   has already progressed past the initial New state. Step 0.7 skips the
   Assigned transition when the issue is already in a later state.

5. **Affects Versions comparison**: Step 3 compares the current Affects Versions
   against the version impact table. If they already match, no correction is
   issued.

### 5. What would trigger mutations on a re-run

A re-run would produce new mutations only if the issue state had changed
between runs:

- **Description changed**: A new description digest comment would be posted
  (different hash from the existing one).
- **New product versions released**: The version impact table might show
  additional affected versions, triggering an Affects Versions correction.
- **Remediation tasks deleted or unlinked**: If TC-8100 or TC-8101 were
  removed, the skill would create new remediation tasks.
- **Label removed**: If `ai-cve-triaged` were removed, the post-triage phase
  would re-add it.
- **Status reset to New**: Step 0.7 would re-assign and re-transition.

None of these conditions apply in this re-run. The issue is in the exact state
the first triage left it in.

## Final Disposition

- **Mutations attempted**: 0
- **Mutations skipped (idempotent)**: 6
  - ai-cve-triaged label addition
  - Status transition
  - Remediation task creation (TC-8100 upstream backport)
  - Remediation task creation (TC-8101 downstream propagation)
  - Description digest comment
  - Post-triage summary comment
- **Read-only operations executed**: Data extraction, version impact analysis,
  sibling/duplicate search, lifecycle check, already-fixed check
- **Outcome**: No new Jira mutations. The issue remains in its current state
  with all triage artifacts intact from the first run.
