import sys
import csv
from google.oauth2 import service_account
from googleapiclient.discovery import build
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QFileDialog,
    QMessageBox,
    QFrame,
    QStyleFactory,
    QGraphicsDropShadowEffect,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

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
        QMessageBox.information(None, "Licence attribuée", f"Licence attribuée à {user_email}")
    except Exception as e:
        QMessageBox.critical(None, "Erreur Licence", f"Erreur lors de l’attribution de la licence : {e}")

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
        QMessageBox.information(None, "Succès", f"Utilisateur créé: {user['primaryEmail']}")
        assign_license(email)
    except Exception as e:
        QMessageBox.critical(None, "Erreur", f"Erreur lors de la création: {e}")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Création d'utilisateur Google")

        # Global, modern stylesheet (dark theme, rounded corners, smooth hover states)
        self.setStyleSheet(
            """
            QWidget { background-color: #111318; color: #E6E8EA; font-family: 'Segoe UI', Arial, sans-serif; font-size: 12pt; }
            QLabel { color: #AAB2BD; font-size: 10pt; }
            QLineEdit {
                background: #1A1D24; border: 1px solid #2A2F3A; padding: 10px 12px; border-radius: 8px; color: #E6E8EA;
            }
            QLineEdit:focus { border: 1px solid #3D7EFF; background: #20242C; }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #2B61FF, stop:1 #7A35FF);
                border: none; color: white; padding: 10px 14px; border-radius: 8px; font-weight: 600;
            }
            QPushButton:hover { filter: brightness(1.05); }
            QPushButton:pressed { filter: brightness(0.95); }
            QFrame#card { background: #0F1218; border: 1px solid #222835; border-radius: 14px; }
            """
        )

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        outer = QHBoxLayout(central_widget)
        outer.setContentsMargins(24, 24, 24, 24)
        outer.setSpacing(0)

        card = QFrame(self)
        card.setObjectName("card")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(24, 24, 24, 24)
        card_layout.setSpacing(14)

        title = QLabel("Création d'utilisateur Google", self)
        title.setStyleSheet("font-size: 16pt; font-weight: 700; color: #EDEFF2;")
        card_layout.addWidget(title)

        self.label_first_name = QLabel("Prénom", self)
        card_layout.addWidget(self.label_first_name)
        self.entry_first_name = QLineEdit(self)
        self.entry_first_name.setPlaceholderText("Entrez le prénom")
        card_layout.addWidget(self.entry_first_name)

        self.label_last_name = QLabel("Nom", self)
        card_layout.addWidget(self.label_last_name)
        self.entry_last_name = QLineEdit(self)
        self.entry_last_name.setPlaceholderText("Entrez le nom")
        card_layout.addWidget(self.entry_last_name)

        self.label_password = QLabel("Mot de passe", self)
        card_layout.addWidget(self.label_password)
        self.entry_password = QLineEdit(self)
        self.entry_password.setPlaceholderText("Définissez un mot de passe temporaire")
        self.entry_password.setEchoMode(QLineEdit.Password)
        card_layout.addWidget(self.entry_password)

        self.btn_create_single = QPushButton("Créer utilisateur unique", self)
        self.btn_create_single.clicked.connect(self.create_single_user)
        card_layout.addWidget(self.btn_create_single)

        self.btn_import_csv = QPushButton("Importer CSV", self)
        self.btn_import_csv.clicked.connect(self.import_users_from_csv)
        card_layout.addWidget(self.btn_import_csv)

        # Soft shadow for the card
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(24)
        shadow.setXOffset(0)
        shadow.setYOffset(8)
        shadow.setColor(QColor(0, 0, 0, 160))
        card.setGraphicsEffect(shadow)

        outer.addStretch(1)
        outer.addWidget(card, 0)
        outer.addStretch(1)

        self.setMinimumSize(520, 480)

    def create_single_user(self):
        first_name = self.entry_first_name.text().strip().lower()
        last_name = self.entry_last_name.text().strip().lower()
        password = self.entry_password.text()

        if not all([first_name, last_name, password]):
            QMessageBox.critical(self, "Erreur", "Tous les champs doivent être remplis")
            return

        create_google_user(first_name, last_name, password)

    def import_users_from_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Sélectionner un fichier CSV", "", "CSV files (*.csv)")
        if not file_path:
            return

        try:
            with open(file_path, mode='r', newline='') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    create_google_user(row['first_name'].lower(), row['last_name'].lower(), row['password'])
            QMessageBox.information(self, "Succès", "Utilisateurs importés avec succès")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de l'importation du CSV: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Use Fusion style for consistency across platforms
    try:
        app.setStyle(QStyleFactory.create("Fusion"))
    except Exception:
        pass
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
