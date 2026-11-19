<!-- SYNTHETIC TEST DATA — Bug issue whose root cause lives in a different repository than the reporting repository, for triage-bug eval testing -->

# Mock Jira Bug Issue (Cross-Repository Root Cause)

**Key**: ACME-530
**Summary**: Advisory list order flips between requests for advisories sharing a document ID
**Issue Type**: Bug (ID: 10020)
**Status**: New
**Labels**: reported-by-user
**Component**: acme-backend
**Web URL**: https://mock-jira.example.com/browse/ACME-530

---

## Description

### **Issue Description**

`GET /api/v2/advisories` returns the advisory list in a different order on every
request. When two advisories share the same `document_id`, consecutive calls
sometimes return them swapped. The handler sorts the rows in memory before
serializing the response, so that one endpoint looks stable, but every other
consumer of the shared data-access layer still receives a non-deterministic list.

### **Steps to Reproduce**

1. Load two advisories that share the same `document_id`.
2. Call `GET /api/v2/advisories` ten times in a row.
3. Compare the returned advisory arrays between calls.

### **Expected Result**

Every call returns advisories in the same, stable order — for advisories sharing a
`document_id`, the order is deterministic.

### **Actual Result**

The advisory order differs between calls: advisories sharing the same `document_id`
appear in a different sequence on different requests.

### **Environment / Version**

Product version: 0.9.0

### **Attachments**

None.

### **Suggested Fix**

The in-memory sort in the handler hides the problem but does not fix it. The
advisory query should define an explicit ordering so every consumer gets a
deterministic result.
