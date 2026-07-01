# External API Claim Verification

## Detected Claims

The following claims were detected in **Section 4 — Requirements** of the user input:

1. **Claim**: "PR reviews cannot be updated after initial submission so always create a new review"
   - **Source**: Requirement row 4, Requirement column

2. **Claim**: "The GitHub API does not support modifying a submitted review"
   - **Source**: Requirement row 4, Notes column

## Verification Finding

**Status**: INCORRECT

Both claims are factually wrong. The GitHub REST API **does** support updating a submitted pull request review via:

```
PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}
```

This endpoint allows modifying the body of an already-submitted review. Therefore, the assertion that reviews cannot be updated after submission is incorrect, and the requirement to "always create a new review" is based on a false premise.

**Reference**: [GitHub REST API — Update a review for a pull request](https://docs.github.com/en/rest/pulls/reviews#update-a-review-for-a-pull-request)

## Suggested Corrected Language

**Original Requirement**:
> PR reviews cannot be updated after initial submission so always create a new review

**Corrected Requirement**:
> Update the existing PR review when re-running evals on the same PR; create a new review only if no prior eval review exists

**Original Notes**:
> The GitHub API does not support modifying a submitted review

**Corrected Notes**:
> Use `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` to update an existing review, or `POST` to create a new one if none exists
