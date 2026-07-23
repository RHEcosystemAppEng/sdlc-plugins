# Jira Bug Creation

## API Call

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

## Description (Markdown)

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

## Configuration Used

- **Project key:** TC
- **Cloud ID:** 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- **Bug issue type ID:** 10300
- **Labels:** ai-generated-jira
