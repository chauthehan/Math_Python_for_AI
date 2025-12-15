# Quick Start Guide

## 🚀 Setup (One-time only)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Get Google Drive API Credentials

**Quick Steps:**
1. Go to: https://console.cloud.google.com/
2. Create new project: "Math Python AI Automation"
3. Enable "Google Drive API"
4. Create OAuth client ID (Desktop app)
5. Download as `credentials.json` → save in this folder

**Detailed instructions:** See [README.md](README.md)

### 3. Verify Setup
```bash
python check_setup.py
```

## ▶️ Run the Automation

```bash
python upload_lesson.py
```

**First time:** Browser will open for authentication → Click "Allow"

## 📁 What Gets Created on Google Drive

```
Math_python_for_AI/
├── Monday_Evening/
│   ├── lesson_1/
│   │   ├── Lesson_1.ipynb (original Colab notebook)
│   │   ├── Khoi.ipynb (→ shared with khoi@email.com, opens in Colab)
│   │   ├── Yen.ipynb (→ shared with yen@email.com, opens in Colab)
│   │   └── ...
│   ├── lesson_2/
│   ├── lesson_3/
│   └── ... (all 7 lessons)
├── Tuesday_Evening/
└── Sunday_Afternoon/
```

**🎉 All `.ipynb` files open directly in Google Colab!**  
Students just click → code runs in browser → no installation needed!

## 📋 Requirements

Your CSV files in `class_information/` must have:
- Column: `Họ và tên học sinh` (Student Name)
- Column: `Email sử dụng để học tập...` (Email)

## ⚠️ Troubleshooting

| Problem | Solution |
|---------|----------|
| Missing `credentials.json` | Download from Google Cloud Console |
| Import errors | Run `pip install -r requirements.txt` |
| Sharing failures | Check email addresses in CSV files |
| Authentication expired | Delete `token.pickle` and run again |

## 📊 Current Data Status

- **Classes:** 3
  - Monday Evening (5 students)
  - Tuesday Evening (6 students)  
  - Sunday Afternoon (5 students)
- **Lessons:** 7 (lesson_1 through lesson_7)
- **Files to create:** ~120+ personalized notebooks

## 🔒 Security Notes

- `credentials.json` - Keep private (in `.gitignore`)
- `token.pickle` - Authentication cache (in `.gitignore`)
- Never commit these files to Git

## ✨ Features

- ✅ Automatic folder organization
- ✅ Personalized **Google Colab** files for each student
- ✅ Auto-sharing with write permission
- ✅ Batch processing for all classes
- ✅ Clean naming (uses student first names)
- ✅ Students run code in browser - no installation needed!

---

**Need help?** Check [README.md](README.md) for detailed documentation.

