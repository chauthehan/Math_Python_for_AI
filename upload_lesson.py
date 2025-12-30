import os
import csv
import shutil
import hashlib
import json
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import pickle
import re

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.file']
STATE_FILE = '.upload_state.json'


def load_upload_state():
    """Return persisted upload hashes so we only re-upload changed files."""
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            # Corrupt state file, start fresh
            return {}
    return {}


def save_upload_state(state):
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=2)


def compute_file_hash(path):
    """Hash file contents to detect changes."""
    digest = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            digest.update(chunk)
    return digest.hexdigest()

class GoogleDriveAutomation:
    def __init__(self):
        self.service = None
        self.authenticate()
        
    def authenticate(self):
        """Authenticate with Google Drive API"""
        creds = None
        # The file token.pickle stores the user's access and refresh tokens
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        
        # If there are no (valid) credentials available, let the user log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        
        self.service = build('drive', 'v3', credentials=creds)
        print("✓ Successfully authenticated with Google Drive")
    
    def _find_folder(self, folder_name, parent_id=None):
        """Return folder id if a folder with this name exists under parent."""
        parent_filter = f" and '{parent_id}' in parents" if parent_id else ""
        query = (
            f"name = '{folder_name}' and "
            f"mimeType = 'application/vnd.google-apps.folder' and trashed = false"
            f"{parent_filter}"
        )
        results = self.service.files().list(q=query, spaces='drive', fields="files(id, name)").execute()
        files = results.get('files', [])
        if files:
            return files[0].get('id')
        return None
    
    def get_or_create_folder(self, folder_name, parent_id=None):
        """Find existing folder (by name under parent) or create it."""
        existing_id = self._find_folder(folder_name, parent_id)
        if existing_id:
            print(f"  Reusing folder: {folder_name} (ID: {existing_id})")
            return existing_id
        
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        
        if parent_id:
            file_metadata['parents'] = [parent_id]
        
        folder = self.service.files().create(
            body=file_metadata,
            fields='id, name'
        ).execute()
        
        print(f"  Created folder: {folder_name} (ID: {folder.get('id')})")
        return folder.get('id')
    
    def upload_file(self, file_path, parent_id=None, new_name=None):
        """Upload a file to Google Drive as a Colab notebook"""
        file_name = new_name if new_name else os.path.basename(file_path)
        
        file_metadata = {
            'name': file_name
        }
        
        if parent_id:
            file_metadata['parents'] = [parent_id]
        
        # For .ipynb files, set MIME type to Google Colab format
        # This makes them open directly in Google Colab
        if file_path.endswith('.ipynb'):
            file_metadata['mimeType'] = 'application/vnd.google.colaboratory'
            source_mime_type = 'application/x-ipynb+json'
        else:
            source_mime_type = 'application/octet-stream'
        
        media = MediaFileUpload(file_path, mimetype=source_mime_type, resumable=True)
        
        # Check if file already exists in parent with same name
        parent_filter = f" and '{parent_id}' in parents" if parent_id else ""
        query = (
            f"name = '{file_name}' and "
            f"mimeType != 'application/vnd.google-apps.folder' and trashed = false"
            f"{parent_filter}"
        )
        results = self.service.files().list(q=query, spaces='drive', fields="files(id, name)").execute()
        files = results.get('files', [])
        
        if files:
            file_id = files[0].get('id')
            # When updating, we cannot include 'parents' in the body
            # Create a new metadata dict without 'parents' field
            update_metadata = {
                'name': file_metadata['name']
            }
            if 'mimeType' in file_metadata:
                update_metadata['mimeType'] = file_metadata['mimeType']
            
            file = self.service.files().update(
                fileId=file_id,
                body=update_metadata,
                media_body=media,
                fields='id, name'
            ).execute()
            print(f"    Updated existing file: {file_name}")
        else:
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id, name'
            ).execute()
            print(f"    Uploaded new file: {file_name}")
        
        return file.get('id')
    
    def share_file_with_user(self, file_id, email, role='writer'):
        """Share a file with a specific user"""
        permission = {
            'type': 'user',
            'role': role,
            'emailAddress': email
        }
        
        try:
            self.service.permissions().create(
                fileId=file_id,
                body=permission,
                sendNotificationEmail=False
            ).execute()
            return True
        except Exception as e:
            print(f"    Warning: Could not share with {email}: {str(e)}")
            return False

def parse_class_name_from_filename(filename):
    """Extract a clean class name from the CSV filename"""
    # Remove the file extension and common suffixes
    name = filename.replace('.csv', '')
    return name

def read_class_information(csv_file_path):
    """Read student information from CSV file"""
    students = []
    
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        
        for row in csv_reader:
            student_name = row.get('Họ và tên học sinh', '').strip()
            student_email = row.get('Email sử dụng để học tập  (email riêng hoặc email của phụ huynh nếu chưa có)', '').strip()
            
            # Skip empty rows
            if student_name and student_email:
                students.append({
                    'name': student_name,
                    'email': student_email
                })
    
    return students

def get_first_name(full_name):
    """Extract first name from full Vietnamese name"""
    # In Vietnamese names, the last word is typically the first name
    parts = full_name.strip().split()
    if parts:
        return parts[-1]
    return full_name

