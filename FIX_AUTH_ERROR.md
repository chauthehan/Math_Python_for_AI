# Fix: Error 403 - access_denied

## Problem
Your app is in "Testing" mode and your Google account isn't listed as a test user.

## Solution: Add Your Email as Test User

### Step 1: Go to OAuth Consent Screen
1. Visit: https://console.cloud.google.com/apis/credentials/consent
2. Make sure you're in the correct project: "Math Python AI Automation"

### Step 2: Add Test Users
1. Scroll down to **"Test users"** section
2. Click **"+ ADD USERS"** button
3. Enter your Google email address (the one you're using to authenticate)
4. Click **"SAVE"**

### Step 3: Run the Script Again
```bash
# Delete the failed token
rm token.pickle

# Run again
python upload_lesson.py
```

The browser will open again, and now you should be able to authorize!

---

## Alternative: Use Internal User Type (if available)

If all users are in the same Google Workspace organization:

1. Go to: https://console.cloud.google.com/apis/credentials/consent
2. Click **"EDIT APP"**
3. Change **User Type** from "External" to "Internal"
4. Click **"SAVE AND CONTINUE"**
5. Run `python upload_lesson.py` again

---

## What Emails to Add?

Add these email addresses as test users:
- **Your email** (the one running the script)
- Optionally: Any other accounts you want to access this automation

You do NOT need to add student emails as test users - they only receive shared files, they don't authenticate the app.

---

## Quick Checklist

- [ ] Go to OAuth consent screen in Google Cloud Console
- [ ] Click "ADD USERS" in Test users section
- [ ] Add your email address
- [ ] Click SAVE
- [ ] Delete `token.pickle` file
- [ ] Run `python upload_lesson.py` again

---

## Still Getting Errors?

### "This app hasn't been verified"
This is normal for testing apps. Click "Advanced" → "Go to Math Python AI (unsafe)"

### "Access blocked: Authorization Error"
Make sure the email you're logging in with matches exactly the one in test users.

### "Invalid credentials"
Your `credentials.json` might be wrong. Re-download from:
https://console.cloud.google.com/apis/credentials

