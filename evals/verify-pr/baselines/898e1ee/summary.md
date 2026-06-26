## Eval Results: verify-pr

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 12/12 | 0 | 100% |
| eval-2 | 11/11 | 0 | 100% |
| eval-3 | 14/14 | 0 | 100% |
| eval-4 | 10/10 | 0 | 100% |
| eval-5 | 5/10 | 5 | 50% |
| eval-6 | 8/10 | 2 | 80% |

### Failed Assertions

<details>
<summary>eval-5: 5 failing assertions</summary>

- **Assertion:** "The report contains a Test Change Classification row with MIXED — both additive and reductive signals are present across the test file changes"
  **Evidence:** "The report's summary table shows 'Test Change Classification | ADDITIVE | Net +3 test functions (4 base -&gt; 7 PR); removed test_recommend_purls_with_qualifiers replaced by test_recommend_purls_dedup with updated behavioral expectations; 3 new tests added in purl_simplify.rs'. The classification is ADDITIVE, not MIXED. While the report acknowledges a removed test and a replacement, it does not classify the overall change as MIXED."

- **Assertion:** "The structural summary or reductive findings identify the removed test function test_recommend_purls_with_qualifiers as a reductive signal"
  **Evidence:** "The report mentions the removal of test_recommend_purls_with_qualifiers in the Test Change Classification row ('removed test_recommend_purls_with_qualifiers replaced by test_recommend_purls_dedup') and in criterion-3.md ('The removed test_recommend_purls_with_qualifiers test verified the old behavior'), but does not identify it as a 'reductive signal'. The classification is ADDITIVE, indicating the removal was not treated as a reductive signal in the structural assessment."

- **Assertion:** "The structural summary or reductive findings note the assertion change in test_recommend_purls_basic — the PURL assertion changed from checking a fully qualified PURL with qualifiers to checking a versioned PURL without qualifiers, which the semantic assessment may identify as a relaxation contributing to the MIXED classification"
  **Evidence:** "The report mentions in criterion-1.md that test_recommend_purls_basic 'now asserts assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12")' and notes the test 'seeds PURLs with qualifiers... but expects them returned without qualifiers'. However, there is no explicit discussion of a relaxation of assertions or PURL assertion change as a reductive signal. There is no MIXED classification and no semantic assessment identifying this as a relaxation."

- **Assertion:** "The test change classification verdict appears in the verification report summary table and is accompanied by a detailed analysis section explaining the structural and semantic assessment"
  **Evidence:** "The Test Change Classification verdict appears in the summary table as 'Test Change Classification | ADDITIVE | Net +3 test functions (4 base -&gt; 7 PR)...'. However, there is no separate detailed analysis section explaining the structural and semantic assessment of test changes. The report has 'Acceptance Criteria Detail' and 'Test Requirements Detail' sections, but no dedicated 'Test Change Classification' analysis section with structural/semantic breakdown."

- **Assertion:** "The test change classification analysis is based on comparing base-branch and PR-branch file content (function additions, removals, assertion changes) — the structural and semantic assessment references test file content, not acceptance criteria or task requirements (constraint 1.18)"
  **Evidence:** "There is no dedicated test change classification analysis section in the report. The Test Change Classification row in the summary table provides only a brief note: 'Net +3 test functions (4 base -&gt; 7 PR); removed test_recommend_purls_with_qualifiers replaced by test_recommend_purls_dedup with updated behavioral expectations; 3 new tests added in purl_simplify.rs'. While this references function counts, there is no detailed structural or semantic assessment section that compares base-branch and PR-branch file content. The criterion files (criterion-1.md through criterion-5.md) analyze acceptance criteria, not test change classification."

</details>

<details>
<summary>eval-6: 2 failing assertions</summary>

- **Assertion:** "Eval pass rate and failing assertion details appear in the verification report's Test Quality row — the report includes eval-3's failing assertions about convention upgrade eligibility and sub-task creation"
  **Evidence:** "The Test Quality row in report.md's Verification Summary states: '| Test Quality | WARN | Eval Quality WARN: 91% pass rate, 2 regression failures in eval-3. No test files in diff (Repetitive Test Detection: N/A, Test Documentation: N/A) |'. While it mentions the pass rate (91%) and the count of regression failures (2 in eval-3), it does NOT include the specific failing assertion details about 'convention upgrade eligibility' and 'sub-task creation' in the Test Quality row itself. Those details appear in the 'Eval-3 regressions' note below the Eval Results table ('Convention upgrade eligibility and sub-task creation for suggestion-classified review comments'), but not in the Test Quality row as asserted."

- **Assertion:** "Root-cause investigation runs on the created eval failure sub-tasks — the report includes a Root-Cause Investigation verdict that is not N/A, indicating the investigation pipeline processed the eval failure sub-tasks"
  **Evidence:** "The report.md Verification Summary table does not contain a 'Root-Cause Investigation' row or verdict. The table rows are: Review Feedback, Scope Containment, Diff Size, Commit Traceability, Sensitive Patterns, CI Status, Acceptance Criteria, Test Quality, Test Change Classification, Verification Commands. There is no Root-Cause Investigation entry anywhere in the report."

</details>

**Pass rate:** 88% · **Tokens:** 72,017 · **Duration:** 271s

**Baseline** (`14692f2`): 100% · 64,828 tokens · 205s

