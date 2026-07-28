# External API Claim Verification

## Detected Claim

The following claims were detected in the **Requirements** section (Section 4):

1. **Claim:** "PR reviews cannot be updated after initial submission so always create a new review"
2. **Claim:** "The GitHub API does not support modifying a submitted review"

These claims assert that the GitHub REST API lacks the capability to update or modify a pull request review after it has been submitted.

## Verification Result

**Status: INCORRECT**

The GitHub REST API **does** support updating a submitted pull request review. The relevant endpoint is:

```
PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}
```

This endpoint allows updating the body of a previously submitted pull request review. The capability is documented in the official GitHub REST API documentation for pull request reviews.

## Evidence

- **Endpoint:** `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}`
- **Method:** PUT
- **Purpose:** Update the body text of a pull request review that has already been submitted
- **Documentation:** GitHub REST API reference for Pull Request Reviews

## Suggested Corrected Language

**Original requirement:**
> PR reviews cannot be updated after initial submission so always create a new review

**Corrected requirement:**
> Update the existing PR review when re-running evals on the same PR, rather than creating duplicate reviews

**Original notes:**
> The GitHub API does not support modifying a submitted review

**Corrected notes:**
> Use `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` to update an existing review in place
