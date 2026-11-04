# External API Claim Verification

## Claim Detected

- **Section:** Requirements (Step 3d), row 4
- **Requirement text:** "PR reviews cannot be updated after initial submission so always create a new review"
- **Notes text:** "The GitHub API does not support modifying a submitted review"
- **Pattern matched:** "X cannot be updated / modified after creation" and "The API does not support Y"
- **External API:** GitHub REST API — Pull Request Reviews

### Notification to user

> I detected a claim about an external API in the Requirements section: **"PR reviews cannot be updated after initial submission"** / **"The GitHub API does not support modifying a submitted review."** I will verify it against the official GitHub REST API documentation before finalizing this section.

## Verification (simulated — no WebSearch/WebFetch calls were made in this eval)

- **Simulated WebSearch:** "GitHub REST API update pull request review"
- **Simulated WebFetch:** https://docs.github.com/en/rest/pulls/reviews#update-a-review-for-a-pull-request

### Findings

The GitHub REST API documents an **"Update a review for a pull request"** endpoint:

```
PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}
```

- Request body parameter `body` (string, required) — the new body text of the review.
- This updates the summary body of an existing (including submitted) review.
- Documentation: https://docs.github.com/en/rest/pulls/reviews#update-a-review-for-a-pull-request

Related endpoints in the same documentation page (for context):
- `POST /repos/{owner}/{repo}/pulls/{pull_number}/reviews` — create a review
- `POST /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}/events` — submit a pending review
- `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}/dismissals` — dismiss a review

## Result: INCORRECT

The claim is **incorrect**. The GitHub REST API does support modifying a submitted review's body via `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}`.

## Suggested Corrected Language

Original row:

| Requirement | Notes | Is MVP? |
|---|---|---|
| PR reviews cannot be updated after initial submission so always create a new review | The GitHub API does not support modifying a submitted review | Yes |

Suggested correction (keeps the user's intent of handling re-runs; removes the false limitation; does not invent a new behavior choice):

| Requirement | Notes | Is MVP? |
|---|---|---|
| Handle subsequent eval runs on the same PR by posting results as a PR review (either updating the existing review or creating a new one — to be decided) | The GitHub REST API supports updating a submitted review's body via `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` ([docs](https://docs.github.com/en/rest/pulls/reviews#update-a-review-for-a-pull-request)), so creating a new review on every run is not required by an API limitation | Yes |

### Prompt to user

> The claim is incorrect: GitHub's REST API provides `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` to update the body of a submitted review (see link above). I suggest replacing the requirement with the corrected language shown. Do you confirm this correction, or would you prefer different wording (e.g., explicitly "update the existing review" vs. "always create a new review")?

**Simulated user response:** Confirmed — use the corrected language.
