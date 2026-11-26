# External API Claim Verification (Simulated)

> Simulated per eval instructions — no WebSearch/WebFetch calls were made. The result
> below is what the verification step would present to the user.

## Claim Detected

- **Section:** Requirements (Step 3d), row 4
- **Requirement text:** "PR reviews cannot be updated after initial submission so always create a new review"
- **Notes text:** "The GitHub API does not support modifying a submitted review"
- **Matched patterns:** "X cannot be updated ... after creation"; "The API does not support Y"
- **External API:** GitHub REST API — Pull request reviews

## User Notification

> I detected a claim about an external API capability in the Requirements section:
> **"PR reviews cannot be updated after initial submission"** / **"The GitHub API does not
> support modifying a submitted review"**. I'll verify this against the official GitHub
> REST API documentation before finalizing this section.

## Verification

- **Simulated search:** "GitHub REST API update pull request review"
- **Official documentation:** https://docs.github.com/en/rest/pulls/reviews#update-a-review-for-a-pull-request
- **Finding:** The GitHub REST API provides an endpoint to update a review:

  ```
  PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}
  ```

  "Update a review for a pull request" — updates the contents (`body`, required parameter)
  of a specified review summary comment. This applies to submitted reviews.

## Result: INCORRECT

The claim is **incorrect**. The GitHub REST API does support modifying a submitted
review's body via `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}`.

## Suggested Corrected Language

The original requirement presents "always create a new review" as forced by an API
limitation. Since that limitation does not exist, the suggested correction removes the
false rationale while keeping the user's behavior choice intact (no new requirement is
invented):

| Requirement | Notes | Is MVP? |
|---|---|---|
| Always create a new review for each eval run | Design choice, not an API limitation — the GitHub REST API supports updating a submitted review body via `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` ([docs](https://docs.github.com/en/rest/pulls/reviews#update-a-review-for-a-pull-request)); updating the existing review is an available alternative | Yes |

Prompt to user:

> The claim appears to be incorrect. GitHub documents
> `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` ("Update a review for
> a pull request"), which updates the body of a submitted review. I suggest the corrected
> wording above. Do you want to apply this correction (or instead change the requirement to
> update the existing review)?

**Simulated user response:** Accept the suggested correction. The preview uses the corrected language.
