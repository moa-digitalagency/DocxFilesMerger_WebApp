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

## 📄 cPanel Deployment

To deploy the application on a cPanel server:

1. Create a Python application in cPanel
2. Upload your application files to the server
3. Set up a virtual environment and install dependencies
4. Configure your database connection in the `.env` file
5. Set up a Passenger WSGI file to run the Flask application
6. Set appropriate file permissions

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