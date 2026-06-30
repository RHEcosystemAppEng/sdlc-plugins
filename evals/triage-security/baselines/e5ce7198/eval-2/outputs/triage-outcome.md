# Triage Outcome — TC-8002

## Decision: Case C — No Supported Versions Affected (Close as Not a Bug)

### Rationale

Version impact analysis confirms that **no supported version** ships a vulnerable
version of serde_json. The CVE (CVE-2026-28940) affects serde_json versions before
1.0.135, but every version across all streams already ships serde_json >= 1.0.135:

- **Stream 2.2.x** (scoped stream for this issue): versions 2.2.0 through 2.2.4
  ship serde_json 1.0.138 or 1.0.139 — all above the fix threshold.
- **Stream 2.1.x** (cross-stream check): versions 2.1.0 and 2.1.1 ship
  serde_json 1.0.137 — also above the fix threshold.

The PSIRT-assigned Affects Versions (RHTPA 2.2.0) is incorrect — version 2.2.0
ships serde_json 1.0.138, which is not vulnerable.

### Proposed Jira Actions

The following actions are **proposed** for engineer confirmation. No mutations
have been executed.

#### 1. Affects Versions Correction (Step 3)

- **Current**: RHTPA 2.2.0
- **Proposed**: Remove all Affects Versions (no versions are affected)
- **Rationale**: Lock file analysis at pinned commit v0.4.5 shows serde_json
  1.0.138, which is above the fix threshold of 1.0.135.

Proposed Jira call:
```
jira.edit_issue("TC-8002", fields={
  "versions": []
})
```

Proposed comment:
```
Corrected Affects Versions: [RHTPA 2.2.0] -> [] (none affected).
Based on lock file analysis at pinned commits from security-matrix.md.
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].

Lock file evidence:
- RHTPA 2.2.0 (v0.4.5): serde_json 1.0.138 (>= 1.0.135, not affected)
```

#### 2. Close as Not a Bug (Step 7, Case C)

Proposed comment:
```
No supported versions ship a vulnerable version of serde_json.

Version impact analysis:

| Stream | Version | Tag | serde_json | Affected? |
|--------|---------|-----|------------|-----------|
| 2.1.x  | 2.1.0   | v0.3.8  | 1.0.137 | NO |
| 2.1.x  | 2.1.1   | v0.3.12 | 1.0.137 | NO |
| 2.2.x  | 2.2.0   | v0.4.5  | 1.0.138 | NO |
| 2.2.x  | 2.2.1   | v0.4.8  | 1.0.138 | NO |
| 2.2.x  | 2.2.2   | v0.4.9  | —       | NO (retag of 2.2.1) |
| 2.2.x  | 2.2.3   | v0.4.11 | 1.0.139 | NO |
| 2.2.x  | 2.2.4   | v0.4.12 | 1.0.139 | NO |

All supported versions ship serde_json >= 1.0.135, which is outside
the affected range (< 1.0.135).
```

Proposed transition:
```
jira.transition_issue("TC-8002", status="Closed", resolution="Not a Bug")
```

#### 3. Set VEX Justification

The VEX Justification custom field (customfield_12345) is configured.

- **Proposed value**: Component not Present
- **Rationale**: The vulnerable version of serde_json (< 1.0.135) is not
  present in any supported version. All versions ship a patched version.

Note: "Component not Present" is used here because the *vulnerable version*
of the component is not present — the lock file analysis confirms that no
shipped version includes serde_json < 1.0.135.

Proposed Jira call:
```
jira.edit_issue("TC-8002", fields={
  "customfield_12345": "Component not Present"
})
```

#### 4. Assign to Current User

```
jira.edit_issue("TC-8002", fields={
  "assignee": {"accountId": "<current-user-account-id>"}
})
```

#### 5. Add ai-cve-triaged Label

```
jira.edit_issue("TC-8002", fields={
  "labels": ["CVE-2026-28940", "pscomponent:org/rhtpa-server", "ai-cve-triaged"]
})
```

#### 6. Post-Triage Summary Comment

A summary comment would be posted to TC-8002 documenting:
1. The version impact table (all versions NOT affected)
2. The Affects Versions correction (RHTPA 2.2.0 removed — not affected)
3. The triage outcome (closed as Not a Bug — no vulnerable serde_json version shipped)
4. VEX Justification: Component not Present
5. @mention of the issue reporter (account ID from Jira issue data)

The comment would include the Comment Footnote per `shared/comment-footnote.md`
with skill name `triage-security`.

### Steps Skipped or Not Applicable

| Step | Name | Status | Reason |
|------|------|--------|--------|
| 1.5 | External CVE Data Enrichment | Skipped | Eval mode — no external API calls |
| 1.7 | Embargo Check | Skipped | CVSS 5.3 (Medium) below threshold of 7.0 |
| 4 | Duplicate/Sibling Check | Not executed | Eval mode — no Jira search available |
| 4.3 | Cross-CVE Overlap Detection | Not executed | Eval mode — no Jira search available |
| 5 | Version Lifecycle Check | Not executed | Eval mode — no WebFetch available |
| 6 | Already Fixed Check | Not executed | Eval mode — no sibling search available |
| 7 (Case A/B) | Remediation Task Creation | Not applicable | No versions are affected |

### No Remediation Tasks Needed

Since no supported versions ship a vulnerable version of serde_json, no
remediation tasks are required. The appropriate action is to close the
Vulnerability issue as "Not a Bug" with VEX justification.
