# TC-8001 — Affects Versions Correction (Step 3)

> PROPOSED correction only. No Jira field has been changed. The change needs
> explicit engineer confirmation.

## 3.1 – Discover available Jira versions

Version IDs are **never hardcoded**. The live run discovers them at runtime:

```
jira.getJiraIssueTypeMetaWithFields(
  projectIdOrKey: "TC",
  issueTypeId: "10024"        # Vulnerability issue type ID from Security Configuration
)
```

The next steps are to take `versions.allowedValues`, filter it by the prefix `RHTPA`, and map each name below to its `id`. No Jira metadata was available in this eval, so the IDs below are placeholders (`<id: RHTPA 2.2.0>` and so on) to be resolved at runtime. If any matrix version has no matching Jira version, flag it with the message "RHTPA X.Y.Z is in the supportability matrix but has no matching Jira version — notify project admin" and continue.

## 3.2 – Compare and correct

**Scope:** the issue suffix is `[rhtpa-2.2]`, so the correction includes only **2.2.x** versions. The affected 2.1.x versions (2.1.0, 2.1.1) belong to a companion or sibling issue (Step 4 and Case A), not to TC-8001.

Stream-scoped evidence from the version impact table:

| Version | quinn-proto | Affected? | Include in TC-8001 Affects Versions? |
|---------|-------------|-----------|--------------------------------------|
| RHTPA 2.2.0 | 0.11.9 | YES | Yes |
| RHTPA 2.2.1 | 0.11.12 | YES | Yes |
| RHTPA 2.2.2 | same as 2.2.1 (retag) | YES | Yes |
| RHTPA 2.2.3 | 0.11.14 | NO | No |
| RHTPA 2.2.4 | 0.11.14 | NO | No |

**PSIRT version is wrong.** `RHTPA 2.0.0` matches no configured stream (only 2.1.x and 2.2.x exist), and no lock-file evidence supports it.

```
Current:  [RHTPA 2.0.0]
Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]

  - RHTPA 2.0.0   (removed: not a supported version and not in the 2.2.x stream)
  + RHTPA 2.2.0   (quinn-proto 0.11.9 @ backend v0.4.5)
  + RHTPA 2.2.1   (quinn-proto 0.11.12 @ backend v0.4.8)
  + RHTPA 2.2.2   (retag of 2.2.1, backend v0.4.8)
```

Development stream: not identified (see version-impact.md §2.2). If the live run finds that the development version belongs to the 2.2.x stream and its HEAD ships quinn-proto < 0.11.14, add that unreleased Jira version too. No dev version is proposed now.

### Proposed mutation (after engineer confirmation)

```
jira.edit_issue("TC-8001", fields={
  "versions": [
    {"id": "<id: RHTPA 2.2.0>"},
    {"id": "<id: RHTPA 2.2.1>"},
    {"id": "<id: RHTPA 2.2.2>"}
  ]
})
```

### Proposed comment (after confirmation)

There is no ProdSec @mention, because no ProdSec Jira account ID is configured.

```
Corrected Affects Versions: [RHTPA 2.0.0] → [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
Based on lock file analysis at pinned commits from security-matrix.md
(quinn-proto 0.11.9 @ v0.4.5, 0.11.12 @ v0.4.8; 2.2.2 is a backend retag of 2.2.1;
2.2.3/2.2.4 ship fixed 0.11.14).
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].

<Comment Footnote per shared/comment-footnote.md, skill name: triage-security>
```
