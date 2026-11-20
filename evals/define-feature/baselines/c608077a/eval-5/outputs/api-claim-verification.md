# External API Claim Verification (simulated)

## Step 0 – Project Configuration validation

- Repository Registry: present (trustify-backend)
- Jira Configuration: Project key `TC`, Cloud ID `2b9e35e3-6bd3-4cec-b838-f4249ee02432`, Feature issue type ID `10142`
- Code Intelligence: present
- Result: PASS, proceeding

## Sections scanned

| Section | Claims detected |
|---|---|
| Feature Overview | None. It mentions posting eval results as a PR review but makes no claim about what the API can or cannot do. |
| Requirements | **1 claim detected** (row 4) |

## Detected claim

- **Section:** Requirements, row 4
- **Requirement text:** "PR reviews cannot be updated after initial submission so always create a new review"
- **Notes text:** "The GitHub API does not support modifying a submitted review"
- **Matched patterns:** "X cannot be updated ... after creation"; "The API does not support Y"
- **External API:** GitHub REST API (Pull Request Reviews)

## User notification (as presented)

> I found a claim about an external API in the Requirements section: **"PR reviews cannot be updated after initial submission"** / **"The GitHub API does not support modifying a submitted review."** I'll check it against the official GitHub REST API documentation before we finalize this section.

## Verification (simulated, no WebSearch or WebFetch calls were made)

- **Planned search:** `GitHub REST API update pull request review`
- **Official documentation:** https://docs.github.com/en/rest/pulls/reviews#update-a-review-for-a-pull-request
- **Finding:** The GitHub REST API has an endpoint for updating a pull request review:

  ```
  PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}
  ```

  It takes a `body` parameter (the new body text for the review) and returns the updated review. The endpoint name is "Update a review for a pull request". The claim says modifying a submitted review is impossible, and this endpoint shows that it is possible.

## Result: **INCORRECT**

The GitHub REST API does let you update a submitted pull request review's body. The requirement to "always create a new review" rests on a false premise.

## Suggested corrected language (presented to the user for confirmation)

| Requirement | Notes | Is MVP? |
|---|---|---|
| Update the existing eval-results PR review on subsequent CI runs rather than creating a new review each time | The GitHub REST API supports updating a submitted review's body via `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` ([docs](https://docs.github.com/en/rest/pulls/reviews#update-a-review-for-a-pull-request)) | Yes |

> The claim that submitted PR reviews can't be modified is incorrect. GitHub's REST API provides `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` to update a review's body. I suggest the corrected wording above. Do you confirm this correction, or would you like to keep the original wording or phrase it differently?

**Simulated user response:** Correction confirmed. The corrected row replaces row 4 in the preview.

Note: the corrected row keeps the user's intent (how repeat eval runs are handled on a PR) and fixes only the incorrect factual premise. It adds no new requirements.
