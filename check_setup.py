"""
Setup validation script - checks if everything is ready before running the automation
"""

import os
import sys

def check_file_exists(filepath, description):
    """Check if a file exists"""
    if os.path.exists(filepath):
        print(f"✓ {description}: Found")
        return True
    else:
        print(f"✗ {description}: NOT FOUND")
        return False

def check_directory_exists(dirpath, description):
    """Check if a directory exists"""
    if os.path.exists(dirpath) and os.path.isdir(dirpath):
        count = len([f for f in os.listdir(dirpath) if not f.startswith('.')])
        print(f"✓ {description}: Found ({count} items)")
        return True
    else:
        print(f"✗ {description}: NOT FOUND")
        return False

def check_python_packages():
    """Check if required packages are installed"""
    required_packages = [
        ('google.oauth2', 'google-auth-oauthlib'),
        ('googleapiclient', 'google-api-python-client'),
    ]
    
    all_installed = True
    for module_name, package_name in required_packages:
        try:
            __import__(module_name)
            print(f"✓ Package {package_name}: Installed")
        except ImportError:
            print(f"✗ Package {package_name}: NOT INSTALLED")
            all_installed = False
    
    return all_installed

def main():
    print("\n" + "="*60)
    print("  Setup Validation")
    print("="*60 + "\n")
    
    all_checks_passed = True
    
    # Check 1: Python packages
    print("[1] Checking Python packages...")
    if not check_python_packages():
        all_checks_passed = False
        print("    → Run: pip install -r requirements.txt")
    print()
    
    # Check 2: Class information directory
    print("[2] Checking class information...")
    class_info_dir = '/Users/han.ct/Documents/math_python_for_AI/class_information'
    if not check_directory_exists(class_info_dir, "Class information directory"):
        all_checks_passed = False
    else:
        csv_files = [f for f in os.listdir(class_info_dir) if f.endswith('.csv')]
        print(f"    Found {len(csv_files)} class file(s):")
        for csv_file in csv_files:
            print(f"      - {csv_file}")
    print()
    
    # Check 3: Lessons directory
    print("[3] Checking lessons...")
    lessons_dir = '/Users/han.ct/Documents/math_python_for_AI/lessons/module_1'
    if not check_directory_exists(lessons_dir, "Lessons directory"):
        all_checks_passed = False
    else:
        lesson_folders = [d for d in os.listdir(lessons_dir) 
                         if os.path.isdir(os.path.join(lessons_dir, d)) 
                         and d.startswith('lesson_')]
        print(f"    Found {len(lesson_folders)} lesson(s):")
        for lesson in sorted(lesson_folders):
            lesson_path = os.path.join(lessons_dir, lesson)
            notebooks = [f for f in os.listdir(lesson_path) if f.endswith('.ipynb')]
            if notebooks:
                print(f"      ✓ {lesson}: {notebooks[0]}")
            else:
                print(f"      ✗ {lesson}: No notebook found!")
                all_checks_passed = False
    print()
    
    # Check 4: Google API credentials
    print("[4] Checking Google API setup...")
    if check_file_exists('credentials.json', "Google API credentials"):
        print("    ✓ Ready to authenticate with Google Drive")
    else:
        all_checks_passed = False
        print("    → Follow README.md Step 2 to get credentials.json")
    
    if check_file_exists('token.pickle', "Saved authentication token"):
        print("    ✓ Already authenticated (will reuse token)")
    else:
        print("    ℹ First run will open browser for authentication")
    print()
    
    # Final summary
    print("="*60)
    if all_checks_passed:
        print("  ✓ All checks passed! Ready to run automation.")
        print("\n  Next step: python upload_lesson.py")
    else:
        print("  ✗ Some checks failed. Please fix the issues above.")
        print("\n  See README.md for setup instructions.")
    print("="*60 + "\n")
    
    return 0 if all_checks_passed else 1

if __name__ == "__main__":
    sys.exit(main())

