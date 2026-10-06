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

This endpoint allows modifying the body of an already-submitted review. It is documented in the official GitHub REST API documentation:

- **Endpoint:** `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}`
- **Method:** PUT
- **Purpose:** Update a pull request review that has already been submitted
- **Documentation:** https://docs.github.com/en/rest/pulls/reviews#update-a-review-for-a-pull-request

## Suggested Correction

The requirement "PR reviews cannot be updated after initial submission so always create a new review" is based on an incorrect premise. The GitHub API does support modifying a submitted review via the PUT endpoint above.

**Corrected requirement language:**

> Update the existing PR review when re-running evals on the same pull request, rather than creating a new review each time. Use `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` to update a previously submitted review with the latest eval results.

The user should confirm whether the intent is to update existing reviews (now that the capability is known to exist) or to still create new reviews for a different reason (e.g., preserving history).
