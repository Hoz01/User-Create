from google.oauth2 import service_account
from googleapiclient.discovery import build
import tkinter as tk
from tkinter import ttk, messagebox

SERVICE_ACCOUNT_FILE = "path/to/your/credentials.json"

ADMIN_EMAIL = "workspaceadmin@yourdomain.com"

SCOPES = ["https://www.googleapis.com/auth/admin.directory.user", "https://www.googleapis.com/auth/apps.licensing"]
DOMAIN = "yourdomain.com"
PRODUCT_ID = "Google-Apps"  # Identifiant du produit Google Workspace
SKU_ID = "1010020026"  # Identifiant de la licence (ex: Business Standard)

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


def create_google_user():
    first_name = entry_first_name.get().strip().lower()
    last_name = entry_last_name.get().strip().lower()
    password = entry_password.get()

    if not all([first_name, last_name, password]):
        messagebox.showerror("Erreur", "Tous les champs doivent être remplis")
        return

    email = f"{first_name[0]}.{last_name}@{DOMAIN}"

    user_info = {
        "name": {"givenName": first_name.capitalize(), "familyName": last_name.capitalize()},
        "password": password,
        "primaryEmail": email,
        "changePasswordAtNextLogin" : True
    }

    try:
        user = service.users().insert(body=user_info).execute()
        messagebox.showinfo("Succès", f"Utilisateur créé: {user['primaryEmail']}")

        # Attribution automatique de la licence après la création de l'utilisateur
        assign_license(email)
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors de la création: {e}")

# Création de la fenêtre principale
root = tk.Tk()
root.title("Création d'utilisateur Google")
root.geometry("350x300")

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

# Bouton pour créer l'utilisateur
btn_create = ttk.Button(root, text="Créer utilisateur", command=create_google_user)
btn_create.pack(pady=10)

# Lancement de la boucle principale
root.mainloop()




