# Step 4.3 -- Cross-CVE Overlap Analysis: TC-8010

## Prerequisites

All three required custom fields are configured and populated on TC-8010:

- **Upstream Affected Component** (customfield_10632): `axios`
- **PS Component** (customfield_10669): `pscomponent:org/rhtpa-ui`
- **Stream** (customfield_10832): `rhtpa-2.2`

Step 4.3 proceeds (prerequisites met).

## JQL Search for Related CVE Jiras

Search query (proposed):
```
project = TC
  AND issuetype = 10024
  AND cf[10632] ~ 'axios'
  AND key != TC-8010
```

Fields requested: `summary, status, labels, issuelinks, customfield_10632, customfield_10669, customfield_10832`

### Search Results

One related CVE Jira returned:

| Field | Value |
|-------|-------|
| Key | TC-8008 |
| Summary | CVE-2026-42035 axios - Prototype Pollution via header parsing [rhtpa-2.2] |
| Status | In Progress |
| Labels | CVE-2026-42035, pscomponent:org/rhtpa-ui |
| customfield_10632 | axios |
| customfield_10669 | pscomponent:org/rhtpa-ui |
| customfield_10832 | rhtpa-2.2 |

## Filtering

TC-8008 shares:
- **Same PS Component** (`pscomponent:org/rhtpa-ui`) -- MATCH
- **Same Stream** (`rhtpa-2.2`) -- MATCH

TC-8008 is a valid cross-CVE overlap candidate.

## Issue Link Traversal

TC-8008 has a linked remediation Task via `Depend` link type:

| Link Type | Linked Issue | Summary | Status |
|-----------|-------------|---------|--------|
| Depend | TC-8009 | Bump axios to 1.9.0 in rhtpa-ui [rhtpa-2.2] | In Progress |

TC-8009 description excerpt: "Bump axios from 1.7.4 to 1.9.0 to resolve CVE-2026-42035. The fix requires axios >= 1.8.0."

## Remediation Coverage Comparison

| Factor | Value |
|--------|-------|
| Current CVE (TC-8010) fix threshold | axios >= **1.8.2** |
| Existing remediation (TC-8009) bump target | axios **1.9.0** |
| Comparison | 1.9.0 >= 1.8.2 |
| **Covers this CVE?** | **YES** |

The existing remediation task TC-8009 bumps axios to 1.9.0, which **meets or exceeds** the current CVE's fix threshold of 1.8.2. The bump to 1.9.0 resolves both CVE-2026-42035 (fix threshold >= 1.8.0) and CVE-2026-44492 (fix threshold >= 1.8.2).

## Proposed Jira Actions

The following traceability links and comment would be created to record the cross-CVE overlap:

### a. Related link (current CVE to related CVE)

Check TC-8010's existing issuelinks for a Related link to TC-8008. No existing links found.

**Proposed action**: Create Related link
```
jira.create_link(
  inwardIssue: TC-8010,
  outwardIssue: TC-8008,
  type: "Related"
)
```

### b. Depend link (covering remediation task to current CVE)

Check TC-8010's existing issuelinks for a Depend link to TC-8009. No existing links found.

**Proposed action**: Create Depend link
```
jira.create_link(
  inwardIssue: TC-8010,
  outwardIssue: TC-8009,
  type: "Depend"
)
```

### c. Overlap comment on TC-8010

**Proposed action**: Post comment on TC-8010
```
Cross-CVE overlap: existing remediation task TC-8009 (from CVE-2026-42035 /
TC-8008) already bumps axios to 1.9.0, which meets or exceeds this CVE's fix
threshold (1.8.2).

Links created:
- Related: TC-8010 <-> TC-8008 (same upstream component)
- Depend: TC-8010 -> TC-8009 (covering remediation)

[Comment Footnote]
```

## Conclusion

Existing remediation task **TC-8009** (from CVE-2026-42035 / TC-8008) already covers this CVE's fix threshold. **No new remediation task is needed** for TC-8010. The recommended triage outcome is to close this issue as covered by the existing remediation.
