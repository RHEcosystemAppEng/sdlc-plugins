# External API Claim Verification (simulated)

## Claim Detected

- **Section:** Requirements (Step 3d), row 4
- **Requirement text:** "PR reviews cannot be updated after initial submission so always create a new review"
- **Notes text:** "The GitHub API does not support modifying a submitted review"
- **Pattern matched:** "X cannot be updated / modified after creation", "The API does not support Y"
- **External API:** GitHub REST API (Pull Request Reviews)

## User Notification

> I found a claim about an external API in the Requirements section: **"PR reviews cannot be updated after initial submission"** / **"The GitHub API does not support modifying a submitted review"**. I'll check it against the official GitHub REST API documentation before we finalize this section.

## Verification

- **Method (simulated):** WebSearch for "GitHub REST API update pull request review", followed by WebFetch of the official docs page. No real web calls were made in this eval run.
- **Source:** GitHub REST API docs, "REST API endpoints for pull request reviews": https://docs.github.com/en/rest/pulls/reviews#update-a-review-for-a-pull-request
- **Finding:** The capability exists. The API provides:

  ```
  PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}
  ```

  "Update a review for a pull request" changes the body text of an existing review, including one that has already been submitted. The required body parameter is `body` (string).

## Result: CLAIM INCORRECT

The GitHub REST API supports updating a submitted pull request review's body via `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}`. The statement that submitted reviews cannot be modified is wrong.

## Suggested Corrected Language

The false rationale is removed. The user's choice to create a new review on each run is kept, and the update option is noted:

| Requirement | Notes | Is MVP? |
|---|---|---|
| Create a new PR review for each eval run rather than editing a previous review | The GitHub REST API does support updating a submitted review's body (`PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}`), so creating a new review is a design choice, not an API limitation. Updating the existing review in place is a possible alternative. | Yes |

Prompt to the user:

> The claim is incorrect. GitHub documents `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` ("Update a review for a pull request", https://docs.github.com/en/rest/pulls/reviews#update-a-review-for-a-pull-request), which updates the body of a submitted review. I suggest rewording the requirement as shown above. Would you like to use this corrected wording, change the requirement to update the existing review in place, or keep the original?

**Simulated user response:** Confirmed the suggested corrected wording. The preview uses it.
