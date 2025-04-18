# 📋 DocxFilesMerger 🏥

## 🌟 Introduction

Welcome to the **DocxFilesMerger** application! 🎉
This web application efficiently and quickly processes ZIP archives containing thousands of medical records in .doc or .docx format.

![Language Badge](https://img.shields.io/badge/Language-Python-blue)
![Framework Badge](https://img.shields.io/badge/Framework-Flask-green)
![Version Badge](https://img.shields.io/badge/Version-1.0.0-orange)

### 📝 Developer

**MOA Digital Agency LLC**  
Website: [https://myoneart.com](https://myoneart.com)  
Contact: [moa@myoneart.com](mailto:moa@myoneart.com)

## 🚀 Main Features

- ✅ **File Extraction**: Automatically extracts all .doc and .docx files from a ZIP archive
- ✅ **Format Conversion**: Converts .doc files to .docx if necessary
- ✅ **Document Merging**: Combines all files into a single document with clear separators
- ✅ **PDF Conversion**: Generates a PDF version of the merged document
- ✅ **Intuitive User Interface**: Simple and responsive web interface for uploading and downloading files

## 🔍 How It Works

1. 📤 **Upload** a ZIP archive containing medical records (.doc/.docx)
2. ⚙️ The system **extracts** all relevant files
3. 🔄 Files are **converted** (if necessary) and **merged** into a single document
4. 📑 A **clear separation** is added before each record: `<FILENAME.extension>...`
5. 📊 The system automatically generates **DOCX and PDF versions** of the final document
6. 📥 **Download** the final documents once processing is complete

## 💻 Technologies Used

- **Backend**: Python, Flask
- **Document Processing**: python-docx, docx2pdf
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap
- **File System**: Temporary file management with zipfile
- **Database**: PostgreSQL (for processing tracking)

## 🚀 Deployment

The application can be deployed on different types of servers:

### Minimum System Requirements
- **CPU**: 2 cores (4 recommended)  
- **RAM**: 2 GB minimum (4 GB recommended)
- **Disk Space**: 20 GB minimum
- **OS**: Linux (Ubuntu 20.04 LTS or newer recommended)

### 🌐 Deployment on cPanel (Domain or Subdomain)

#### Prerequisites
- Hosting with cPanel supporting Python 3.7+ and PostgreSQL
- SSH access (recommended but not mandatory)
- Configured domain or subdomain

#### Step 1: PostgreSQL Database Configuration
1. Log in to your cPanel interface
2. Go to the "Databases" section and click on "PostgreSQL Databases"
3. Create a new database named `docxfilesmerger_db`
4. Create a new user with a secure password (e.g., `docxuser`)
   - Use a password generator to create a strong password
   - **IMPORTANT**: Note these credentials, you'll need them later
5. Associate the user with the database with all privileges

#### Step 2: Python Environment Setup
1. In cPanel, go to "Setup Python App"
2. Create a new application with the following settings:
   - **Python version**: 3.9 or newer
   - **Application root**: `/docxfilesmerger` or desired path
   - **Application URL**: Your domain or subdomain (e.g., `docxfilesmerger.yourdomain.com`)
   - **Application startup file**: `main.py`
   - **Application Entry point**: `app`
3. Click "Create" to create the Python environment

#### Step 3: Download and Configure Files
1. Upload the application via cPanel File Manager:
   - Access the application folder created in the previous step
   - Upload all application files (.py, templates/, static/, etc.)

2. Create a `.env` file at the root of the project:
   ```
   DATABASE_URL=postgresql://docxuser:your_password@localhost:5432/docxfilesmerger_db
   FLASK_SECRET_KEY=a_very_long_random_secure_string
   UPLOAD_FOLDER=/home/username/docxfilesmerger/uploads
   OUTPUT_FOLDER=/home/username/docxfilesmerger/outputs
   STATUS_FOLDER=/home/username/docxfilesmerger/status
   ```
   Replace `username` with your cPanel username and `your_password` with the PostgreSQL password.

3. Create a `requirements.txt` file containing:
   ```
   flask==2.0.1
   flask-sqlalchemy==3.0.0
   psycopg2-binary==2.9.1
   python-docx==0.8.11
   docx2pdf==0.1.8
   PyPDF2==2.10.5
   reportlab==3.6.1
   gunicorn==20.1.0
   python-dotenv==0.19.0
   ```

4. Create or modify the `.htaccess` file at the root of your application:
   ```
   RewriteEngine On
   RewriteCond %{REQUEST_FILENAME} !-f
   RewriteRule ^(.*)$ /main.py [QSA,L]
   
   <Files ~ "\.(py|env)$">
       Order allow,deny
       Deny from all
   </Files>
   
   <Files main.py>
       SetHandler wsgi-script
       Options +ExecCGI
   </Files>
   
   # Increase maximum upload size
   php_value upload_max_filesize 300M
   php_value post_max_size 300M
   ```

#### Step 4: Install Dependencies
1. In cPanel, go back to "Setup Python App"
2. Select your application
3. Click on the "Install Python Modules" or "PIP Install" tab
4. Select "From requirements.txt" and click "Install Packages"

#### Step 5: Upload Folder Configuration
1. Via cPanel File Manager, create the following folders:
   - `uploads/` - For uploaded ZIP files
   - `outputs/` - For processed files
   - `status/` - For status files
2. Set permissions to 755 for these folders:
   ```bash
   chmod 755 uploads outputs status
   ```

#### Step 6: Database Configuration and First Start
1. Access your application via SSH if available:
   ```bash
   cd ~/docxfilesmerger
   source venv/bin/activate  # Path may vary depending on your cPanel configuration
   python
   ```
2. Run the following Python commands:
   ```python
   from app import app, db
   with app.app_context():
       db.create_all()
       exit()
   ```

3. Restart the Python application from cPanel

#### Step 7: CRON Tasks Configuration for Cleanup
1. In cPanel, go to "Cron Jobs"
2. Create a new cron task that runs daily:
   ```
   0 3 * * * cd ~/docxfilesmerger && /usr/local/bin/python3 -c "from utils import cleanup_old_files; cleanup_old_files('uploads', 24); cleanup_old_files('outputs', 24); cleanup_old_files('status', 24)"
   ```

#### Common Troubleshooting:
- **500 Error**: Check Apache error logs in cPanel
- **Database connection issues**: Verify connection information in `.env`
- **Files not found**: Check permissions of `uploads`, `outputs`, and `status` folders
- **PDF conversion fails**: Install LibreOffice via SSH or contact your hosting provider

### Detailed Documentation

For complete deployment instructions, see our detailed documentation available at [moa@myoneart.com](mailto:moa@myoneart.com).

## 🛠️ Keyboard Shortcuts

| Shortcut | Action |
|-----------|--------|
| <kbd>Ctrl</kbd> + <kbd>O</kbd> | Open file selector |
| <kbd>Esc</kbd> | Cancel current operation |
| <kbd>Ctrl</kbd> + <kbd>D</kbd> | Download DOCX document |
| <kbd>Ctrl</kbd> + <kbd>P</kbd> | Download PDF document |
| <kbd>Ctrl</kbd> + <kbd>R</kbd> | Reset application |
| <kbd>Ctrl</kbd> + <kbd>H</kbd> | Display shortcuts help |

## 📋 Prerequisites

- Python 3.7+
- Python libraries: flask, python-docx, docx2pdf, etc.
- Modern web browser (Chrome, Firefox, Safari, Edge)

## ⚠️ Important Notes

- 🔒 **Privacy**: This application processes files locally and does not send them to external servers
- 📦 **Maximum Size**: The application has been tested with archives containing more than 5,000 files
- ⏱️ **Processing Time**: Processing can take several minutes for large archives
- 🧹 **Automatic Cleanup**: Temporary files are automatically deleted after 24 hours

## 🔧 Troubleshooting

| Problem | Solution |
|----------|----------|
| ZIP archive not accepted | Make sure the file is in ZIP format (not RAR or 7z) |
| Extraction error | Make sure the archive is not corrupted |
| PDF conversion fails | Install LibreOffice to improve PDF conversion |
| Missing files | Only .doc and .docx files are processed, other formats are ignored |

## 📞 Support

For any questions or issues, feel free to:
- 📧 Contact support: [moa@myoneart.com](mailto:moa@myoneart.com)
- 🌐 Visit our website: [https://myoneart.com](https://myoneart.com)

## 📜 License

This project is developed by MOA Digital Agency LLC. All rights reserved © 2025.