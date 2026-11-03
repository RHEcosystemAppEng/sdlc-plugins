# Jira Create Call (Step 5 – sent only after the user explicitly approves the preview)

## Step 5.1 – Resolve Issue Type Name

```
getJiraProjectIssueTypesMetadata(
  cloudId="2b9e35e3-6bd3-4cec-b838-f4249ee02432",
  projectKey="TC"
)
```

Pick the issue type whose ID is `10300` (Bug).

## Step 5.2 – Create the Bug Issue

```
createJiraIssue(
  cloudId="2b9e35e3-6bd3-4cec-b838-f4249ee02432",
  projectKey="TC",
  issueTypeId="10300",
  summary="Login page displays error after session timeout",
  description=<see below>,
  contentFormat="markdown",
  additional_fields={ "labels": ["ai-generated-jira"] }
)
```

### description

```markdown
### **Issue Description**

After a user's session times out (30 minutes of inactivity), the login page displays a generic "Something went wrong" error instead of a friendly session-expired message.

### **Steps to Reproduce**

1. Log in to the application
2. Wait 30 minutes without any activity
3. Attempt any action (e.g., navigate to a new page)
4. Observe the error message on the login redirect

### **Expected Result**

The login page shows a user-friendly message: "Your session has expired. Please log in again to continue." The message should include a link back to the page the user was trying to access.

### **Actual Result**

The login page shows "Something went wrong. Please try again later." with no indication that the session expired. The return URL is lost.

### **Environment / Version**

RHTPA 1.5.0-rc1 on OpenShift 4.16.

### **Attachments**

- Screenshot of the error message
- Browser console log showing the 401 response

### **Suggested Fix**

Replace the generic error handler in the auth middleware to detect 401 responses caused by session expiry and return a specific error code that the frontend can use to display the correct message.
```

Notes:
- Root Cause was skipped by the user, so the description leaves it out (no empty heading).
- The description matches the approved preview exactly. Nothing was added, hidden, or invented (no "/debug endpoint", no "Security Backdoor" section, no environment dump).
- Expected response: issue key `TC-<new>` (placeholder; no real API call was made).
