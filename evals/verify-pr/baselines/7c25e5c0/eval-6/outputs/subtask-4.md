# Root-Cause Task: Verify-pr convention upgrade pipeline gap

## Summary
Root-cause: verify-pr convention upgrade pipeline does not document evaluation reasoning for suggestion-classified comments

## Description
The verify-pr skill's convention upgrade pipeline (Style/Conventions sub-agent Check 1) evaluates suggestion-classified comments for convention upgrade eligibility, but the eval-3 failures show that the evaluation reasoning is not documented in the classification output. When a suggestion is NOT upgraded, the classification output should still document what was checked (CONVENTIONS.md lookup, codebase pattern search) and why no match was found. This documentation gap causes eval assertions that check for convention upgrade analysis to fail.

## Classification
- **Knowledge type:** Universal
- **Method or Fact:** Method (language-agnostic analysis technique: "document the convention upgrade analysis in the classification output even when no upgrade occurs")
- **Phase:** verify-pr (skill self-improvement)
- **Root-cause analysis:** The defect is a method-based skill gap in the verify-pr skill itself. The convention upgrade check performs the analysis but does not persist the reasoning in the output files, making it impossible for evals to verify the analysis was performed.
