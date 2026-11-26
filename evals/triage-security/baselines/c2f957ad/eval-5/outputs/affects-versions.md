# Step 3 – Affects Versions Correction: TC-8005

## 3.1 – Version discovery

In a live run, Jira versions come from
`getJiraIssueTypeMetaWithFields(projectIdOrKey: "TC", issueTypeId: "10024")`, filtered by
prefix `RHTPA`. No version IDs are hardcoded. Jira was not called in this eval, so the
version names below must be resolved to IDs at runtime.

## 3.2 – Correction (scoped to stream 2.2.x per `[rhtpa-2.2]` suffix)

The PSIRT-assigned version is **wrong**: `RHTPA 2.0.0` is not in any supported stream.
There is no 2.0.x stream in the Version Streams table or security matrix.

```
Current:  [RHTPA 2.0.0]
Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
```

| Version | Action | Evidence |
|---------|--------|----------|
| RHTPA 2.0.0 | Remove | Not a supported/configured version; no lock file evidence |
| RHTPA 2.2.0 | Add | openssl-libs 3.0.7-25.el9_3 at `v0.4.5` |
| RHTPA 2.2.1 | Add | openssl-libs 3.0.7-27.el9_4 at `v0.4.8` |
| RHTPA 2.2.2 | Add | retag of 2.2.1 (`v0.4.8`), same result |
| RHTPA 2.2.3 | Not added | 3.0.7-28.el9_4 (fixed) |
| RHTPA 2.2.4 | Not added | 3.0.7-28.el9_4 (fixed) |

Excluded by scope: RHTPA 2.1.0 and RHTPA 2.1.1 are also affected (3.0.7-24.el9) but belong
to stream 2.1.x. They go to a sibling/companion issue (Step 4) or to a preemptive task (Step 8 Case A).

Development stream: not included because it was not evaluated (see version-impact.md).

If any proposed version has no matching Jira version, flag it: "RHTPA X.Y.Z is in the
supportability matrix but has no matching Jira version — notify project admin". Then continue.

## Proposed mutation (requires engineer confirmation)

```
jira.edit_issue("TC-8005", fields={
  "versions": [{"id": "<id of RHTPA 2.2.0>"}, {"id": "<id of RHTPA 2.2.1>"}, {"id": "<id of RHTPA 2.2.2>"}]
})
```

## Proposed comment

```
Corrected Affects Versions: [RHTPA 2.0.0] → [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
Based on lock file analysis (rpms.lock.yaml) at pinned commits from security-matrix.md.
Scoped to stream 2.2.x per issue suffix.

---
<Comment Footnote per shared/comment-footnote.md, skill name: triage-security>
```

(No ProdSec Jira account ID is configured, so the @mention is omitted.)
