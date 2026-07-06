## Eval Results: triage-security

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 11/11 | 0 | 100% |
| eval-10 | 5/5 | 0 | 100% |
| eval-11 | 5/5 | 0 | 100% |
| eval-12 | 5/5 | 0 | 100% |
| eval-13 | 5/5 | 0 | 100% |
| eval-14 | 5/5 | 0 | 100% |
| eval-15 | 5/5 | 0 | 100% |
| eval-16 | 7/7 | 0 | 100% |
| eval-18 | 5/5 | 0 | 100% |
| eval-19 | 5/5 | 0 | 100% |
| eval-2 | 5/5 | 0 | 100% |
| eval-20 | 4/4 | 0 | 100% |
| eval-21 | 4/4 | 0 | 100% |
| eval-22 | 4/4 | 0 | 100% |
| eval-23 | 4/4 | 0 | 100% |
| eval-24 | 4/4 | 0 | 100% |
| eval-25 | 4/4 | 0 | 100% |
| eval-3 | 5/5 | 0 | 100% |
| eval-4 | 5/5 | 0 | 100% |
| eval-5 | 6/6 | 0 | 100% |
| eval-6 | 6/6 | 0 | 100% |
| eval-7 | 5/5 | 0 | 100% |
| eval-8 | 5/8 | 3 | 62% |
| eval-9 | 5/5 | 0 | 100% |

### Failed Assertions

<details>
<summary>eval-8: 3 failing assertions</summary>

- **Assertion:** "Step 4.3 creates a Related link between the current CVE (TC-8010) and the related CVE (TC-8008) with an idempotency check on existing issuelinks before creating"
  **Evidence:** "overlap-check.md line 66 proposes 'Create Related link: TC-8010 &lt;-&gt; TC-8008' but this is listed under 'Proposed actions (pending engineer confirmation)' (line 64), not confirmed as executed. Furthermore, there is no explicit idempotency check on existing issuelinks in Step 4.3 before proposing the link creation. While data-extraction.md line 24 notes 'Existing issue links | None', this is in Step 1, not an idempotency guard in Step 4.3."

- **Assertion:** "Step 4.3 creates a Depend link from the covering remediation task (TC-8009) to the current CVE (TC-8010) with an idempotency check on existing issuelinks before creating"
  **Evidence:** "overlap-check.md line 67 proposes 'Create Depend link: TC-8010 -&gt; TC-8009' but this is listed under 'Proposed actions (pending engineer confirmation)' (line 64), not confirmed as executed. No explicit idempotency check on existing issuelinks is demonstrated in the Step 4.3 output before proposing link creation."

- **Assertion:** "A comment is posted on the current CVE documenting the cross-CVE overlap finding — including the related CVE key (TC-8008), covering task key (TC-8009), library (axios), bump version (1.9.0), and fix threshold (1.8.2)"
  **Evidence:** "overlap-check.md lines 68-74 contain a proposed comment that includes all required elements (TC-8008, TC-8009, axios, 1.9.0, 1.8.2). However, the comment is listed under 'Proposed actions (pending engineer confirmation)' (line 64) and is not confirmed as actually posted. triage-outcome.md line 23 similarly lists 'Post cross-CVE overlap comment' as a 'Proposed Jira Action (pending engineer confirmation)'. No evidence the comment was actually posted to the issue."

</details>

**Pass rate:** 98% · **Tokens:** 44,243 · **Duration:** 111s

**Baseline** (`7b46435b`): 98% · 56,030 tokens · 134s

