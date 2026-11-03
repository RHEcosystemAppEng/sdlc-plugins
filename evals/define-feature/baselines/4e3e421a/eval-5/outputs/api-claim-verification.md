# External API Claim Verification (simulated)

> Simulated for this eval. No WebSearch or WebFetch calls were made. The result below reflects the official GitHub REST API documentation as it would be found.

## Step 0 – Project Configuration Validation

- Repository Registry: present (trustify-backend)
- Jira Configuration: Project key `TC`, Cloud ID `2b9e35e3-6bd3-4cec-b838-f4249ee02432`, Feature issue type ID `10142`
- Code Intelligence: present
- Result: PASS. Continuing.

## Claim Detected

- **Section:** Requirements (Step 3d), row 4
- **Requirement text:** "PR reviews cannot be updated after initial submission so always create a new review"
- **Notes text:** "The GitHub API does not support modifying a submitted review"
- **Pattern matched:** "X cannot be updated ... after creation" / "The API does not support Y"
- **External API:** GitHub REST API (Pull request reviews)

User notification:

> "I found a claim about an external API in your Requirements: **'PR reviews cannot be updated after initial submission' / 'The GitHub API does not support modifying a submitted review'**. I will verify this against the official GitHub REST API documentation before finalizing this section."

## Verification

- **Search (simulated WebSearch):** `GitHub REST API update pull request review`
- **Source (simulated WebFetch):** https://docs.github.com/en/rest/pulls/reviews#update-a-review-for-a-pull-request
- **Finding:** The GitHub REST API provides an endpoint to update a review:

  ```
  PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}
  ```

  "Update a review for a pull request" — updates the contents (the `body` field, required) of a specified review summary comment. This applies to submitted reviews.

## Result: INCORRECT

The claim is **incorrect**. The GitHub REST API does support modifying a submitted review's body via `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}`.

## Suggested Corrected Language

Original row:

| Requirement | Notes | Is MVP? |
|---|---|---|
| PR reviews cannot be updated after initial submission so always create a new review | The GitHub API does not support modifying a submitted review | Yes |

Suggested correction (removes the incorrect API limitation; the underlying behavior decision is left to the user, since the original rationale was based on a false premise):

| Requirement | Notes | Is MVP? |
|---|---|---|
| On subsequent eval runs for the same PR, update the existing eval results review rather than always creating a new review | The GitHub REST API supports updating a submitted review's body via `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` ([docs](https://docs.github.com/en/rest/pulls/reviews#update-a-review-for-a-pull-request)) | Yes |

Prompt presented to user:

> "The claim is incorrect: GitHub supports updating a submitted review with `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` (see https://docs.github.com/en/rest/pulls/reviews#update-a-review-for-a-pull-request). I suggest the corrected wording above. Do you confirm this correction, or would you prefer to keep creating a new review each run (with the incorrect API-limitation rationale removed)?"

**Simulated user response:** Confirmed the suggested correction. The corrected row is used in the preview and in the Jira create call.

## Other Sections

- Feature Overview: no external API capability claims detected.
- All other sections: SKIP (no content to scan).
