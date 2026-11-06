# TC-8001 — Affects Versions Correction (Step 3)

> **Simulation notice:** This is a proposal only. No `getJiraIssueTypeMetaWithFields`,
> `edit_issue`, or `add_comment` call was made.

## 3.1 Jira version discovery (not executed)

```
jira.getJiraIssueTypeMetaWithFields(projectIdOrKey: "TC", issueTypeId: "10024")
```

Filter `versions.allowedValues` by the prefix `RHTPA`. Version IDs are looked up at
runtime and never hardcoded. Here they appear as `<id:RHTPA 2.2.x>` placeholders.
If any of the proposed versions has no Jira version, flag it with: "RHTPA X.Y.Z is in
the supportability matrix but has no matching Jira version — notify project admin".
Triage continues either way.

## 3.2 Comparison (scoped to stream 2.2.x per the `[rhtpa-2.2]` suffix)

| | Versions |
|---|---|
| **Current (PSIRT)** | RHTPA 2.0.0 |
| **Proposed** | RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 |

```
Current: [RHTPA 2.0.0] → Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
```

Why:

- **RHTPA 2.0.0 is wrong.** There is no 2.0.x stream in the Version Streams table or
  in either supportability matrix. It is a scan-time artifact, so remove it.
- **Add 2.2.0, 2.2.1 and 2.2.2.** Their lock files show quinn-proto 0.11.9, 0.11.12,
  and (for 2.2.2) the 2.2.1 result carried over because 2.2.2 is a backend retag.
  All are below 0.11.14.
- **Leave out 2.2.3 and 2.2.4.** They ship quinn-proto 0.11.14, which is not affected.
- **Leave out 2.1.0 and 2.1.1.** They are affected but belong to stream 2.1.x, which is
  outside this issue's scope. They are handled under Step 8 Case A (cross-stream impact).
- **No development-stream version is added.** The development stream could not be
  identified because no unreleased-version metadata is available.

## Proposed mutation (requires engineer confirmation)

```
jira.edit_issue("TC-8001", fields={
  "versions": [{"id": "<id:RHTPA 2.2.0>"}, {"id": "<id:RHTPA 2.2.1>"}, {"id": "<id:RHTPA 2.2.2>"}]
})
```

## Proposed comment (requires engineer confirmation)

No ProdSec Jira account ID is configured, so the comment has no @mention.

```
Corrected Affects Versions: [RHTPA 2.0.0] → [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
Based on lock file analysis at pinned commits from security-matrix.md
(quinn-proto: 2.2.0=0.11.9, 2.2.1=0.11.12, 2.2.2=retag of 2.2.1; 2.2.3/2.2.4=0.11.14, not affected).
RHTPA 2.0.0 does not correspond to any supported version stream.
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].

---
<Comment Footnote per shared/comment-footnote.md, skill name: triage-security>
```

## Steps 4–7 notes (they lead into remediation)

- **Step 4 (siblings):** the JQL
  `project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8001`
  was not run, so it is unknown whether a 2.1.x companion issue exists. Step 8 Case A
  depends on the answer.
- **Step 4.3 (cross-CVE overlap):** skipped. The Upstream Affected Component, PS
  Component and Stream fields are not configured.
- **Step 4.4 (preemptive reconciliation):** the JQL for `security-preemptive` and
  `CVE-2026-31812` tasks was not run. No preemptive task for 2.2.x is assumed.
- **Step 5 (lifecycle):** the product pages URL was not fetched, so all matrix versions
  are assumed to be supported. This must be verified.
- **Step 6 (already fixed):** no resolved siblings are known. Separately, the 2.2.x fix
  has already **shipped in RHTPA 2.2.3** (see remediation.md).
- **Step 7 (concurrent triage):** skipped. The Upstream Affected Component field is not
  configured.
