
# OpaleMergeFlaskAzureApp

## Brief Description
**OpaleMergeFlaskAzureApp** is a versatile web application designed for *merging CSV files* using Flask, optimized for deployment on Azure. This tool simplifies data handling by allowing users to **upload, process, and merge** various CSV files into a unified format, making it ideal for data analysts and anyone managing large datasets.

### Features
- **CSV File Upload**: Allows users to upload multiple CSV files for processing.
- **Column Management**: Automatically detects and manages different column structures such as 'initials_name' and 'patient_number'.
- **Column Prefixing**: Automatically adds prefixes to column names based on the order of the files, facilitating identification after merging.
- **CSV File Merging**: Merges multiple uploaded CSV files into one consolidated file.
- **Merged File Download**: Users can download the merged CSV file directly from the web interface.

### Installation
To install this project locally, follow these steps:

1. *Clone the repository*:
   ```bash
   git clone https://github.com/IDMDataHub/OpaleMergeFlaskAzureApp.git
   ```
2. *Install the required dependencies*:
   ```bash
   pip install -r requirements.txt
   ```

### Usage
To run the Flask application:
```bash
python app.py
```
Access the web application via `localhost:5000` in your web browser.

### Endpoints
- **Home (`/`)**: Landing page for uploading files.
- **Upload (`/upload`)**: Access point for uploading and processing CSV files.
- **Download (`/download`)**: Access point to download the merged CSV file.

### Libraries Used
- `pandas`: For DataFrame manipulation.
- `Flask`: Web framework to handle HTTP requests and template rendering.
- `os`, `io`: Utilities for file operations and input/output.

### Contribution
Contributions are welcome! For major changes, please open an issue first to discuss what you would like to change.

### License
This project is licensed under the [MIT License](https://choosealicense.com/licenses/mit/).

### Author
*Maxime Jacoupy*
