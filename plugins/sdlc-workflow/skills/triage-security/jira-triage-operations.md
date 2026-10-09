# Jira Triage Operations

This companion file contains the detailed procedures for Steps 3–6 of the
triage-security skill. These steps handle Affects Versions correction,
duplicate and sibling detection, cross-CVE overlap detection, preemptive task
reconciliation, version lifecycle checks, and already-fixed detection.

## Fullsend action mapping

This file's interactive procedures and confirmation prompts are unchanged when
`FULLSEND_OUTPUT_DIR` is absent. In Fullsend mode, use only validated trusted input
and `authorization.mutation_authorized`; never call Jira or ask the engineer to
confirm a sandbox action.

If authorization is false, do not serialize any mutation from Steps 3–7. Return the
top-level evidence-backed report-only result with exactly its one `report-only`
action, and name each withheld correction, link, closure, assignment, label update,
or comment in the report. If authorization is true, map each write one-for-one to
the existing result-schema types below. Every marker is stable and unique in the
form `triage-security:<lowercase-issue>:<operation>:<target>` (using only
schema-valid marker characters), and existing `idempotency.action_markers` or trusted
existing artifacts mean the action is omitted on retry.

| Procedure write | Fullsend action |
|---|---|
| Affects Versions correction, VEX value, assignment, add/remove label, resolution | `field-edit` |
| Assigned, In Progress, Closed | `status-transition` |
| Affects Versions, duplicate, overlap, lifecycle, already-fixed, reconciliation, and skip comments | `comment` with `body_adf` |
| Related, Depend, Blocks links | `link` with the same `link_type` |

Build all comment bodies as ADF documents, retaining required Comment Footnotes and
ProdSec mentions. Step 4.4 reconciliation is specifically a `link` action for the
new `Depend` relationship and a `field-edit` action that removes
`security-preemptive`; it is never a direct Jira update in the sandbox. Keep the
skill's step order, and defer comments that list newly created tasks until the
executor-owned `remediation-task` action has registered each task reference and
posted its description digest exactly once, followed by that task's links. Do not
serialize a separate digest comment or post-creation `resolve-reference` action.

## Step 3 – Affects Versions Correction

### 3.1 – Discover available Jira versions

Before correcting Affects Versions, dynamically discover what version values exist
in the Jira project. This is done via API — no hardcoded version IDs.

1. Call `getJiraIssueTypeMetaWithFields` for the Vulnerability issue type:
   ```
   jira.getJiraIssueTypeMetaWithFields(
     projectIdOrKey: "<project-key>",
     issueTypeId: "<vulnerability-issue-type-id>"
   )
   ```
2. Extract the `versions` field's `allowedValues` array. Each entry contains:
   - `id` — the Jira version ID (used for mutations)
   - `name` — the display name (e.g., `MYPRODUCT 2.1.0`)
   - `released` — boolean indicating release status
   - `releaseDate` — planned or actual release date
3. Filter by the Jira version prefix (e.g., `MYPRODUCT`) to exclude unrelated versions
   (Helm Charts, Operators, DA releases, etc.).

Present the filtered version registry:

```
Jira Versions matching "<prefix>":

| Jira ID | Name        | Released | Release Date |
|---------|-------------|----------|--------------|
| 62643   | MYPRODUCT 2.1.0 | yes      | 2025-07-27   |
| 62604   | MYPRODUCT 2.1.1 | yes      | 2025-09-16   |
| ...     | ...         | ...      | ...          |
| 104611  | MYPRODUCT 3.0   | no       | 2026-06-30   |
```

### 3.2 – Compare and correct Affects Versions

**Scope the correction to the issue's stream.** If the issue has a stream scope
(from Step 1 stream scope resolution), only include versions belonging to that
stream. If the issue is unscoped, include all affected versions across all streams.

