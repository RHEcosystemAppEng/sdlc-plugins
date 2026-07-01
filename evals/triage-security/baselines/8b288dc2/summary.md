## Eval Results: triage-security

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 10/10 | 0 | 100% |
| eval-10 | 5/5 | 0 | 100% |
| eval-11 | 5/5 | 0 | 100% |
| eval-12 | 5/5 | 0 | 100% |
| eval-13 | 5/5 | 0 | 100% |
| eval-14 | 5/5 | 0 | 100% |
| eval-15 | 5/5 | 0 | 100% |
| eval-16 | 7/7 | 0 | 100% |
| eval-17 | 4/5 | 1 | 80% |
| eval-19 | 5/5 | 0 | 100% |
| eval-2 | 5/5 | 0 | 100% |
| eval-20 | 4/4 | 0 | 100% |
| eval-21 | 4/4 | 0 | 100% |
| eval-22 | 4/4 | 0 | 100% |
| eval-23 | 4/4 | 0 | 100% |
| eval-24 | 4/4 | 0 | 100% |
| eval-3 | 5/5 | 0 | 100% |
| eval-4 | 5/5 | 0 | 100% |
| eval-5 | 6/6 | 0 | 100% |
| eval-6 | 6/6 | 0 | 100% |
| eval-7 | 5/5 | 0 | 100% |
| eval-8 | 5/5 | 0 | 100% |
| eval-9 | 5/5 | 0 | 100% |

### Failed Assertions

<details>
<summary>eval-17: 1 failing assertion</summary>

- **Assertion:** "Step 0 extracts the Embargo policy URL from the Security Configuration as an optional field without raising an error (§1.71 — backward compatible extraction)"
  **Evidence:** "The data-extraction.md output is labeled 'Step 1 -- Data Extraction' (no Step 0 output exists) and does not mention the Embargo policy URL at all. The URL only appears in embargo-check.md (Step 1.7) under its Configuration section. While the embargo-check.md does note backward compatibility ('If no Embargo policy URL were configured in Security Configuration, Step 1.7 would be skipped entirely regardless of severity'), the extraction is not demonstrated in the data extraction step as required by the assertion. No Step 0 output file exists."

</details>

**Pass rate:** 99% · **Tokens:** 45,946 · **Duration:** 89s

**Baseline** (`1f575ac4`): 97% · 49,041 tokens · 111s

