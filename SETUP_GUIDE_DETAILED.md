# Detailed Setup Guide with Step-by-Step Instructions

## 🔧 Complete Setup Process

### Part 1: Install Python Dependencies

```bash
cd /Users/han.ct/Documents/math_python_for_AI
pip install -r requirements.txt
```

Expected output:
```
Successfully installed google-auth-oauthlib-1.2.0 ...
```

---

### Part 2: Google Cloud Console Setup

#### Step 2.1: Create Project

1. **Go to:** https://console.cloud.google.com/
2. **Click:** "Select a project" dropdown (top left)
3. **Click:** "NEW PROJECT" button
4. **Enter project name:** `Math Python AI Automation`
5. **Click:** "CREATE"
6. **Wait:** Until project is created (notification will appear)
7. **Select:** Your new project from the dropdown

#### Step 2.2: Enable Google Drive API

1. **In the search bar (top), type:** `Google Drive API`
2. **Click:** "Google Drive API" from results
3. **Click:** "ENABLE" button
4. **Wait:** Until enabled (you'll see the API dashboard)

#### Step 2.3: Configure OAuth Consent Screen

1. **Go to:** https://console.cloud.google.com/apis/credentials/consent
2. **Or:** Navigate: "APIs & Services" → "OAuth consent screen" (left menu)

3. **Choose User Type:**
   - Select: **"External"**
   - Click: **"CREATE"**

4. **Fill in OAuth consent screen:**
   - **App name:** `Math Python AI Automation`
   - **User support email:** Your email
   - **Developer contact information:** Your email
   - Click: **"SAVE AND CONTINUE"**

5. **Scopes page:**
   - Click: **"SAVE AND CONTINUE"** (no changes needed)

6. **Test users page:** ⚠️ **IMPORTANT - This prevents the 403 error!**
   - Click: **"+ ADD USERS"**
   - Enter your Google email address (the one you'll use to run the script)
   - Click: **"ADD"**
   - Click: **"SAVE AND CONTINUE"**

7. **Summary page:**
   - Review your settings
   - Click: **"BACK TO DASHBOARD"**

#### Step 2.4: Create OAuth Credentials

1. **Go to:** https://console.cloud.google.com/apis/credentials
2. **Or:** Navigate: "APIs & Services" → "Credentials" (left menu)

3. **Click:** "CREATE CREDENTIALS" button (top)
4. **Select:** "OAuth client ID"

5. **Configure OAuth client:**
   - **Application type:** Desktop app
   - **Name:** `Math Python Desktop`
   - Click: **"CREATE"**

6. **Download credentials:**
   - A popup appears: "OAuth client created"
   - Click: **"DOWNLOAD JSON"** button
   - Save the file

7. **Rename the downloaded file:**
   ```bash
   # The downloaded file has a long name like:
   # client_secret_123456-xxxx.apps.googleusercontent.com.json
   
   # Rename it to:
   mv ~/Downloads/client_secret_*.json /Users/han.ct/Documents/math_python_for_AI/credentials.json
   ```

---

### Part 3: Verify Setup

```bash
python check_setup.py
```

Expected output:
```
============================================================
  Setup Validation
============================================================

[1] Checking Python packages...
✓ Package google-auth-oauthlib: Installed
✓ Package google-api-python-client: Installed

[2] Checking class information...
✓ Class information directory: Found (3 items)
    Found 3 class file(s):
      - Thông tin học sinh lớp Math-Python for AI (Tối thứ 2)...
      - Thông tin học sinh lớp Math-Python for AI (Tối thứ 3)...
      - Thông tin lớp Math-Python for AI (Chiều chủ nhật 3h-4h30)...

[3] Checking lessons...
✓ Lessons directory: Found (7 items)
    Found 7 lesson(s):
      ✓ lesson_1: Lesson_1.ipynb
      ✓ lesson_2: Lesson_2.ipynb
      ...

[4] Checking Google API setup...
✓ Google API credentials: Found
    ✓ Ready to authenticate with Google Drive

============================================================
  ✓ All checks passed! Ready to run automation.

  Next step: python upload_lesson.py
============================================================
```

---

### Part 4: Run the Automation

```bash
python upload_lesson.py
```

#### First Run - Authentication:

1. **Browser opens automatically**
2. **Sign in** with your Google account
3. **You may see:** "This app hasn't been verified"
   - Click: **"Advanced"**
   - Click: **"Go to Math Python AI Automation (unsafe)"**
4. **Grant permissions:**
   - Click: **"Allow"**
5. **Browser shows:** "The authentication flow has completed"
6. **Close browser** and return to terminal

#### What Happens Next:

```
============================================================
  Google Drive Lesson Automation System
============================================================

✓ Successfully authenticated with Google Drive

[1] Creating parent folder structure...
  Created folder: Math_python_for_AI (ID: 1a2b3c...)

[2] Found 3 class(es) to process

[3] Found 7 lesson(s) to upload

============================================================
Processing Class: Monday_Evening
============================================================

  Found 5 student(s) in this class
    1. Trịnh Khôi Nguyên (bichly6387@gmail.com)
    2. Nguyễn Ngọc Tâm Yên (bkhoanghanh@gmail.com)
    ...

  Creating class folder: Monday_Evening
  Created folder: Monday_Evening (ID: 1x2y3z...)

  Processing lesson_1...
  Created folder: lesson_1 (ID: 1p2q3r...)
    Uploading original: Lesson_1.ipynb
    Creating personalized copies:
      - Nguyen.ipynb for Trịnh Khôi Nguyên
      - Yen.ipynb for Nguyễn Ngọc Tâm Yên
      ...

... (continues for all classes and lessons) ...

============================================================
  ✓ Automation completed successfully!
============================================================

Summary:
  - Processed 3 class(es)
  - Created 7 lesson folder(s) per class
  - Generated personalized files for all students
  - Set up sharing permissions automatically

Check your Google Drive for the 'Math_python_for_AI' folder!
```

---

## 🚨 Common Issues and Solutions

### Issue 1: Error 403 - access_denied

**Error message:**
```
Math Python AI has not completed the Google verification process.
Error 403: access_denied
```

**Solution:**
1. Go to: https://console.cloud.google.com/apis/credentials/consent
2. Scroll to "Test users" section
3. Click "+ ADD USERS"
4. Add your email address
5. Click "SAVE"
6. Delete `token.pickle`: `rm token.pickle`
7. Run script again: `python upload_lesson.py`

See: [FIX_AUTH_ERROR.md](FIX_AUTH_ERROR.md) for details

---

### Issue 2: credentials.json not found

**Error message:**
```
FileNotFoundError: [Errno 2] No such file or directory: 'credentials.json'
```

**Solution:**
1. Go to: https://console.cloud.google.com/apis/credentials
2. Find your OAuth 2.0 Client ID
3. Click download icon (⬇️) on the right
4. Save as `credentials.json` in project folder

---

### Issue 3: Module not found errors

**Error message:**
```
ModuleNotFoundError: No module named 'google'
```

**Solution:**
```bash
pip install -r requirements.txt
```

Or install packages individually:
```bash
pip install google-auth-oauthlib google-api-python-client
```

---

### Issue 4: "This app hasn't been verified" warning

**This is NORMAL for testing apps.**

**What to do:**
1. Click "Advanced" link
2. Click "Go to Math Python AI Automation (unsafe)"
3. Continue with authorization

This warning appears because your app is in testing mode. It's safe to proceed.

---

## 🔍 Verification Commands

Check if everything is working:

```bash
# Check if credentials exist
ls -la credentials.json

# Check if packages are installed
python -c "import google.oauth2; print('✓ Google packages installed')"

# Run full validation
python check_setup.py

# Test authentication (will open browser)
python upload_lesson.py
```

---

## 📧 Support

If you encounter issues not covered here:

1. Check error messages carefully
2. Review [README.md](README.md) for detailed documentation
3. See [FIX_AUTH_ERROR.md](FIX_AUTH_ERROR.md) for OAuth issues
4. Check Google Cloud Console for API quotas

---

## ✅ Success Checklist

Before running the automation, ensure:

- [ ] Python packages installed (`pip install -r requirements.txt`)
- [ ] Google Cloud project created
- [ ] Google Drive API enabled
- [ ] OAuth consent screen configured
- [ ] **Your email added as test user** ⚠️ Important!
- [ ] OAuth credentials downloaded as `credentials.json`
- [ ] File `credentials.json` in project root
- [ ] Class CSV files in `class_information/` folder
- [ ] Lesson notebooks in `lessons/module_1/` folders
- [ ] `check_setup.py` passes all checks

Once all checked, run:
```bash
python upload_lesson.py
```

🎉 Your automation will create and organize ~120 files on Google Drive!