Example for a **scoped** issue with suffix `[myproduct-2.2]`:
- Version impact table shows: MYPRODUCT 2.1.0 (YES), 2.1.1 (YES), 2.2.0 (YES), 2.2.1 (YES)
- This issue is scoped to stream `2.2.x` → only propose: `[MYPRODUCT 2.2.0, MYPRODUCT 2.2.1]`
- The 2.1.x versions belong to a sibling issue (see Step 4)

Compare the PSIRT-assigned Affects Versions (from the Jira `versions` field) against
the **stream-scoped** version impact table:

- **If PSIRT version is wrong** (e.g., "MYPRODUCT 2.0.0" when 2.0 doesn't exist):
  - Show the diff: `Current: [MYPRODUCT 2.0.0] → Proposed: [MYPRODUCT 2.2.0, MYPRODUCT 2.2.1]`
  - Present correction to engineer for confirmation

- **If PSIRT version is correct but incomplete**:
  - Show the additions: `Current: [MYPRODUCT 2.2.0] → Proposed: [MYPRODUCT 2.2.0, MYPRODUCT 2.2.1]`
  - Present correction to engineer for confirmation

- **If the version impact table includes versions not registered in Jira**:
  - Flag: "MYPRODUCT X.Y.Z is in the supportability matrix but has no matching Jira
    version — notify project admin"
  - Continue with available versions; do not block triage

- **If Affects Versions are already correct**: note this and proceed without changes.

**After engineer confirmation**, update the Affects Versions:

```
jira.edit_issue(<jira-issue-id>, fields={
  "versions": [{"id": "<version-id-1>"}, {"id": "<version-id-2>"}, ...]
})
```

Use the Jira version IDs discovered in Step 3.1, not hardcoded values.

**Include development stream versions**: if the issue's stream includes the
development stream and it is affected (from Step 2.2), include the unreleased
Jira version in the Affects Versions correction. Unreleased versions are valid
Affects Versions values — they track that the CVE must be fixed before the next
release ships.

Add a comment documenting the correction. If a ProdSec Jira account ID is
configured in Security Configuration, append an @mention before the Comment
Footnote using an ADF mention node:

```json
{ "type": "mention", "attrs": { "id": "<prodsec-jira-account-id>", "text": "@<prodsec-name>" } }
```

If no ProdSec Jira account ID is configured, omit the @mention silently.

```
jira.add_comment(<jira-issue-id>, "Corrected Affects Versions: [old] → [new].
Based on lock file analysis at pinned commits from security-matrix.md.
Scoped to stream <stream> per issue suffix.
[ProdSec @mention if configured]")
```

## Step 4 – Duplicate, Sibling, and Overlap Check

Search for sibling Vulnerability issues with the same CVE label:

```
jira.search_jql(
  "project = <project-key> AND labels = '<CVE-ID>' AND issuetype = <vulnerability-issue-type-id> AND key != <current-issue-key>"
)
```

For each sibling found, parse its summary stream suffix (e.g., `[myproduct-2.0]`) to
determine its stream scope. Classify siblings into:

- **Same-stream siblings** — same stream suffix as the current issue (or both unscoped)
- **Different-stream siblings** — different stream suffix (companion trackers)

### 4.1 – Same-stream duplicates

If a same-stream sibling exists and is open or in progress:
- **Recommendation**: Close the current issue as Duplicate.
- Present the sibling issue key and its Affects Versions to the engineer.
- After confirmation:
  1. Add comment: "Duplicate of [sibling-key] — same CVE tracked for the same
     stream [stream]. Version impact analysis confirms overlap."
  2. Transition to Closed with resolution "Duplicate".
  3. Assign to current user.

### 4.2 – Cross-stream coordination

Different-stream siblings are **companion trackers**, not duplicates. PSIRT creates
one issue per stream intentionally. For each different-stream sibling:

1. **Check for existing link** before creating one. Read the current issue's
   `issuelinks` array from the `jira.get_issue` response (already fetched in
   Step 1). Check if any existing link satisfies all of:
   - `type.name` is `"Related"`
   - `inwardIssue.key` or `outwardIssue.key` matches the sibling key

   If a matching link exists, skip link creation and log:
   > "Related link to [sibling-key] already exists — skipping"

   If no matching link exists, create the link:
   ```
   jira.create_link(
     inwardIssue: <current-issue-key>,
     outwardIssue: <sibling-key>,
     type: "Related"
   )
   ```
2. **Verify no Affects Versions overlap** — each issue should only carry versions
   from its own stream. If overlap is detected (e.g., both issues claim MYPRODUCT 2.2.0),
   flag it to the engineer: "Version overlap detected between [current-key] and
   [sibling-key] — both claim [overlapping versions]. Please confirm which issue
   should own these versions."
3. **Present the sibling landscape** to the engineer:
   ```
   CVE-YYYY-XXXXX companion issues:

   | Issue     | Stream | Status      | Affects Versions          |
   |-----------|--------|-------------|---------------------------|
   | TC-1234   | 2.1.x  | In Progress | MYPRODUCT 2.1.0, MYPRODUCT 2.1.1 |
   | TC-5678 ← | 2.2.x  | New         | MYPRODUCT 2.2.0, MYPRODUCT 2.2.1 |
   ```

**If no siblings found**, proceed to Step 4.3.

### 4.3 – Cross-CVE overlap detection

Search for Vulnerability issues that affect the **same upstream component** as the
current issue, regardless of CVE ID. This detects cases where a different CVE's
remediation already bumped the library past the current CVE's fix threshold.

**Prerequisite:** This step requires the Upstream Affected Component custom field,
PS Component custom field, and Stream custom field to be configured in Security
Configuration (Step 0). If any of these fields are not configured, skip this step
entirely.

1. **Extract the Upstream Affected Component** from the current issue's
   `<upstream-affected-component-field>` (already fetched in Step 1 with
   `fields=["*all"]`). If the field is empty or not present, skip this step —
   cross-CVE overlap detection requires the component field to be populated.

2. **Search for related CVE Jiras** with the same component value:

   ```
   jira.search_jql(
     "project = <project-key> AND issuetype = <vulnerability-issue-type-id> AND cf[<upstream-affected-component-field-number>] ~ '<component-value>' AND key != <current-issue-key>",
     fields: ["summary", "status", "labels", "issuelinks", "<upstream-affected-component-field>", "<ps-component-field>", "<stream-field>"]
   )
   ```

   Where `<upstream-affected-component-field-number>` is the numeric portion of the
   configured field ID (e.g., `10632` from `customfield_10632`).

3. **Filter results** to matching PS Component (`<ps-component-field>`) and Stream
   (`<stream-field>`) values. Only issues that share the same PS Component and
   Stream as the current issue are relevant — different components or streams are
   tracked separately.

4. **Traverse issue links** on each matching CVE Jira. For each match, inspect
   its `issuelinks` array for linked remediation Tasks (link type `"Depend"` —
   the same link type used when `triage-security` creates remediation tasks).
   Fetch each linked remediation Task to inspect its description.

5. **Compare remediation coverage.** For each remediation Task found, extract
   the dependency version bump from its description (the target version the
   library is bumped to). Compare this version against the current CVE's fix
   threshold (from Step 1's Data Extraction — the "fixed version" field):

   - If the remediation task's bump version **meets or exceeds** the current
     CVE's fix threshold: the existing remediation already covers this CVE.
   - If the bump version is **below** the fix threshold: the existing
     remediation does not cover this CVE.

6. **Present findings** to the engineer. If a ProdSec Jira account ID is
   configured in Security Configuration, append an @mention before the Comment
   Footnote in any comments posted during this step, using an ADF mention node:

   ```json
   { "type": "mention", "attrs": { "id": "<prodsec-jira-account-id>", "text": "@<prodsec-name>" } }
   ```

   If no ProdSec Jira account ID is configured, omit the @mention silently.

   - **If a covering remediation exists:**

     Create traceability links and post an explanatory comment as soon as the
     overlap is confirmed (these record a factual relationship and must not be
     deferred to a closure decision):

     a. **Create Related link** between the current CVE and the related CVE
        (idempotent — check existing `issuelinks` first, same pattern as
        Step 4.2):

        Check the current issue's `issuelinks` array (already fetched in
        Step 1) for an existing link where `type.name` is `"Related"` and
        `inwardIssue.key` or `outwardIssue.key` matches the related CVE key.

        If a matching link exists, skip and log:
        > "Related link to [related-cve-key] already exists — skipping"

        If no matching link exists, create the link:
        ```
        jira.create_link(
          inwardIssue: <current-cve-key>,
          outwardIssue: <related-cve-key>,
          type: "Related"
        )
        ```

     b. **Create Depend link** from the covering remediation task to the
        current CVE (same link type as standard remediation linkage in
        `remediation-templates.md`):

        Check the current issue's `issuelinks` array for an existing link
        where `type.name` is `"Depend"` and `inwardIssue.key` or
        `outwardIssue.key` matches the covering task key.

        If a matching link exists, skip and log:
        > "Depend link to [covering-task-key] already exists — skipping"

        If no matching link exists, create the link:
        ```
        jira.create_link(
          inwardIssue: <current-cve-key>,
          outwardIssue: <covering-task-key>,
          type: "Depend"
        )
        ```

     c. **Post a comment** on the current CVE documenting the cross-CVE
        overlap finding. If a ProdSec Jira account ID is configured, include
        an @mention before the Comment Footnote:
        ```
        Cross-CVE overlap: existing remediation task [covering-task-key] (from
        [related-CVE-ID] / [related-cve-key]) already bumps [library] to
        [version], which meets or exceeds this CVE's fix threshold
        ([fix-version]).

        Links created:
        - Related: [current-cve-key] ↔ [related-cve-key] (same upstream component)
        - Depend: [current-cve-key] → [covering-task-key] (covering remediation)

        [ProdSec @mention if configured]
        [Comment Footnote]
        ```

        MUST include the Comment Footnote (see SKILL.md).

     Then present the finding and recommendation to the engineer:
     ```
     Existing remediation task [task-key] (from [related-CVE-ID]) already bumps
     [library] to [version], which meets or exceeds this CVE's fix threshold
     ([fix-version]). No new remediation task needed.

     Recommendation: Close this issue — the fix is already covered by [task-key].
     [ProdSec @mention if configured]
     ```
   - **If related CVEs exist but no covering remediation:**
     ```
     Related CVE Jiras found for [component] in the same stream:

     | Related CVE | Issue | Remediation Task | Bump Version | Covers This CVE? |
     |-------------|-------|------------------|--------------|------------------|
     | CVE-YYYY-XXXXX | TC-1234 | TC-1235 | 1.2.3 | No (threshold: 1.3.0) |

     No existing remediation covers this CVE's fix threshold. Proceeding with
     new remediation task creation.
     [ProdSec @mention if configured]
     ```
   - **If no related CVEs found for this component:** proceed silently to Step 4.4.

### 4.4 – Preemptive task reconciliation

When triaging a new CVE Jira for a specific stream, check whether a proactive
remediation task already exists for this CVE and stream (created by a prior
Step 8 Case B run on a different stream's CVE Jira).

1. **Search for preemptive tasks** matching the current CVE:

   ```
   jira.search_jql(
     "project = <project-key> AND issuetype = Task AND labels = 'security-preemptive' AND labels = '<CVE-ID>' ORDER BY created DESC",
     fields: ["summary", "status", "labels", "issuelinks"]
   )
   ```

2. **Filter results** to tasks whose summary contains the current issue's stream
   name (e.g., the stream suffix from the issue summary). A preemptive task
   created for stream `rhtpa-2.1` will have `(rhtpa-2.1)` in its summary.

3. **If a matching preemptive task is found:**

   a. **Link** the new CVE Jira to the preemptive task with "Depend" (standard
      remediation linkage):
      ```
      jira.create_link(
        inwardIssue: <current-cve-jira-key>,
        outwardIssue: <preemptive-task-key>,
        type: "Depend"
      )
      ```
   b. **Remove the `security-preemptive` label** from the task — it is now
      linked to a proper CVE Jira:
      ```
      current_labels = <preemptive-task-labels>
      updated_labels = current_labels.filter(l => l != "security-preemptive")
      jira.edit_issue(<preemptive-task-key>, fields={
        "labels": updated_labels
      })
      ```
   c. **Inform the engineer:**
      ```
      Existing preemptive remediation task [task-key] found for this CVE and
      stream. Created from cross-stream analysis of [originating-CVE-Jira]
      (linked via "Related").

      Actions taken:
      - Linked [current-cve-key] → [task-key] with "Depend"
      - Removed "security-preemptive" label from [task-key]

      The preemptive task is now a standard remediation task for this CVE Jira.
      Skipping new remediation task creation in Step 8.
      ```
   d. **Record the reconciliation** — mark that remediation already exists for
      this stream so Step 8 skips task creation for it.

4. **If no matching preemptive task found:** proceed silently to Step 5.

## Step 5 – Version Lifecycle Check

Verify that the affected product versions are still within their support lifecycle.

1. Fetch the product lifecycle page using the Product pages URL from Security
   Configuration:
   ```
   WebFetch(url: "<product-pages-url>", prompt: "Extract the list of supported
   product versions and their support status (active, maintenance, EOL)")
   ```
2. For each affected version (from the version impact table), check whether it
   appears as actively supported.

**If ALL affected versions are EOL or unsupported**:
- **Recommendation**: Close as Won't Do.
- After confirmation:
  1. Add comment: "All affected versions ([versions]) are EOL per product pages —
     no fix required."
  2. Transition to Closed with resolution "Won't Do".
  3. Assign to current user.

**If SOME affected versions are EOL**: note the EOL versions but continue with
triage for the supported versions. Remove EOL versions from Affects Versions if
they were included.

**If ALL affected versions are supported**: proceed to Step 6.

## Step 6 – Already Fixed Check

Cross-reference resolved sibling Vulnerability issues for the same CVE against the
version impact table.

1. Reuse the JQL results from Step 4 (sibling issues).
2. For siblings with status "Closed" and resolution "Done":
   - Check their Affects Versions.
   - Cross-reference against the version impact table.

**If the current issue's affected versions are all already covered by resolved
siblings**, and the version impact table shows "NO" (not affected) for remaining
versions:
- **Recommendation**: Close as Not a Bug (already fixed by sibling).
- After confirmation:
  1. Add comment: "All affected versions are already covered by resolved sibling
     [sibling-key]. No additional fix required."
  2. Transition to Closed with resolution "Not a Bug".
  3. Assign to current user.
Do **not** set VEX Justification for already-fixed closures — VEX applies only when
the vulnerability does not affect the product.

**If the fix is partial** (some versions covered, others not), narrow the scope to
the unfixed versions and proceed to Step 8.

**If no resolved siblings exist**, proceed to Step 8.

## Step 7 – Concurrent Triage Detection

Before creating remediation tasks (Cases A/B), check whether another engineer is
actively triaging a different CVE that affects the same upstream component. This
prevents duplicate remediation tasks when two triages reach Step 8 simultaneously.

**Prerequisite:** This step requires the Upstream Affected Component custom field
to be configured in Security Configuration (Step 0). If the field is not configured,
skip this step entirely — consistent with Step 4.3's conditional behavior.

1. **Extract the Upstream Affected Component** from the current issue (already
   fetched in Step 1). If the field is empty, skip this step.

2. **Search for in-progress triages** on the same component:

   ```
   jira.search_jql(
     "project = <project-key> AND issuetype = <vulnerability-issue-type-id> AND cf[<upstream-affected-component-field-number>] ~ '<component-value>' AND status IN ('In Progress', 'Code Review') AND key != <current-issue-key>",
     fields: ["summary", "status", "labels", "assignee"]
   )
   ```

3. **If results are returned**, present the concurrent triages to the engineer:

   ```
   ⚠️ Concurrent triage detected on the same upstream component (<component-value>):

   | CVE Issue | Status | Assignee |
   |-----------|--------|----------|
   | <key-1>   | In Progress | <assignee-1> |

   Another engineer is actively triaging a related CVE. Creating remediation
   tasks now may produce duplicates.

   Options:
   1. Wait — pause until the other triage completes, then re-run Step 4.3
      to detect any overlap
   2. Skip — skip remediation task creation for this CVE
   3. Proceed — create tasks anyway with a `concurrent-triage-overlap` label
      so the other engineer's Step 4.3 catches the overlap
   ```

4. **Handle user choice:**
   - **Wait**: stop execution and inform the user to re-run after the concurrent
     triage completes.
   - **Skip**: skip Step 8 entirely (do not create remediation tasks) and add a
     Jira comment explaining why task creation was skipped.
   - **Proceed**: add the `concurrent-triage-overlap` label to the current issue
     and continue to Case A/B/C branching. The label ensures the other triage's
     Step 4.3 cross-CVE overlap detection picks up the overlap.

5. **If no results are returned**, proceed silently to Case A/B/C branching.

## Step 7.5 – Release Jira Orchestration

Before creating remediation tasks (Step 8), find or create the release Jira
structure for each affected stream. This provides a release-scoped container
that links all CVE triages and remediation tasks for a given product version.

**Prerequisite:** This step runs after Step 7 (Concurrent Triage Detection) and
before Case A/B/C branching in Step 8. It applies to all non-preemptive
remediation types (upstream backport, downstream propagation, system package,
dependency bump).

### Fullsend release procedure

The following 7.5.1–7.5.3 searches, confirmations and writes are interactive-only.
In Fullsend mode, use only the validated `jira_metadata.release_jira` entries for
matrix release families and `authorization.release_decisions`. Do not fetch a
release issue, choose a patch bump, prompt or contact Jira.

1. For each affected family, require its trusted release entry. If missing, report
   **manual release decision required**, identify the family and withheld work,
   and leave release-dependent remediation unresolved. Do not claim completion.
2. Honor `{family, skip: true}` by explicitly reporting the skip and continuing
   Step 8 without release links for that family. Otherwise use the decision's
   exact version, or reuse the existing Epic selected by the trusted query order
   (7.5.1). Require exact configured prefix/version summaries, Epic type, Task type
   and child parent identity. Ambiguous identities require manual review.
3. Reuse existing Epic/Task keys with `resolve-reference` before dependent actions;
   reuse never needs a creation permission. If an identity is missing, require
   `mutation_authorized: true`, the decision's exact family/version, and its
   individual `create_epic: true` or `create_task: true`. A permission for one
   does not authorize the other. Missing permission/decision yields the manual
   release decision required report, no guessed version or dependent creation.
4. Append `release-epic` before `release-task`; the Task's `parent` is the matching
   existing Epic key or `{{release-epic-ref.key}}`. Both actions carry family,
   version, ref, project, exact summary, description_adf and labels (optional
   priority/fix_versions). Use unique stable markers and one creation action per
   identity. Always retain planned release creation actions on partial retries,
   even with a recorded marker: the host reuses the typed snapshot and repairs
   its digest before dependent links/comments. Do not add standalone digest
   comments or post-creation resolve-reference actions.
5. For dedup, inspect only the selected release Task's Blocks inward endpoints
   in `remediation`, then their Depend-linked `originating_cves`. Compare the
   originating CVE's `upstream_affected_component` with the current issue's
   configured `upstream_affected_component_field`. Preserve 7.5.3's prerequisite:
   no configured field means skip dedup. Use library-summary fallback only when
   the Depend link or component field on the originating CVE is missing; a
   present nonmatching component never authorizes a summary fallback. Missing
   trusted graph evidence must not be replaced by a Jira query.
6. A match emits no new remediation Task: append Depend with current CVE inward
   and covering Task outward, Related with release Task inward and current CVE
   outward, and field-edit adding the CVE label while retaining all existing
   labels. Record family/version, covering Task and match evidence in the report.
   Nonmatches follow Step 8, including dependency bump plus downstream
   propagation when applicable, then Blocks (remediation inward, release Task
   outward) and Related (release Task inward, current CVE outward).
7. When global authorization is false, serialize none of these mutations. Keep
   exactly one report-only action and report existing release references, dedup
   evidence, explicit skips and all withheld creation/link/label work. Missing
   decisions remain unresolved; never describe withheld operations as completed.

### 7.5.1 – Resolve stream-to-version mapping

For each affected stream, derive the release version from the stream name using
the Version Streams table in Security Configuration:

1. **Parse the stream name** — e.g., `rhtpa-3.0` maps to the `3.0.x` release family.
2. **Search for an existing release Epic** matching the pattern
   `"RHTPA <major>.<minor>.* Release Tasks"`:

   ```
   jira.search_jql(
     "project = <project-key> AND issuetype = Epic AND summary ~ 'RHTPA <major>.<minor>' AND summary ~ 'Release Tasks' ORDER BY created DESC",
     fields: ["summary", "status"],
     maxResults: 5
   )
   ```

3. **If an existing release Epic is found**, extract the version from its summary
   (e.g., `"RHTPA 3.1.1 Release Tasks"` → version `3.1.1`). Use this Epic and
   proceed to Step 7.5.2.

4. **If no release Epic exists**, determine the version to use:
   a. **Default**: next patch bump from the latest released version in that stream's
      Supportability Matrix (e.g., latest is `3.0.2` → default to `3.0.3`).
   b. **Prompt the engineer for confirmation**:

      ```
      No release Epic found for stream <stream>.

      Proposed version: RHTPA <default-version> Release Tasks
      (based on latest released version <latest-version> in supportability matrix)

      Options:
      1. Accept — create Epic with version <default-version>
      2. Specify different version
      3. Skip — do not create release Jira for this stream

      Choose (1/2/3):
      ```

   c. **If the engineer specifies a different version**, use that version.
   d. **If the engineer skips**, proceed to Step 8 without release Jira for this
      stream — remediation tasks are still created but not linked to a release Task.

5. **Create the release Epic** (after engineer confirmation):

   ```
   release_epic = jira.create_issue(
     projectKey: "<project-key>",
     issueTypeName: "Epic",
     summary: "RHTPA <version> Release Tasks",
     description: "Release tracking Epic for RHTPA <version>. Contains CVE triage and remediation tasks for this release.",
     labels: ["ai-generated-jira"]
   )
   ```

   Post a description digest comment per `shared/description-digest-protocol.md`.

### 7.5.2 – Find or create the release Task

Search for an existing release Task under the release Epic:

```
jira.search_jql(
  "project = <project-key> AND issuetype = Task AND parent = <release-epic-key> AND summary ~ 'RHTPA <version> CVE triage' ORDER BY created DESC",
  fields: ["summary", "status", "issuelinks"],
  maxResults: 5
)
```

1. **If a release Task exists**, use it and proceed to Step 7.5.3.

2. **If no release Task exists**, prompt the engineer:

   ```
   No release Task found under <release-epic-key>.

   Proposed: Create "RHTPA <version> CVE triage" as child of <release-epic-key>

   Proceed? (Yes / No)
   ```

3. **Create the release Task** (after confirmation):

   ```
   release_task = jira.create_issue(
     projectKey: "<project-key>",
     issueTypeName: "Task",
     summary: "RHTPA <version> CVE triage",
     description: "CVE triage tracking task for RHTPA <version>. Linked to CVE Vulnerability issues (Related) and blocked by remediation Tasks (Blocks).",
     labels: ["ai-generated-jira"],
     parent: <release-epic-key>
   )
   ```

   Post a description digest comment per `shared/description-digest-protocol.md`.

Store the release Task key for use in Step 8's post-creation linking.

### 7.5.3 – Cross-CVE dedup check

Before creating remediation tasks, check whether an existing remediation Task
already covers the same Upstream Affected Component for the same release version.
This prevents duplicate tasks when multiple CVEs affect the same library.

**Prerequisite:** Requires the Upstream Affected Component custom field to be
configured. If not configured, skip dedup and proceed to Step 8.

1. **Extract the Upstream Affected Component** from the current CVE issue
   (already fetched in Step 1).

2. **Inspect the release Task's issue links.** Fetch the release Task with
   expanded issue links:

   ```
   jira.get_issue(<release-task-key>, fields=["issuelinks"])
   ```

   For each linked issue where `type.name` is `"Blocks"` (remediation Tasks that
   block the release Task), fetch the linked Task with its own issue links:

   ```
   jira.get_issue(<linked-task-key>, fields=["summary", "labels", "issuelinks"])
   ```

3. **Resolve each remediation Task's parent CVE.** For each linked remediation
   Task, traverse its `issuelinks` to find Depend links pointing to CVE
   Vulnerability issues. The standard linkage (see `remediation-templates.md`)
   creates a Depend link from each remediation Task to its originating CVE.

   For each Depend-linked CVE, fetch the Upstream Affected Component:

   ```
   jira.get_issue(<linked-cve-key>, fields=["<upstream-affected-component-field>"])
   ```

4. **Match by Upstream Affected Component.** Compare the Upstream Affected
   Component value on each resolved CVE against the current CVE's Upstream
   Affected Component (extracted in Step 1). If the values match, the existing
   remediation Task already covers the same upstream component.

   **Fallback** (when the Depend link or Upstream Affected Component field is
   missing on the resolved CVE): fall back to summary matching — if the
   remediation Task's summary contains the same library name as the current
   CVE's vulnerable library (from Step 1), treat it as a match.

5. **If a covering remediation Task is found:**

   a. **Skip remediation task creation** for this CVE/stream combination.
   b. **Link the current CVE to the existing remediation Task** (Depend):
      ```
      jira.create_link(
        inwardIssue: <current-cve-key>,
        outwardIssue: <covering-task-key>,
        type: "Depend"
      )
      ```
   c. **Link the current CVE to the release Task** (Related):
      ```
      jira.create_link(
        inwardIssue: <release-task-key>,
        outwardIssue: <current-cve-key>,
        type: "Related"
      )
      ```
   d. **Add the current CVE's label to the existing remediation Task**:
      ```
      current_labels = <covering-task-labels>
      updated_labels = current_labels + ["<current-CVE-ID>"]
      jira.edit_issue(<covering-task-key>, fields={
        "labels": updated_labels
      })
      ```
   e. **Inform the engineer:**
      ```
      Dedup: existing remediation task <covering-task-key> already covers
      <upstream-component> for release <version>. Skipping new task creation.

      Actions taken:
      - Linked <current-cve-key> → <covering-task-key> (Depend)
      - Linked <release-task-key> → <current-cve-key> (Related)
      - Added <current-CVE-ID> label to <covering-task-key>
      ```
   f. **Record the dedup** — mark that remediation already exists for this
      stream so Step 8 skips task creation for it.

6. **If no covering Task is found**, proceed to Step 8 for standard remediation
   task creation. After task creation, link the new tasks to the release Task
   (see `remediation-templates.md` Jira Linkage section).
