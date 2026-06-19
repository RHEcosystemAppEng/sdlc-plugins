# Duplicate and Sibling Check — TC-8003

## Step 4 — Duplicate/Sibling Analysis

### JQL Search Results

A JQL search for sibling Vulnerability issues with the same CVE label was performed:

```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8003
```

**Result**: 1 sibling found.

| Issue | Summary | Status | Labels | Affects Versions | Stream Suffix |
|-------|---------|--------|--------|------------------|---------------|
| TC-7999 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | In Progress | CVE-2026-31812, pscomponent:org/rhtpa-server | RHTPA 2.2.0, RHTPA 2.2.1 | [rhtpa-2.2] |

### Classification

**TC-7999** has the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** stream.
**TC-8003** (the current issue) also has the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** stream.

Both issues are scoped to the **same stream** (2.2.x).

Classification: **Same-stream sibling** (duplicate).

### Step 4.1 — Same-Stream Duplicate Detection

TC-7999 is a same-stream sibling that is currently **In Progress** (open and actively being worked on). Per the triage-security skill rules:

> "If a same-stream sibling exists and is open or in progress: Recommendation: Close the current issue as Duplicate."

**Duplicate confirmed:**

- TC-7999 is already tracking CVE-2026-31812 for the 2.2.x stream
- TC-7999 is in status "In Progress", meaning work has already begun
- TC-7999 has Affects Versions: RHTPA 2.2.0, RHTPA 2.2.1 (which covers the affected versions from TC-8003)
- TC-8003 has Affects Versions: RHTPA 2.2.0 (a subset of TC-7999's versions)
- Both issues track the same CVE, same library (quinn-proto), same stream ([rhtpa-2.2])

### Recommendation

**Close TC-8003 as Duplicate of TC-7999.**

Proposed actions (pending engineer confirmation):

1. Add comment to TC-8003:
   > "Duplicate of TC-7999 — same CVE (CVE-2026-31812) tracked for the same stream [rhtpa-2.2]. TC-7999 is already In Progress with Affects Versions [RHTPA 2.2.0, RHTPA 2.2.1]. Version impact analysis confirms overlap: quinn-proto versions before 0.11.14 affect versions 2.2.0, 2.2.1, and 2.2.2 in this stream."

2. Transition TC-8003 to **Closed** with resolution **Duplicate**.

3. Assign TC-8003 to current user.

4. Add the `ai-cve-triaged` label to TC-8003.

### Note on Affects Versions Gap

TC-7999 already covers RHTPA 2.2.0 and RHTPA 2.2.1. The version impact analysis shows that RHTPA 2.2.2 is also affected (it is a retag of 2.2.1 and ships quinn-proto 0.11.12). If RHTPA 2.2.2 is not yet in TC-7999's Affects Versions, the engineer may want to update TC-7999 to include it. However, this is outside the scope of TC-8003's triage — the current issue is a duplicate and should be closed.
