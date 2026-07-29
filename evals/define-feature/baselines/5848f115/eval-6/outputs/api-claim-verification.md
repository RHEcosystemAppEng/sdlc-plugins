# External API Claim Verification

## Detected Claim

**Section:** Requirements (Section 4)

**Claim:** "PR reviews cannot be updated after initial submission so always create a new review" / "The GitHub API does not support modifying a submitted review"

**API:** GitHub REST API

## Verification Result

**Status:** UNVERIFIED (web tools unavailable)

WebSearch and WebFetch are unavailable in this environment. The claim could not be verified against the official GitHub REST API documentation.

> I detected a claim about an external API but cannot verify it right now
> (web tools unavailable). The claim is: **"The GitHub API does not support modifying a submitted review — PR reviews cannot be updated after initial submission."** Would you like to proceed as-is, or verify it manually before continuing?

## Recommendation

This claim should be manually verified before finalizing the Feature. The GitHub REST API documentation for pull request reviews should be checked at:
- https://docs.github.com/en/rest/pulls/reviews

Specifically, check whether a `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` endpoint exists, which would allow updating a submitted review and contradict the claim.

## Impact on Requirements

If the claim is incorrect and the GitHub API does support updating reviews, Requirement 4 ("PR reviews cannot be updated after initial submission so always create a new review") should be revised. The implementation could update an existing review instead of always creating a new one, which would reduce noise on pull requests.
