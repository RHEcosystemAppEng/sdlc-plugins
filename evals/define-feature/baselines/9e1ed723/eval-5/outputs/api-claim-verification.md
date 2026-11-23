# External API Claim Verification (simulated)

> Simulated for the eval. No WebSearch or WebFetch calls were made. The result below is what checking GitHub's official REST API documentation would show.

## Claim found

- **Section:** Requirements (Step 3d), row 4
- **Requirement text:** "PR reviews cannot be updated after initial submission so always create a new review"
- **Notes text:** "The GitHub API does not support modifying a submitted review"
- **Pattern matched:** "X cannot be updated ... after creation" / "The API does not support Y"
- **External API:** GitHub REST API, Pull Request Reviews

## What I told the user

> "I found a claim about an external API in the Requirements section: **PR reviews cannot be updated after initial submission. The GitHub API does not support modifying a submitted review.** I'll check this against the official GitHub REST API documentation before finishing this section."

## How it was verified (simulated)

1. WebSearch: `GitHub REST API update pull request review`
2. WebFetch: https://docs.github.com/en/rest/pulls/reviews#update-a-review-for-a-pull-request

## Result: INCORRECT

The GitHub REST API does let you update a review after it is submitted:

- **Endpoint:** `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}`
- **Operation:** "Update a review for a pull request"
- **What it does:** Replaces the review's summary text (`body`, required parameter).
- **Documentation:** https://docs.github.com/en/rest/pulls/reviews#update-a-review-for-a-pull-request
- **Related endpoints:** `GET /repos/{owner}/{repo}/pulls/{pull_number}/reviews` lists reviews, so an earlier bot review can be found and its `review_id` reused. `POST /repos/{owner}/{repo}/pulls/{pull_number}/reviews` creates a review.

Limit worth noting: the update endpoint changes the review body only. It does not change the review state (APPROVE / REQUEST_CHANGES / COMMENT) or the inline comments.

## Suggested correction for the user

Original row:

| Requirement | Notes | Is MVP? |
|---|---|---|
| PR reviews cannot be updated after initial submission so always create a new review | The GitHub API does not support modifying a submitted review | Yes |

Suggested row:

| Requirement | Notes | Is MVP? |
|---|---|---|
| On later eval runs for the same PR, update the review posted earlier instead of creating a new one | The GitHub REST API supports updating a submitted review's body via `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` ([docs](https://docs.github.com/en/rest/pulls/reviews#update-a-review-for-a-pull-request)). Only the body can be changed, not the review state. | Yes |

Question to the user:

> "The claim is incorrect: GitHub supports updating a submitted review (endpoint, docs link, and limits above). Should I replace the requirement with the corrected wording above? Or would you rather keep 'always create a new review' as a deliberate design choice and only remove the incorrect API limitation from the Notes?"

**Simulated user response:** The user accepted the suggested correction. The corrected row is used in the preview and the Jira description.
