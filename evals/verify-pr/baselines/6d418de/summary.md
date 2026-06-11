## Eval Results: verify-pr

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 12/12 | 0 | 100% |
| eval-2 | 11/11 | 0 | 100% |
| eval-3 | 14/14 | 0 | 100% |
| eval-4 | 10/10 | 0 | 100% |
| eval-5 | 9/10 | 1 | 90% |
| eval-6 | 9/10 | 1 | 90% |

### Failed Assertions

<details>
<summary>eval-5: 1 failing assertion</summary>

- **Assertion:** "The structural summary or reductive findings note the assertion change in test_recommend_purls_basic — the PURL assertion changed from checking a fully qualified PURL with qualifiers to checking a versioned PURL without qualifiers, which the semantic assessment may identify as a relaxation contributing to the MIXED classification"
  **Evidence:** "report.md describes test_recommend_purls_basic as 'Assertions tightened to verify simplified PURLs without qualifiers (MODIFIED)' — it characterizes the change as 'tightened' rather than noting the shift from a fully qualified PURL assertion to a versioned PURL without qualifiers. The report does not characterize the assertion change as a relaxation or note that it contributes to the MIXED classification. The criterion-1.md file shows the new assertion 'assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12")' but does not discuss the original assertion value or characterize the change as a relaxation."

</details>

<details>
<summary>eval-6: 1 failing assertion</summary>

- **Assertion:** "Root-cause investigation runs on the created eval failure sub-tasks — the report includes a Root-Cause Investigation verdict that is not N/A, indicating the investigation pipeline processed the eval failure sub-tasks"
  **Evidence:** "report.md line 6: '| Root-Cause Investigation | N/A | Review feedback is repo-specific (Markdown-heavy repository context); convention gap -- no sub-task needed beyond the review feedback fix |'. The Root-Cause Investigation verdict is N/A, not a non-N/A value. The investigation pipeline did not process the eval failure sub-tasks. The assertion requires the verdict to be 'not N/A' but it is N/A."

</details>

**Pass rate:** 97% · **Tokens:** 65,665 · **Duration:** 261s

**Baseline** (`7160d2f`): 92% · 55,871 tokens · 158s

