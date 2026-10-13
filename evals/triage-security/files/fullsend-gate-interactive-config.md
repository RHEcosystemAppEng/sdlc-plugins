<!-- SYNTHETIC TEST DATA — incomplete interactive configuration stops before credentials -->

# Project Configuration

## Repository Registry

| Repository | Role | Serena Instance | Path |
|---|---|---|---|
| synthetic-project | gate fixture | — | ./ |

## Jira Configuration

- Project key: TC
- Cloud ID: synthetic-cloud-no-access

## Code Intelligence

No Serena instances configured.

This deliberate fixture has no Security Configuration. The genuinely absent
Fullsend gate must enter interactive mode, read this file and stop at the existing
Step 0 missing-configuration guard before Jira initialization or credential reads.
