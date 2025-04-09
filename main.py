from google.oauth2 import service_account
from googleapiclient.discovery import build
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv

SERVICE_ACCOUNT_FILE = "path/to/your/credentials.json"
ADMIN_EMAIL = "workspaceadmin@yourdomain.com"
SCOPES = ["https://www.googleapis.com/auth/admin.directory.user", "https://www.googleapis.com/auth/apps.licensing"]
DOMAIN = "yourdomain.com"
PRODUCT_ID = "Google-Apps"
SKU_ID = "1010020026"

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

delegated_credentials = credentials.with_subject(ADMIN_EMAIL)

service = build("admin", "directory_v1", credentials=delegated_credentials)
license_service = build("licensing", "v1", credentials=delegated_credentials)

def assign_license(user_email):
    try:
        license_service.licenseAssignments().insert(
            productId=PRODUCT_ID,
            skuId=SKU_ID,
            body={"userId": user_email}
        ).execute()
        messagebox.showinfo("Licence attribuée", f"Licence attribuée à {user_email}")
    except Exception as e:
        messagebox.showerror("Erreur Licence", f"Erreur lors de l’attribution de la licence : {e}")

def create_google_user(first_name, last_name, password):
    email = f"{first_name[0]}.{last_name}@{DOMAIN}"

    user_info = {
        "name": {"givenName": first_name.capitalize(), "familyName": last_name.capitalize()},
        "password": password,
        "primaryEmail": email,
        "changePasswordAtNextLogin": True
    }

    try:
        user = service.users().insert(body=user_info).execute()
        messagebox.showinfo("Succès", f"Utilisateur créé: {user['primaryEmail']}")
        assign_license(email)
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors de la création: {e}")

def create_single_user():
    first_name = entry_first_name.get().strip().lower()
    last_name = entry_last_name.get().strip().lower()
    password = entry_password.get()

    if not all([first_name, last_name, password]):
        messagebox.showerror("Erreur", "Tous les champs doivent être remplis")
        return

    create_google_user(first_name, last_name, password)

def import_users_from_csv():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if not file_path:
        return

    try:
        with open(file_path, mode='r', newline='') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                create_google_user(row['first_name'].lower(), row['last_name'].lower(), row['password'])
        messagebox.showinfo("Succès", "Utilisateurs importés avec succès")
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors de l'importation du CSV: {e}")

# Création de la fenêtre principale
root = tk.Tk()
root.title("Création d'utilisateur Google")
root.geometry("350x350")

# Labels et champs de saisie
label_first_name = ttk.Label(root, text="Prénom")
label_first_name.pack()
entry_first_name = ttk.Entry(root)
entry_first_name.pack()

label_last_name = ttk.Label(root, text="Nom")
label_last_name.pack()
entry_last_name = ttk.Entry(root)
entry_last_name.pack()

label_password = ttk.Label(root, text="Mot de passe")
label_password.pack()
entry_password = ttk.Entry(root, show="*")
entry_password.pack()

# Bouton pour créer un utilisateur unique
btn_create_single = ttk.Button(root, text="Créer utilisateur unique", command=create_single_user)
btn_create_single.pack(pady=10)

# Bouton pour importer des utilisateurs à partir d'un CSV
btn_import_csv = ttk.Button(root, text="Importer CSV", command=import_users_from_csv)
btn_import_csv.pack(pady=10)

# Lancement de la boucle principale
root.mainloop()
