# External API Claim Verification

## Detected Claim

**Source:** Section 4 — Requirements, row 4

**Claim:** "PR reviews cannot be updated after initial submission" / "The GitHub API does not support modifying a submitted review"

## Verification Result

**Status:** INCORRECT

The GitHub REST API **does** support updating a submitted pull request review. The relevant endpoint is:

```
PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}
```

This endpoint updates the body of an existing pull request review. It accepts a `body` parameter (string, required) containing the updated text of the review.

**Documentation:** https://docs.github.com/en/rest/pulls/reviews#update-a-review-for-a-pull-request

## Evidence

The GitHub REST API `pulls/reviews` resource supports the full lifecycle of PR reviews, including:

- `POST /repos/{owner}/{repo}/pulls/{pull_number}/reviews` — Create a review
- `GET /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` — Get a review
- `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` — Update a review
- `DELETE /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` — Delete a pending review
- `POST /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}/dismissals` — Dismiss a review

The `PUT` endpoint allows modifying the body text of a previously submitted review.

## Suggested Correction

**Original requirement:** "PR reviews cannot be updated after initial submission so always create a new review"

**Corrected requirement:** "Update the existing eval review if one was previously posted, otherwise create a new review"

**Original notes:** "The GitHub API does not support modifying a submitted review"

**Corrected notes:** "Use PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id} to update an existing review"

This correction avoids creating duplicate reviews on the same PR and instead updates the existing one with the latest eval results.
