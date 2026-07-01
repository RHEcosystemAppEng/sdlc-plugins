## Eval Results: triage-security

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 10/10 | 0 | 100% |
| eval-10 | 5/5 | 0 | 100% |
| eval-11 | 5/5 | 0 | 100% |
| eval-12 | 5/5 | 0 | 100% |
| eval-13 | 5/5 | 0 | 100% |
| eval-14 | 4/5 | 1 | 80% |
| eval-15 | 5/5 | 0 | 100% |
| eval-16 | 7/7 | 0 | 100% |
| eval-17 | 5/5 | 0 | 100% |
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
| eval-8 | 5/5 | 0 | 100% |
| eval-9 | 5/5 | 0 | 100% |

### Failed Assertions

<details>
<summary>eval-14: 1 failing assertion</summary>

- **Assertion:** "The SBOM verification result is presented alongside the rpms.lock.yaml result in the dependency chain output, not as a separate section (Step 2.3.5 sub-step 6)"
  **Evidence:** "The SBOM verification results are in a SEPARATE file (sbom-verification.md), not integrated alongside rpms.lock.yaml in the dependency chain output. version-impact.md lines 55-62 reference 'See outputs/sbom-verification.md for the full SBOM verification analysis' and provides only a summary. While the individual version entries in sbom-verification.md do show both signals together (e.g., lines 13-17 for 2.2.0), the overall structure is a separate section/file rather than being presented alongside the rpms.lock.yaml result within the dependency chain context. However, examining more closely, the sbom-verification.md per-version entries DO present both rpms.lock.yaml and SBOM results side by side in the same code block (e.g., lines 13-14: 'rpms.lock.yaml: present... -&gt; explicit install / SBOM verification: present in both... -&gt; base image'). The summary table (lines 102-108) also puts them alongside. But the assertion says 'not as a separate section' and version-impact.md explicitly delegates to a separate file. This is a structural violation -- FAIL because the dependency chain output (version-impact.md) defers to a separate sbom-verification.md rather than presenting them together inline."

</details>

**Pass rate:** 99% · **Tokens:** 0 · **Duration:** 0s

**Baseline** (`b22bcfd2`): 100% · 67,626 tokens · 107s

