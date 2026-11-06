# Jira Create Issue (Step 5 – simulated, not executed)

Preconditions: The user approved the preview in Step 4. No MCP or Jira API calls were made. This file records the intended call.

## Step 5.1 – Resolve Issue Type Name

```
getJiraProjectIssueTypesMetadata(
  cloudId="2b9e35e3-6bd3-4cec-b838-f4249ee02432",
  projectKey="TC"
)
```
Look up the issue type with ID `10300` (expected name: Bug).

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

Expected result: the created issue key, recorded as `TC-<new>` (placeholder because no real call was made).
