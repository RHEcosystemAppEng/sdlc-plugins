# External API Claim Verification

## Detected Claim

**Section:** Requirements (Section 4)

**Claim:** "PR reviews cannot be updated after initial submission" / "The GitHub API does not support modifying a submitted review"

**Requirement row:** "PR reviews cannot be updated after initial submission so always create a new review"

## Verification Result

**Status:** INCORRECT

The GitHub REST API **does** support updating a submitted pull request review. The endpoint is:

```
PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}
```

This endpoint allows modifying the body of a previously submitted review. Documentation reference: [GitHub REST API - Update a review for a pull request](https://docs.github.com/en/rest/pulls/reviews#update-a-review-for-a-pull-request)

## Evidence

- **Method:** `PUT`
- **Endpoint:** `/repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}`
- **Capability:** Updates the body of a submitted review on a pull request
- **Parameters:** `body` (required) - The body text of the pull request review

## Suggested Correction

The original requirement assumes a limitation that does not exist. The corrected requirement should acknowledge that reviews can be updated and leverage this capability to avoid creating duplicate reviews.

**Original requirement:**
> PR reviews cannot be updated after initial submission so always create a new review

**Corrected requirement:**
> Update the existing PR review when re-running evals on the same PR

**Original notes:**
> The GitHub API does not support modifying a submitted review

**Corrected notes:**
> Use PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id} to update the review body instead of creating duplicate reviews
