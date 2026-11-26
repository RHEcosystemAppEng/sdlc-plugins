# External API Claim Verification (Simulated)

## Claim Detected

- **Section:** Requirements (Step 3d), row 4
- **Claim text (Requirement):** "PR reviews cannot be updated after initial submission so always create a new review"
- **Claim text (Notes):** "The GitHub API does not support modifying a submitted review"
- **Pattern matched:** "X cannot be updated / modified after creation" and "The API does not support Y"
- **External API:** GitHub REST API — Pull request reviews

## User Notification

> I detected a claim about an external API capability in the Requirements section:
> **"PR reviews cannot be updated after initial submission"** / **"The GitHub API does not support modifying a submitted review"**.
> I will verify this against the official GitHub REST API documentation before finalizing the section.

## Verification (simulated — no WebSearch/WebFetch calls were made per eval instructions)

- **Simulated WebSearch query:** `GitHub REST API update pull request review`
- **Simulated WebFetch source:** https://docs.github.com/en/rest/pulls/reviews#update-a-review-for-a-pull-request
- **Finding:** The GitHub REST API provides an endpoint to update a pull request review:

  ```
  PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}
  ```

  "Update a review for a pull request" — updates the body text of a review. Request body parameter: `body` (string, required) — the body text of the pull request review.

## Result: CLAIM INCORRECT

The GitHub REST API **does** support modifying a submitted review's body via
`PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}`. The requirement's
rationale ("always create a new review because reviews cannot be updated") is based on a
false premise.

## Suggested Corrected Language

| Requirement | Notes | Is MVP? |
|---|---|---|
| On subsequent CI runs, update the existing eval-results PR review instead of creating a new one | Use `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` to update the body of the previously posted review ([GitHub docs](https://docs.github.com/en/rest/pulls/reviews#update-a-review-for-a-pull-request)) | Yes |

Note: the original requirement's intent was to decide behavior on re-runs. The correction
preserves the user's MVP flag and only replaces the incorrect premise; whether to update
the existing review versus create a new one is a user decision.

## User Confirmation Prompt

> The claim is incorrect: GitHub supports updating a submitted review via
> `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}`
> (https://docs.github.com/en/rest/pulls/reviews#update-a-review-for-a-pull-request).
> Would you like to replace the requirement with the corrected language above, keep the
> original wording, or revise it differently?

**Simulated user response:** Accept the corrected language. (The preview reflects the correction.)