def main():
    print("\n" + "="*60)
    print("  Google Drive Lesson Automation System")
    print("="*60 + "\n")
    
    upload_state = load_upload_state()
    bootstrap_state_only = os.getenv("BOOTSTRAP_STATE_ONLY", "").lower() in ("1", "true", "yes")
    
    # Initialize Google Drive API unless we are only bootstrapping the state file
    drive = None if bootstrap_state_only else GoogleDriveAutomation()
    
    # Define paths
    class_info_dir = '/Users/han.ct/Documents/math_python_for_AI/class_information'
    lessons_dir = '/Users/han.ct/Documents/math_python_for_AI/lessons/module_1'
    
    if bootstrap_state_only:
        print("\n[1] Bootstrapping upload state without uploading...")
        parent_folder_id = None
    else:
        # Create or reuse parent folder: Math_python_for_AI
        print("\n[1] Ensuring parent folder structure...")
        parent_folder_id = drive.get_or_create_folder('Math_python_for_AI')
    
    # Get all CSV files in class_information directory
    csv_files = [f for f in os.listdir(class_info_dir) if f.endswith('.csv')]
    
    print(f"\n[2] Found {len(csv_files)} class(es) to process\n")
    
    # Get all lesson folders
    lesson_folders = sorted([d for d in os.listdir(lessons_dir) 
                            if os.path.isdir(os.path.join(lessons_dir, d)) 
                            and d.startswith('lesson_')])
    
    print(f"[3] Found {len(lesson_folders)} lesson(s) to upload\n")
    
    # Process each class
    for csv_file in csv_files:
        csv_path = os.path.join(class_info_dir, csv_file)
        class_name = parse_class_name_from_filename(csv_file)
        
        print(f"\n{'='*60}")
        print(f"Processing Class: {class_name}")
        print(f"{'='*60}\n")
        
        # Read student information
        students = read_class_information(csv_path)
        print(f"  Found {len(students)} student(s) in this class")
        for i, student in enumerate(students, 1):
            print(f"    {i}. {student['name']} ({student['email']})")
        
        # Create class folder
        if bootstrap_state_only:
            class_folder_id = None
            print(f"\n  Recording class: {class_name}")
        else:
            print(f"\n  Ensuring class folder: {class_name}")
            class_folder_id = drive.get_or_create_folder(class_name, parent_folder_id)
        
        # Process each lesson
        for lesson_folder in lesson_folders:
            lesson_path = os.path.join(lessons_dir, lesson_folder)
            lesson_number = lesson_folder.split('_')[1]  # Extract number from lesson_X
            lesson_name = f"lesson_{lesson_number}"
            
            print(f"\n  Processing {lesson_name}...")
            
            # Create lesson folder in Google Drive
            lesson_folder_id = None if bootstrap_state_only else drive.get_or_create_folder(lesson_name, class_folder_id)
            
            # Find the notebook file in this lesson folder
            notebook_file = None
            for file in os.listdir(lesson_path):
                if file.endswith('.ipynb'):
                    notebook_file = os.path.join(lesson_path, file)
                    break
            
            if notebook_file:
                source_hash = compute_file_hash(notebook_file)
                # Upload original lesson file as Google Colab notebook
                original_filename = f"Lesson_{lesson_number}.ipynb"
                original_key = f"{class_name}/{lesson_name}/{original_filename}"
                if upload_state.get(original_key) != source_hash:
                    if bootstrap_state_only:
                        print(f"    Recording original: {original_filename}")
                        upload_state[original_key] = source_hash
                    else:
                        print(f"    Uploading original: {original_filename} (as Colab notebook)")
                        drive.upload_file(notebook_file, lesson_folder_id, original_filename)
                        upload_state[original_key] = source_hash
                else:
                    print(f"    Skipping unchanged original: {original_filename}")
                
                # Create personalized copies for each student as Colab notebooks
                print(f"    Creating personalized Colab notebooks:")
                for student in students:
                    first_name = get_first_name(student['name'])
                    student_filename = f"{first_name}.ipynb"
                    
                    student_key = f"{class_name}/{lesson_name}/{student_filename}"
                    if upload_state.get(student_key) != source_hash:
                        if bootstrap_state_only:
                            print(f"      - Recording {student_filename} for {student['name']}")
                            upload_state[student_key] = source_hash
                        else:
                            print(f"      - Uploading {student_filename} for {student['name']}")
                            file_id = drive.upload_file(notebook_file, lesson_folder_id, student_filename)
                            upload_state[student_key] = source_hash
                            # Share the file with the student
                            drive.share_file_with_user(file_id, student['email'], role='writer')
                    else:
                        print(f"      - Skipping unchanged notebook for {student['name']}")
            else:
                print(f"    Warning: No notebook file found in {lesson_folder}")
    
    save_upload_state(upload_state)
    
    if bootstrap_state_only:
        print("\nBootstrap complete. State saved to .upload_state.json. No files were uploaded.\n")
        return
    
    print("\n" + "="*60)
    print("  ✓ Automation completed successfully!")
    print("="*60 + "\n")
    print("Summary:")
    print(f"  - Processed {len(csv_files)} class(es)")
    print(f"  - Created {len(lesson_folders)} lesson folder(s) per class")
    print(f"  - Generated personalized Colab notebooks for all students")
    print(f"  - Set up sharing permissions automatically")
    print(f"  - All .ipynb files will open in Google Colab")
    print("\nCheck your Google Drive for the 'Math_python_for_AI' folder!")
    print("Students can click on their files to open them directly in Colab!\n")

if __name__ == "__main__":
    main()
