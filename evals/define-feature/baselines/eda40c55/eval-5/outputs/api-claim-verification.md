# External API Claim Verification

## Detected Claim

In the **Requirements** section (Section 4), the following claims were detected:

1. "PR reviews cannot be updated after initial submission so always create a new review"
2. "The GitHub API does not support modifying a submitted review"

These statements assert that the GitHub REST API lacks the capability to update a PR review once it has been submitted.

## Verification Result: INCORRECT

The claim is **incorrect**. The GitHub REST API does support updating a submitted pull request review.

### Evidence

The GitHub REST API provides the following endpoint for updating a review:

```
PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}
```

This endpoint allows updating the body of a submitted review. It accepts the `review_id` of an existing review and a new `body` parameter, enabling modification of a previously submitted review.

**Documentation reference:** GitHub REST API — Pull Request Reviews — [Update a pull request review](https://docs.github.com/en/rest/pulls/reviews#update-a-pull-request-review)

## Suggested Corrected Language

Original requirement:
> "PR reviews cannot be updated after initial submission so always create a new review"

Original notes:
> "The GitHub API does not support modifying a submitted review"

Corrected requirement:
> "Update existing PR review when re-running evals on the same PR, or create a new review if none exists"

Corrected notes:
> "PR reviews can be updated using the GitHub REST API (PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}); consider updating existing reviews rather than always creating new ones"
