# External API Claim Verification

## Detected Claim

In the **Requirements** section (Section 4), the following claim about an external API was detected:

> "PR reviews cannot be updated after initial submission so always create a new review"
> "The GitHub API does not support modifying a submitted review"

This claim asserts that the GitHub REST API lacks the capability to update or modify a pull request review after it has been submitted.

## Verification Result: INCORRECT

The claim is **incorrect**. The GitHub REST API does support updating a submitted pull request review.

### Evidence

The GitHub REST API provides the following endpoint for updating a pull request review:

```
PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}
```

This endpoint allows modifying the body of a submitted review. It accepts a JSON payload with the updated `body` field and returns the updated review object. This means PR reviews can be updated after initial submission -- there is no need to always create a new review.

Documentation reference: GitHub REST API documentation for Pull Reviews -- "Update a pull request review" endpoint.

## Suggested Corrected Language

**Original requirement:**
> PR reviews cannot be updated after initial submission so always create a new review

**Suggested correction:**
> Update an existing eval review on subsequent runs instead of creating a new review each time

**Original notes:**
> The GitHub API does not support modifying a submitted review

**Suggested correction:**
> Use PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id} to update an existing review
