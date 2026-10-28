# External API Claim Verification

## Detected Claim

In **Section 4 -- Requirements**, the following claim was identified:

> "PR reviews cannot be updated after initial submission so always create a new review"
> Notes: "The GitHub API does not support modifying a submitted review"

This is a claim asserting that the GitHub REST API lacks the capability to update a submitted pull request review.

## Verification Result: INCORRECT

The claim is **incorrect**. The GitHub REST API **does** support updating a submitted pull request review.

### Evidence

The GitHub REST API provides the following endpoint for updating a pull request review:

```
PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}
```

This endpoint allows modifying the body of a previously submitted review. It accepts the `review_id` of an existing review and a new `body` parameter to update the review content.

Documentation reference: [GitHub REST API -- Update a pull request review](https://docs.github.com/en/rest/pulls/reviews#update-a-pull-request-review)

### Suggested Corrected Language

**Original Requirement:**
> PR reviews cannot be updated after initial submission so always create a new review

**Corrected Requirement:**
> Update the existing PR review when re-running evals on the same PR, rather than creating a new review each time

**Original Notes:**
> The GitHub API does not support modifying a submitted review

**Corrected Notes:**
> Use PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id} to update an existing review with the latest eval results

## Conclusion

The requirement and its notes should be revised to reflect the actual GitHub REST API capabilities. The corrected language recommends updating existing reviews instead of always creating new ones, which avoids cluttering the PR timeline with duplicate reviews.
