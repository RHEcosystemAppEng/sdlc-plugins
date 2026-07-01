# External API Claim Verification

## Detected Claim

In the **Requirements** section (Row 4), the following claim was identified:

> "PR reviews cannot be updated after initial submission"
> "The GitHub API does not support modifying a submitted review"

This claim asserts that the GitHub REST API lacks the capability to modify a pull request review after it has been submitted, and therefore the requirement proposes always creating a new review instead of updating an existing one.

## Verification Result: INCORRECT

The claim is **incorrect**. The GitHub REST API does support updating a submitted pull request review.

### Evidence

The GitHub REST API provides the following endpoint for updating a review:

```
PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}
```

This endpoint allows updating the body of a submitted pull request review. It accepts a `body` parameter containing the updated text for the review and returns the updated review object.

Documentation reference: [GitHub REST API - Update a pull request review](https://docs.github.com/en/rest/pulls/reviews#update-a-pull-request-review)

## Suggested Corrected Language

**Original requirement:**

| Requirement | Notes | Is MVP? |
|---|---|---|
| PR reviews cannot be updated after initial submission so always create a new review | The GitHub API does not support modifying a submitted review | Yes |

**Corrected requirement:**

| Requirement | Notes | Is MVP? |
|---|---|---|
| Update existing PR review when re-running evals on the same PR, or create a new review if none exists | Use `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` to update an existing review | Yes |

The corrected language reflects that the GitHub REST API supports updating a submitted review via the PUT endpoint, so the workflow should update an existing review rather than always creating a new one.
