# External API Claim Verification (simulated)

## Claim detected

- **Section:** Requirements (Step 3d), row 4
- **Requirement text:** "PR reviews cannot be updated after initial submission so always create a new review"
- **Notes text:** "The GitHub API does not support modifying a submitted review"
- **Pattern matched:** "X cannot be updated / modified after creation" and "The API does not support Y"
- **External API:** GitHub REST API (Pull Request Reviews)

## User notification

> I detected a claim about an external API capability in the Requirements section:
> **"PR reviews cannot be updated after initial submission"** / **"The GitHub API does not support modifying a submitted review"**.
> I'll verify this against the official GitHub REST API documentation before finalizing the section.

## Verification (simulated — no WebSearch/WebFetch calls were made)

- **Simulated WebSearch query:** `GitHub REST API update pull request review`
- **Simulated WebFetch source:** https://docs.github.com/en/rest/pulls/reviews#update-a-review-for-a-pull-request
- **Finding:** The GitHub REST API provides an "Update a review for a pull request" endpoint:

  ```
  PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}
  ```

  It accepts a `body` parameter (required) and replaces the summary text of the specified review. This allows the body of an existing, submitted review to be modified.

## Result: INCORRECT

The claim is incorrect. The GitHub API does support modifying the body of a submitted pull request review via `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}`.

## Evidence presented to user

- **Endpoint:** `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}`
- **Capability:** Update the body text of an existing pull request review
- **Documentation:** https://docs.github.com/en/rest/pulls/reviews#update-a-review-for-a-pull-request

## Suggested corrected language

| Requirement | Notes | Is MVP? |
|---|---|---|
| When re-running evals on a PR, update the existing eval-results review rather than always creating a new one | The GitHub REST API supports updating a submitted review's body via `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` | Yes |

The corrected wording preserves the user's intent (define how repeated eval runs post their results) while removing the factually incorrect API limitation. The user's original decision about whether to update vs. create new reviews should be confirmed by the user.

## Confirmation prompt to user

> The claim appears to be incorrect. GitHub's REST API documents `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` ("Update a review for a pull request"), which modifies the body of a submitted review.
> Suggested replacement for requirement row 4:
> **Requirement:** "When re-running evals on a PR, update the existing eval-results review rather than always creating a new one"
> **Notes:** "The GitHub REST API supports updating a submitted review's body via `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}`"
> Do you want to apply this correction, or keep the original wording?

**Simulated user response:** Apply the correction. (The preview in `preview.md` uses the corrected language.)
