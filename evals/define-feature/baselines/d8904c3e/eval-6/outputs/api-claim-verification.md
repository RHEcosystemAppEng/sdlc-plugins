# External API Claim Verification

## Detected Claim

**Source section:** Requirements (Section 4)

**Requirement:** PR reviews cannot be updated after initial submission so always create a new review

**Claim:** "The GitHub API does not support modifying a submitted review"

**Classification:** Assertion that an external API lacks a specific capability (update/modify operation)

## Verification Result

**Status:** UNVERIFIED (fallback)

**Reason:** Web tools (WebSearch, WebFetch) are unavailable. The claim could not be verified against the official GitHub REST API documentation.

**Fallback message presented to user:**

> I detected a claim about an external API but cannot verify it right now
> (web tools unavailable). The claim is: **"The GitHub API does not support
> modifying a submitted review."** Would you like to proceed as-is, or
> verify it manually before continuing?

## Recommendation

This claim should be manually verified before implementation. The user should
check the GitHub REST API documentation for Pull Request Reviews to confirm
whether an update endpoint exists (e.g.,
`PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}`).

If the claim is incorrect and the API does support updating reviews, the
requirement "always create a new review" may need to be revised to consider
updating existing reviews instead.
