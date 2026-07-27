# External API Claim Verification

## Detected Claim

In **Section 4 — Requirements**, the following claim was identified:

> **Claim:** "PR reviews cannot be updated after initial submission so always create a new review"
> **Supporting note:** "The GitHub API does not support modifying a submitted review"

This is a statement asserting that the GitHub REST API lacks the capability to modify a PR review after it has been submitted.

## Verification Method

Searched the official GitHub REST API documentation for pull request review endpoints to determine whether updating a submitted review is supported.

## Verification Result: INCORRECT

The claim is **incorrect**. The GitHub REST API **does** support updating a submitted pull request review.

**Evidence:**

- **Endpoint:** `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}`
- **Capability:** Updates the body (top-level comment) of a submitted pull request review.
- **Documentation:** [GitHub REST API — Update a pull request review](https://docs.github.com/en/rest/pulls/reviews#update-a-pull-request-review)

The `PUT` method on this endpoint allows modifying the review body after the review has been submitted. This means the requirement to "always create a new review" is based on an incorrect premise.

## Suggested Correction

The requirement should be revised to account for the ability to update existing reviews. Suggested corrected language:

- **Requirement:** "Update the existing eval review if one was previously posted, or create a new review if none exists"
- **Notes:** "Use `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` to update an existing review"
