# Jira Create Issue Call

## Function Call

```
createJiraIssue(
  cloudId="2b9e35e3-6bd3-4cec-b838-f4249ee02432",
  projectKey="TC",
  issueTypeId="10142",
  summary="Add SBOM dependency graph visualization",
  description="## Feature Overview\n\nAdd an interactive dependency graph visualization to the SBOM detail page.\nUsers should be able to explore package dependencies as a zoomable,\nsearchable graph where nodes represent packages and edges represent\ndependency relationships. The graph should highlight packages with known\nvulnerabilities and allow filtering by severity level. This reduces the\ntime security teams spend manually tracing transitive dependency chains\nfrom hours to seconds.\n\n## Background and Strategic Fit\n\nDependency graph visualization is a key differentiator for SBOM management\nplatforms. Competitors like Snyk and Sonatype offer similar capabilities.\nOur platform already ingests and stores full dependency trees during SBOM\nprocessing, but currently only displays them as flat lists on the package\ndetail page. Surfacing this data as an interactive graph aligns with the\nproduct roadmap goal of \"making vulnerability impact assessment intuitive\"\nand directly supports the Q3 OKR for reducing mean-time-to-triage.\n\n## Goals\n\n- **Who benefits**: Security analysts and engineering leads reviewing\n  transitive dependency exposure\n- **Current state**: Dependencies are shown as a flat, paginated list on\n  the SBOM detail page. Users must manually click through packages to\n  trace transitive chains. There is no visual representation of the\n  dependency tree structure.\n- **Target state**: An interactive graph view on the SBOM detail page\n  renders the full dependency tree with visual indicators for vulnerable\n  packages. Users can zoom, pan, search, and filter the graph.\n- **Goal statements**:\n  - Enable security teams to trace transitive vulnerability paths in\n    under 30 seconds\n  - Provide a visual overview of dependency depth and breadth at a glance\n  - Support filtering by vulnerability severity to prioritize remediation\n\n## Requirements\n\n| Requirement | Notes | Is MVP? |\n|---|---|---|\n| Display SBOM dependencies as an interactive directed graph | Use a force-directed layout with zoom and pan controls | Yes |\n| Highlight packages with known vulnerabilities using color coding | Red for critical/high, orange for medium, grey for low/none | Yes |\n| Support filtering graph nodes by vulnerability severity | Filter controls in a sidebar panel | Yes |\n| Provide a search box to locate specific packages in the graph | Search highlights matching nodes and centers the viewport | Yes |\n| Show package details on node click | Display name, version, license, and vulnerability count in a popover | Yes |\n| Export graph as SVG or PNG | Download button in the graph toolbar | No |\n| Support collapsing/expanding subtrees | Click to collapse a node's children for large graphs | No |\n\n## Non-Functional Requirements\n\n- Graph rendering must handle SBOMs with up to 2,000 packages without\n  visible lag (initial render < 3 seconds, interaction response < 100ms)\n- The graph component must be accessible -- keyboard navigation between\n  nodes and screen reader announcements for node focus changes\n- Memory usage must not exceed 200MB for the largest expected graphs\n- The feature must work in the latest versions of Chrome, Firefox, and\n  Safari\n\n## Use Cases (User Experience & Workflow)\n\n### UC-1: Investigate transitive vulnerability exposure\n\n**Persona**: Security analyst\n**Pre-conditions**: SBOM has been ingested with vulnerability data linked\nto packages\n**Steps**:\n1. Analyst navigates to SBOM detail page and clicks \"Graph View\" tab\n2. Graph renders showing all packages as nodes with vulnerability coloring\n3. Analyst filters to show only critical/high severity packages\n4. Analyst clicks a vulnerable package node to see details\n5. Analyst traces the path from the vulnerable package back to the root\n   to understand the transitive dependency chain\n\n**Expected outcome**: Analyst identifies which direct dependencies bring\nin the vulnerable transitive package and can recommend a remediation path\n\n### UC-2: Assess dependency tree breadth\n\n**Persona**: Engineering lead\n**Pre-conditions**: SBOM ingested for a new service before production\ndeployment\n**Steps**:\n1. Lead opens the dependency graph for the service's SBOM\n2. Lead visually assesses the overall structure -- depth, breadth, and\n   clustering\n3. Lead searches for a specific package to check if it is present\n4. Lead exports the graph as PNG for inclusion in a review document\n\n**Expected outcome**: Lead has a clear picture of dependency complexity\nand can make informed decisions about dependency management\n\n## Customer Considerations\n\n- Large SBOMs (1,000+ packages) may require performance tuning -- consider\n  progressive rendering or level-of-detail approaches\n- Organizations using air-gapped environments need the graph library\n  bundled (no CDN dependencies)\n- Users with color vision deficiency need non-color indicators (shapes or\n  patterns) in addition to the color coding\n\n## Customer Information/Supportability\n\n- Add graph rendering performance metrics to the existing frontend\n  Grafana dashboard (render time, node count, interaction latency)\n- Monitor for browser memory issues on large SBOMs -- add a client-side\n  memory guard that shows a warning if the graph exceeds the threshold\n- Customer feedback channel: existing \"Feature Requests\" board in the\n  support portal\n\n## Documentation Considerations\n\n- **Doc Impact**: New Content -- document the graph view feature, controls,\n  and keyboard shortcuts\n- **Updates to existing content**: Update the SBOM detail page\n  documentation to reference the new Graph View tab\n- **Release Notes**: Include as a highlight feature in the next release\n  notes\n- **User purpose**: Security analysts need to understand how to read and\n  navigate the dependency graph effectively\n- **Reference material**: Link to the graph library documentation for\n  advanced customization options",
  contentFormat="markdown",
  additional_fields={
    "labels": ["ai-generated-jira"],
    "assignee": { "accountId": "<user-account-id>" },
    "priority": { "name": "Major" },
    "fixVersions": [{ "name": "1.5.0" }]
  }
)
```

## Parameter Table

| Parameter | Value |
|---|---|
| cloudId | `2b9e35e3-6bd3-4cec-b838-f4249ee02432` |
| projectKey | `TC` |
| issueTypeId | `10142` |
| summary | `Add SBOM dependency graph visualization` |
| description | _(composed description with all 9 sections -- see above)_ |
| contentFormat | `markdown` |
| additional_fields.labels | `["ai-generated-jira"]` |
| additional_fields.assignee | `{ "accountId": "<user-account-id>" }` |
| additional_fields.priority | `{ "name": "Major" }` |
| additional_fields.fixVersions | `[{ "name": "1.5.0" }]` |
