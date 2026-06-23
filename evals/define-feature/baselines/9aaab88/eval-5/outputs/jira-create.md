# Jira Create Parameters

## API Call: Create Issue

**Endpoint**: `mcp__jira__jira_create_issue`

### Parameters

| Parameter | Value |
|---|---|
| `project_key` | TC |
| `issue_type_id` | 10142 |
| `summary` | Add automated PR review posting for eval results |
| `status` | To Do |
| `assignee` | _(unassigned)_ |

### Description (Jira Wiki Markup)

```
h2. Feature Overview

Add a CI workflow step that posts eval results as a PR review comment on pull requests that modify skill definitions. When a PR changes a SKILL.md file, the CI pipeline should run the corresponding eval suite and post a summary of pass/fail assertions as a PR review. This gives reviewers immediate visibility into whether skill behavior changes break existing eval expectations.

h2. Requirements

||Requirement||Notes||Is MVP?||
|Post eval results as a GitHub PR review when SKILL.md files change|Use the GitHub REST API to create a review with pass/fail summary|Yes|
|Include per-assertion results in the review body|Format as a Markdown checklist|Yes|
|Handle the case where no evals exist for the modified skill|Post an informational comment instead of a review|Yes|
|Update an existing bot review if one already exists; otherwise create a new review|Use PUT /repos/\{owner\}/\{repo\}/pulls/\{pull_number\}/reviews/\{review_id\} to update an existing review, or POST to create a new one|Yes|

{panel:title=API Claim Correction}
The original input claimed "PR reviews cannot be updated after initial submission" and "The GitHub API does not support modifying a submitted review." This is incorrect. The GitHub REST API supports PUT /repos/\{owner\}/\{repo\}/pulls/\{pull_number\}/reviews/\{review_id\} to update an existing review. The requirement has been corrected accordingly.
{panel}
```
