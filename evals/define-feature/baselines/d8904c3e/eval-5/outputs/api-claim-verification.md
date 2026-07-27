# External API Claim Verification

## Claim Detected

**Source section:** Requirements (Section 4), row 4

**Claim:** "PR reviews cannot be updated after initial submission" / "The GitHub API does not support modifying a submitted review"

## Verification Result: INCORRECT

The claim is **incorrect**. The GitHub REST API does support updating a submitted pull request review.

### Evidence

The GitHub REST API provides the following endpoint for updating a review:

```
PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}
```

This endpoint allows updating the body of a submitted review. It is documented in the official GitHub REST API reference under Pull Request Reviews.

**Documentation link:** https://docs.github.com/en/rest/pulls/reviews#update-a-review-for-a-pull-request

### Impact on Feature Description

The original requirement stated:

> "PR reviews cannot be updated after initial submission so always create a new review"
> Notes: "The GitHub API does not support modifying a submitted review"

Since the API does support updating reviews, the requirement and its notes should be corrected. The corrected language should reflect that an existing review can be updated via `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}`, rather than always creating a new review.

### Suggested Correction

**Requirement:** "Update the existing PR review when re-running evals on the same PR, rather than creating a new review"

**Notes:** "Use PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id} to update an existing review"
