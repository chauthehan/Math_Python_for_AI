# Google Drive Lesson Automation System

This system automates the process of organizing class materials on Google Drive, creating personalized lesson files for each student.

## Features

- ✅ Reads student information from CSV files
- ✅ Creates organized folder structure on Google Drive
- ✅ Uploads lesson notebooks as **Google Colab** files
- ✅ Generates personalized copies for each student
- ✅ Sets up sharing permissions automatically
- ✅ Students can run code directly in browser (no installation needed!)

## Setup Instructions

### Step 1: Install Required Packages

```bash
pip install -r requirements.txt
```

### Step 2: Set Up Google Drive API

1. **Go to Google Cloud Console:**
   - Visit: https://console.cloud.google.com/

2. **Create a New Project:**
   - Click "Select a project" → "New Project"
   - Name it: "Math Python AI Automation"
   - Click "Create"

3. **Enable Google Drive API:**
   - In the search bar, type "Google Drive API"
   - Click on "Google Drive API"
   - Click "Enable"

4. **Create OAuth 2.0 Credentials:**
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "OAuth client ID"
   - If prompted, configure the OAuth consent screen:
     - User Type: External
     - App name: "Math Python AI Automation"
     - User support email: your email
     - Developer contact: your email
     - Click "Save and Continue"
     - Scopes: Skip this, click "Save and Continue"
     - Test users: Add your Google account email
     - Click "Save and Continue"
   
5. **Download Credentials:**
   - Back in Credentials page, click "Create Credentials" → "OAuth client ID"
   - Application type: "Desktop app"
   - Name: "Math Python Desktop"
   - Click "Create"
   - Click "Download JSON"
   - **IMPORTANT:** Save the downloaded file as `credentials.json` in this project folder

### Step 3: Run the Automation Script

```bash
python upload_lesson.py
```

**First Run:**
- A browser window will open
- Sign in with your Google account
- Click "Allow" to grant permissions
- The script will create a `token.pickle` file for future use

## Folder Structure Created

```
Math_python_for_AI/
├── Monday_Evening_7PM/
│   ├── lesson_1/
│   │   ├── Lesson_1.ipynb (original)
│   │   ├── Khoi.ipynb (personalized for student Khoi)
│   │   ├── Yen.ipynb (personalized for student Yen)
│   │   └── ...
│   ├── lesson_2/
│   │   └── ...
│   └── ...
├── Tuesday_Evening_7PM/
│   └── ...
└── Sunday_Afternoon_3PM/
    └── ...
```

## How It Works

1. **Reads Class Information:**
   - Scans `class_information/` folder for CSV files
   - Extracts student names and emails

2. **Creates Folder Structure:**
   - Creates parent folder: `Math_python_for_AI`
   - Creates class folders based on schedule
   - Creates lesson folders: `lesson_1`, `lesson_2`, etc.

3. **Uploads Files as Google Colab Notebooks:**
   - Uploads original lesson notebook to each lesson folder
   - Creates personalized copies for each student
   - Names files using student's first name
   - **Uses Colab MIME type so files open in Google Colab**

4. **Sets Permissions:**
   - Shares each student's personalized file with their email
   - Grants "writer" access so students can edit their files
   - Students can click and run code directly in browser!

## Student Information Format

CSV files in `class_information/` must contain these columns:
- `Họ và tên học sinh` (Student Name)
- `Email sử dụng để học tập  (email riêng hoặc email của phụ huynh nếu chưa có)` (Email)

## Troubleshooting

### "credentials.json not found"
- Download OAuth credentials from Google Cloud Console
- Save as `credentials.json` in project root

### "Permission denied" errors
- Make sure you've enabled Google Drive API
- Check that test users are added in OAuth consent screen

### Files not sharing with students
- Verify email addresses in CSV files are correct
- Check your Google Drive sharing settings

## Notes

- First run requires browser authentication
- Subsequent runs use saved `token.pickle`
- Each student gets editor access to their personalized files
- Original lesson files are uploaded but not shared individually
- **All notebooks open as Google Colab files** - students can run code in browser
- No Python installation needed for students - just a Google account!

## Google Colab Integration

All `.ipynb` files are uploaded as Google Colab notebooks, which means:
- ✅ Students click on file → Opens directly in browser
- ✅ Can run Python code immediately (no setup required)
- ✅ Free GPU/TPU access for advanced lessons
- ✅ Auto-saves to Google Drive
- ✅ Works on any device (PC, Mac, iPad, Chromebook)

See [COLAB_INFO.md](COLAB_INFO.md) for detailed information about Colab integration.

