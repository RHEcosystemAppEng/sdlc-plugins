# External API Claim Verification

## Detected Claim

In the **Requirements** section (Section 4), the following claim was identified:

> "PR reviews cannot be updated after initial submission so always create a new review"
> "The GitHub API does not support modifying a submitted review"

This asserts that the GitHub REST API lacks the capability to update or modify a PR review after it has been submitted, and therefore a new review must always be created.

## Verification Result: INCORRECT

The claim is **incorrect**. The GitHub REST API does support updating a submitted pull request review.

### Correct Endpoint

**`PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}`**

This endpoint allows updating the body of a previously submitted pull request review. It accepts the following parameters:

- `owner` (string, required) - The account owner of the repository
- `repo` (string, required) - The name of the repository
- `pull_number` (integer, required) - The number of the pull request
- `review_id` (integer, required) - The unique identifier of the review
- `body` (string, required) - The body text of the pull request review

Documentation reference: https://docs.github.com/en/rest/pulls/reviews#update-a-pull-request-review

## Suggested Corrected Language

**Original requirement:**
> PR reviews cannot be updated after initial submission so always create a new review

**Corrected requirement:**
> Update the existing eval review on subsequent runs instead of creating a new review each time

**Original notes:**
> The GitHub API does not support modifying a submitted review

**Corrected notes:**
> Use PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id} to update an existing review rather than creating duplicates
