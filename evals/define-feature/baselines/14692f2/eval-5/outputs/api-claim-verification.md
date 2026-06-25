# External API Claim Verification

## Detected Claim

In the **Requirements** section (Section 4), the following claim was identified:

> "PR reviews cannot be updated after initial submission so always create a new review"
> Notes: "The GitHub API does not support modifying a submitted review"

This asserts that the GitHub REST API lacks the ability to update a pull request review after it has been submitted.

## Verification Result: INCORRECT

The claim is **incorrect**. The GitHub REST API does support updating a submitted pull request review.

### Evidence

The GitHub REST API provides the following endpoint for updating a review:

```
PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}
```

This endpoint allows modifying the body of a previously submitted pull request review. It accepts the `review_id` of the submitted review and a new `body` parameter to update the review content.

**Documentation reference:** GitHub REST API - Pull Request Reviews - Update a review

### Suggested Corrected Language

**Original requirement:**
> PR reviews cannot be updated after initial submission so always create a new review

**Corrected requirement:**
> PR reviews can be updated after submission using the GitHub REST API update endpoint; prefer updating an existing review over creating a new one to reduce notification noise

**Original notes:**
> The GitHub API does not support modifying a submitted review

**Corrected notes:**
> Use `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` to update an existing review rather than creating a new one
