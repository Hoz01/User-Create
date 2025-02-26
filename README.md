# Google User Creation with Tkinter Interface

## Description
This program allows automatic creation of Google Workspace users through a **Tkinter** graphical interface. It generates an email in the format `firstletteroffirstname.lastname@mydomain.com`, assigns a Google Workspace license, and forces the user to set a new password on first login.

## Features
- User-friendly interface with **Tkinter & TTK**.
- Creation of Google Workspace users via the **Admin SDK**.
- Automatic assignment of a **Google Workspace license**.
- Enforces password change on first login.

## Prerequisites
### 🔹 Google Cloud Configuration
1. **Enable the Admin SDK API and Licensing API**
   - Go to **[Google Cloud Console](https://console.cloud.google.com/)**.
   - Enable **Google Admin SDK API** and **Google Workspace License Manager API**.

2. **Create a service account and obtain the JSON key**
   - Go to **API & Services > Credentials**.
   - Create a **service account** and download the **JSON** file.
   - Ensure the service account has **domain-wide delegation**.
   - Add these **API scopes**:
     ```
     https://www.googleapis.com/auth/admin.directory.user
     https://www.googleapis.com/auth/apps.licensing
     ```

3. **Modify script settings**
   - Replace `path/to/your/service-account.json` with **your JSON file path**.
   - Update `ADMIN_EMAIL` with a **super administrator email**.
   - Set `DOMAIN` with your custom domain.
   - Replace `PRODUCT_ID` and `SKU_ID` with correct values for your Google Workspace subscription.

## Installation
1. **Install Python (if not installed)**
   - Download Python from **[python.org](https://www.python.org/downloads/)**.
   - Ensure Python is added to your **PATH**.

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the program**
   ```bash
   python main.py
   ```

## Dependencies
The `requirements.txt` file includes:
```txt
google-auth==2.22.0
google-auth-oauthlib==1.0.0
google-auth-httplib2==0.1.0
google-api-python-client==2.97.0
tkinter
```

## Usage
1. **Launch the application**: Fill in the **First Name, Last Name, and Password** fields.
2. **Click "Create User"**:
   - The user is created in Google Workspace.
   - A license is automatically assigned.
   - On first login, the user must change their password.

## Common Issues
### ❌ **Error `TclError: Can't find a usable init.tcl`**
- Solution: Reinstall **Python with Tcl/Tk included**.
- Test: Run `python -m tkinter` to verify the installation.

### ❌ **Error `403 Forbidden` when creating a user**
- Ensure the service account has administrative permissions.
- Check that **domain-wide delegation** is enabled.

## Possible Improvements
- Add **email and password validation**.
- Connect to a **database** to store created users.
- Improve error handling with **detailed logs**.

## Auteur
👤 **Hoz01**  
📧 Discord :  Hoz01#4051

