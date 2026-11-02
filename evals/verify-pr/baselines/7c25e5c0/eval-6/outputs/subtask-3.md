# Root-Cause Task: Implement-task phase — Markdown exclusion gap

## Summary
Root-cause: implement-task did not account for Markdown being a primary file format in documentation-heavy repositories when implementing the Documentation Coverage check

## Description
The implement-task skill produced a blanket Markdown exclusion ("Markdown: not applicable — skip Markdown files") in the Documentation Coverage check without recognizing that the target repository's primary content files are Markdown. The implement-task skill should analyze the repository's file composition and adjust language-specific rules when the repository is predominantly Markdown-based.

## Classification
- **Knowledge type:** Universal
- **Method or Fact:** Method (language-agnostic analysis technique: "analyze the repository's primary file types before applying blanket language exclusions")
- **Phase:** implement-task
- **Root-cause analysis:** The defect is a method-based skill gap in the implement-task phase. The skill should check whether excluded file types are actually the repository's primary content format before applying a blanket exclusion.
