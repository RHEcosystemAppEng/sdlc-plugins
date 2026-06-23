# Jira create_issue Call Parameters

## API Call: `mcp__jira__create_issue`

- **Cloud ID**: `2b9e35e3-6bd3-4cec-b838-f4249ee02432`
- **Project key**: `TC`
- **Summary**: `Add SBOM dependency graph visualization`
- **Issue type ID**: `10142`
- **Labels**: `["ai-generated-jira"]`
- **Assignee**: self (current user / `-1`)

## Description

The `description` field contains the full Feature description in Atlassian Document Format (ADF), composed from all 9 template sections with the following headings:

1. **Feature Overview** — Interactive dependency graph visualization for the SBOM detail page with zoomable, searchable graph, vulnerability highlighting, and severity filtering.
2. **Background and Strategic Fit** — Competitive differentiator aligning with product roadmap and Q3 OKR for reducing mean-time-to-triage.
3. **Goals** — Enable security teams to trace transitive vulnerability paths in under 30 seconds; provide visual dependency overview; support severity-based filtering.
4. **Requirements** — 7 requirements (5 MVP, 2 non-MVP) covering interactive graph, vulnerability color coding, filtering, search, node details, export, and subtree collapsing.
5. **Non-Functional Requirements** — Performance (2,000 packages < 3s render), accessibility, memory limits (200MB), cross-browser support.
6. **Use Cases (User Experience & Workflow)** — UC-1: Investigate transitive vulnerability exposure (security analyst); UC-2: Assess dependency tree breadth (engineering lead).
7. **Customer Considerations** — Performance tuning for large SBOMs, air-gapped environment support, color vision deficiency accommodations.
8. **Customer Information/Supportability** — Grafana dashboard metrics, memory guards, feedback channel.
9. **Documentation Considerations** — New content for graph view, updates to SBOM detail page docs, release notes highlight.

## Raw Parameters

```json
{
  "cloud_id": "2b9e35e3-6bd3-4cec-b838-f4249ee02432",
  "project_key": "TC",
  "summary": "Add SBOM dependency graph visualization",
  "issue_type_id": "10142",
  "labels": ["ai-generated-jira"],
  "assignee": "-1",
  "description": "<ADF document containing all 9 sections as formatted above in preview.md>"
}
```
