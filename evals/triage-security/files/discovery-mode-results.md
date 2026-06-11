<!-- SYNTHETIC TEST DATA — mock JQL search results for discovery mode eval testing. Keys, CVE IDs, summaries, and dates are fictional. JQL query structure mirrors SKILL.md §Discovery Mode (Steps 1-2); update both when query patterns change. -->

# Mock JQL Search Results for Discovery Mode

## Query 1: Untriaged Issues

**JQL**: `project = TC AND issuetype = 10024 AND labels NOT IN (ai-cve-triaged) ORDER BY status ASC, created DESC`

**Results** (4 issues):

| Key | Summary | Status | Labels | Created |
|-----|---------|--------|--------|---------|
| TC-9001 | CVE-2026-40112 h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2] | New | CVE-2026-40112, pscomponent:org/rhtpa-server | 2026-06-08T14:30:00.000+0000 |
| TC-9002 | CVE-2026-40297 serde_json - Stack overflow on deeply nested input [rhtpa-2.1] | New | CVE-2026-40297, pscomponent:org/rhtpa-server | 2026-06-07T09:15:00.000+0000 |
| TC-9003 | CVE-2026-40455 tokio - Race condition in task cancellation [rhtpa-2.2] | In Progress | CVE-2026-40455, pscomponent:org/rhtpa-server | 2026-06-05T11:00:00.000+0000 |
| TC-9004 | CVE-2026-40518 ring - Timing side-channel in RSA verification [rhtpa-2.2] | New | CVE-2026-40518, pscomponent:org/rhtpa-server | 2026-06-04T16:45:00.000+0000 |

## Query 2: Triaged but still New

**JQL**: `project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status = New ORDER BY created DESC`

**Results** (1 issue):

| Key | Summary | Status | Labels | Created |
|-----|---------|--------|--------|---------|
| TC-9010 | CVE-2026-39874 quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2] | New | CVE-2026-39874, pscomponent:org/rhtpa-server, ai-cve-triaged | 2026-05-28T10:20:00.000+0000 |
