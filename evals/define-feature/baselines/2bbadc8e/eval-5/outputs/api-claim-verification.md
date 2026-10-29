# External API Claim Verification

## Detected Claim

**Section:** Requirements (Section 4)

**Claim:** "PR reviews cannot be updated after initial submission" / "The GitHub API does not support modifying a submitted review"

**Requirement row:** "PR reviews cannot be updated after initial submission so always create a new review"

**Notes from user:** "The GitHub API does not support modifying a submitted review"

## Verification Process

1. **Claim identified:** The Requirements table contains an assertion that the GitHub REST API lacks the capability to update a submitted pull request review. This is a negative capability claim about an external API ("The API does not support Y").

2. **Verification against official documentation:** Searched for the GitHub REST API documentation on pull request reviews. The official GitHub REST API reference documents the following endpoint:

   **`PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}`**

   - **Documentation:** https://docs.github.com/en/rest/pulls/reviews#update-a-pull-request-review
   - **Method:** PUT
   - **Purpose:** Update the body text of a pull request review that has already been submitted.
   - **Required parameter:** `body` (string) -- The body text of the review.
   - **Authentication:** Requires appropriate repository permissions.

3. **Result:** The claim is **INCORRECT**. The GitHub REST API **does** support updating a submitted pull request review via the PUT endpoint listed above. The `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` endpoint allows modifying the body of an already-submitted review.

## Suggested Correction

The requirement should be revised to acknowledge that reviews can be updated. Instead of always creating a new review, the implementation should update the existing review when one already exists from a previous CI run.

**Original wording:**
> PR reviews cannot be updated after initial submission so always create a new review

**Corrected wording:**
> Update the existing PR review if one was previously posted by the CI workflow; create a new review only on the first run

**Original notes:**
> The GitHub API does not support modifying a submitted review

**Corrected notes:**
> Use PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id} to update an existing review
