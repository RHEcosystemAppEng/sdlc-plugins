# External API Claim Verification

## Detected Claim

In the **Requirements** section (Section 4), the following claim was identified:

> "PR reviews cannot be updated after initial submission so always create a new review"
> Notes: "The GitHub API does not support modifying a submitted review"

This matches the verification trigger pattern: "X cannot be updated after creation" / "The API does not support Y".

## Verification Result: INCORRECT

The claim is **incorrect**. The GitHub REST API does support updating a submitted pull request review.

### Evidence

The GitHub REST API provides the following endpoint to update a submitted review:

```
PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}
```

This endpoint allows modifying the body of an already-submitted pull request review. It accepts a JSON payload with a `body` field containing the updated review text.

**Documentation reference:** [GitHub REST API — Update a review for a pull request](https://docs.github.com/en/rest/pulls/reviews#update-a-review-for-a-pull-request)

### Suggested Corrected Language

**Original requirement:** "PR reviews cannot be updated after initial submission so always create a new review"
**Original notes:** "The GitHub API does not support modifying a submitted review"

**Corrected requirement:** "Update existing PR review when re-running evals on the same PR, or create a new review if none exists"
**Corrected notes:** "Use PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id} to update an existing review, or POST to create a new one"

The corrected language reflects that the GitHub REST API supports updating submitted reviews, so the implementation should prefer updating an existing review rather than always creating a new one.
