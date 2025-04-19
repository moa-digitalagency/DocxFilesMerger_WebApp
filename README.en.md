# 📋 DocxFilesMerger 🏥

*[Version française disponible ici](README.md)*

## Medical Document Processing Application

Developed by MOA Digital Agency LLC (https://myoneart.com)  
Email: moa@myoneart.com  
Copyright © 2025 MOA Digital Agency LLC. Developed by Aisance Kalonji. All rights reserved.

## 📋 Overview

DocxFilesMerger is a specialized web application designed to process, merge, and convert medical records contained in ZIP archives. The application provides a user-friendly interface for:

- Uploading ZIP files containing .doc or .docx medical records
- Extracting and merging all files into a single document
- Converting the merged document to PDF
- Downloading both the merged DOCX and PDF files

## ✨ Features

- 📤 Drag-and-drop interface for easy file uploading
- 📊 Real-time processing progress with percentage display
- 🔄 Background processing for large files (5,000+ documents)
- 📈 Administrator interface with usage statistics
- 🌐 Multi-language support (English, French)
- 🔐 Secure processing with temporary file management
- 🔍 Detailed processing logs and error handling
- 🖥️ Responsive, mobile-friendly design

## 📦 Technologies Used

- **Backend**: Python, Flask, SQLAlchemy
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap
- **File Processing**: python-docx, docx2pdf, reportlab
- **Database**: PostgreSQL

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- PostgreSQL database

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/myoneart/docxfilesmerger.git
   cd docxfilesmerger
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file based on `.env.example` and configure your environment variables.

5. Initialize the database:
   ```
   flask db upgrade
   ```

6. Start the application:
   ```
   python main.py
   ```

7. Access the application at `http://localhost:5000`

## 📋 Usage

1. **Upload a ZIP file**: Drag and drop your ZIP file containing .doc or .docx files onto the upload area, or click "Browse files" to select a file from your computer.

2. **Process the file**: Once uploaded, the application will automatically begin processing the file. You'll see a progress bar and percentage indicating the status of the operation.

3. **Download results**: When processing is complete, you can download both the merged DOCX file and the PDF version using the provided buttons.

## ⌨️ Keyboard Shortcuts

- `Ctrl+U`: Open file browser for uploading
- `Ctrl+D`: Download merged DOCX (when available)
- `Ctrl+P`: Download PDF (when available)
- `Ctrl+R`: Restart the application (clear current files)
- `Ctrl+H`: Display help with shortcuts

## 🔑 Administration

The application includes an admin panel that provides:

- Total usage statistics
- Recent processing jobs
- Daily statistics
- Configuration settings

To access the admin panel:
1. Click on the "Admin" link in the navigation bar
2. Enter your administrator credentials (set in the `.env` file)

## 📄 cPanel Deployment (Advanced Method)

### ⚠️ Important cPanel Considerations
cPanel does not natively support Python applications like Flask. The method described below uses advanced techniques to work around these limitations:

### Prerequisites
- cPanel hosting that allows Python installation (via "Setup Python App" or manually)
- SSH access (strongly recommended)
- Configured domain or subdomain
- At least an intermediate or professional level hosting plan

### Step 1: PostgreSQL Database Configuration
1. Log in to your cPanel interface
2. Navigate to "Databases" → "PostgreSQL Databases"
3. Create a new database (e.g., `docxfilesmerger_db`)
4. Create a new user with a secure password
   - **IMPORTANT**: Keep these credentials safe
5. Associate the user with the database with all privileges

### Step 2: Python Installation via cPanel (Method 1 - Preferred)
If your cPanel offers the "Setup Python App" option:
1. Access this section and create a new application
2. Select Python 3.9+ and configure application paths
3. Note the created virtual environment path

### Step 2 (Alternative): Manual Python Installation (Method 2)
If "Setup Python App" is not available:
1. Connect via SSH:
   ```bash
   ssh username@yourhosting.com
   ```
2. Install Python locally:
   ```bash
   cd ~
   mkdir -p python/pythonvenv
   curl -O https://www.python.org/ftp/python/3.9.9/Python-3.9.9.tgz
   tar xzf Python-3.9.9.tgz
   cd Python-3.9.9
   ./configure --prefix=$HOME/python --enable-optimizations
   make
   make install
   cd ~/python
   ~/python/bin/python3 -m venv pythonvenv
   ```
3. Verify the installation:
   ```bash
   ~/python/pythonvenv/bin/python --version
   ```

### Step 3: Project Configuration
1. Download the application files to your public_html folder or a subfolder:
   ```bash
   cd ~/public_html/subdomain  # Or your desired folder
   git clone https://github.com/yourrepository/docxfilesmerger.git .  # If Git is available
   # OR manually upload via the cPanel File Manager
   ```

2. Create a `.env` file at the project root:
   ```
   DATABASE_URL=postgresql://username:password@localhost:5432/docxfilesmerger_db
   FLASK_SECRET_KEY=a_very_long_and_random_secret_key
   ADMIN_USERNAME=choose_an_admin_name
   ADMIN_PASSWORD=secure_admin_password
   UPLOAD_FOLDER=/home/username/public_html/subdomain/uploads
   OUTPUT_FOLDER=/home/username/public_html/subdomain/outputs
   STATUS_FOLDER=/home/username/public_html/subdomain/status
   ```
   Replace `username`, `password`, etc. with your actual values.

3. Create the necessary folders:
   ```bash
   mkdir -p uploads outputs status
   chmod 755 uploads outputs status
   ```

### Step 4: Installing Dependencies
1. Activate the Python environment and install dependencies:
   ```bash
   # For installation via Setup Python App (Method 1)
   source ~/virtualenv/pythonX.X/bin/activate  # Exact path depends on your cPanel configuration
   
   # OR for manual installation (Method 2)
   source ~/python/pythonvenv/bin/activate
   
   # Then install dependencies
   pip install flask flask-sqlalchemy psycopg2-binary python-docx docx2pdf PyPDF2 reportlab gunicorn python-dotenv flask-login
   ```

### Step 5: WSGI Server Configuration
Since cPanel has no native support for Python WSGI, we'll use a hybrid approach:

1. Create a `passenger_wsgi.py` file:
   ```python
   import os
   import sys
   
   # Path to your Python environment
   PYTHON_PATH = '/home/username/python/pythonvenv/bin/python'  # Method 2
   # OR
   # PYTHON_PATH = '/home/username/virtualenv/pythonX.X/bin/python'  # Method 1
   
   # Path to the application folder
   APP_PATH = '/home/username/public_html/subdomain'
   
   # Add the application path to the system
   sys.path.insert(0, APP_PATH)
   
   # Set the Python environment variable
   os.environ['PYTHONHOME'] = PYTHON_PATH.replace('/bin/python', '')
   
   # Application function for Passenger
   def application(environ, start_response):
       # Run the Flask WSGI application
       from main import app as flask_app
       return flask_app(environ, start_response)
   ```
   Replace `username` and paths with your actual values.

2. Create an `.htaccess` file:
   ```apache
   PassengerEnabled On
   PassengerPython /home/username/python/pythonvenv/bin/python  # Method 2
   # OR
   # PassengerPython /home/username/virtualenv/pythonX.X/bin/python  # Method 1
   
   <Files ~ "\.(py|env)$">
       Order allow,deny
       Deny from all
   </Files>
   
   <Files passenger_wsgi.py>
       Order allow,deny
       Allow from all
   </Files>
   
   # Increase maximum upload size
   php_value upload_max_filesize 300M
   php_value post_max_size 300M
   
   # Protection for sensitive folders
   <DirectoryMatch "^/.*/\.(git|env)/">
       Require all denied
   </DirectoryMatch>
   ```

### Step 6: Database Initialization
1. Via SSH, run Python to initialize the database:
   ```bash
   cd ~/public_html/subdomain
   # Activate the appropriate virtual environment based on the method used
   
   python -c "from app import app, db; with app.app_context(): db.create_all()"
   ```

### Step 7: Deployment Configuration Without Passenger (alternative)
If Passenger is not available, use a CGI script:

1. Create a `cgi-bin/app.cgi` file:
   ```python
   #!/home/username/python/pythonvenv/bin/python
   import os
   import sys
   
   # Adjust the path to your application
   sys.path.insert(0, '/home/username/public_html/subdomain')
   
   # Load environment variables
   from dotenv import load_dotenv
   load_dotenv('/home/username/public_html/subdomain/.env')
   
   # Run the application
   from wsgiref.handlers import CGIHandler
   from main import app
   
   CGIHandler().run(app)
   ```
   
2. Make the script executable:
   ```bash
   chmod +x cgi-bin/app.cgi
   ```

3. Create a special `.htaccess` for CGI redirection:
   ```apache
   RewriteEngine On
   RewriteCond %{REQUEST_FILENAME} !-f
   RewriteRule ^(.*)$ /cgi-bin/app.cgi/$1 [QSA,L]
   ```

### Step 8: CRON Task for Maintenance
1. In cPanel, go to "Cron Jobs"
2. Create a daily task:
   ```
   0 3 * * * cd /home/username/public_html/subdomain && /home/username/python/pythonvenv/bin/python -c "from utils import cleanup_old_files; cleanup_old_files('uploads', 24); cleanup_old_files('outputs', 24); cleanup_old_files('status', 24)"
   ```

### Common Troubleshooting
- **500 Error**: Check Apache error logs in cPanel → "Error Log"
- **Python path issues**: Verify all paths in `passenger_wsgi.py` and `.htaccess` match your environment
- **Missing dependencies**: Install necessary system libraries (contact hosting support)
- **Permissions**: Make sure uploads/outputs/status folders have 755 permissions
- **Database inaccessible**: Check PostgreSQL configuration in your hosting

### Notes on cPanel Limitations
- cPanel is not optimized for Python applications; expect some technical challenges
- Deployment may require assistance from hosting support for certain configurations
- Some hosts impose resource limits that can affect performance
- For an optimal experience, consider specialized platforms for Python (PythonAnywhere, Heroku, DigitalOcean, etc.)

## 🔧 Troubleshooting

- **File upload issues**: Ensure your ZIP file is not corrupted and contains valid .doc or .docx files.
- **Processing errors**: Check the application logs for detailed error information.
- **Database connection issues**: Verify your database credentials in the `.env` file.

## 📝 License

This project is proprietary software owned by MOA Digital Agency LLC. All rights reserved.

## 🤝 Contact

For support, feature requests, or inquiries, please contact:

- Email: moa@myoneart.com
- Website: https://myoneart.com