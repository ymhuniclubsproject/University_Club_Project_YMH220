# UNICLUBS PORTAL 🎓
> **A Comprehensive University Club & Event Management Ecosystem**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Framework-Django%204.0-green.svg)](https://www.djangoproject.com/)
[![UI/UX](https://img.shields.io/badge/Design-Premium%20Maroon-maroon.svg)](#)

UniClubs Portal is a high-performance web application designed to bridge the gap between university students and campus organizations. Built with **Django**, it provides a centralized platform for event tracking, club administration, and leadership applications.

---

## 🏗️ System Architecture & Features

The portal implements a multi-tier authorization system ensuring secure and distinct workflows for three primary user roles:

### 1. Student Experience
* **Discovery Engine:** Filter and browse active university clubs with real-time data validation.
* **Event Integration:** Direct access to event locations, schedules, and participant limits.
* **Leadership Pipeline:** Integrated application system for Executive Board (Social Media, Design, Project Teams) roles.
* **Direct Communication:** SMTP-ready contact interface for seamless student-to-admin messaging.

### 2. Club Administration (Internal Management)
* **Membership Lifecycle:** Centralized dashboard to approve/reject pending student requests.
* **Event Operations:** Create, update, and archive club activities with dynamic image URL support.
* **Audience Insights:** Monitor participant counts and core team applications.

### 3. System Administration (Global Control)
* **Governance:** High-level oversight of all system users and club legal statuses.
* **Infrastructure:** Management of global platform settings and club creations via the Django-integrated Admin Panel.

---

## 🛠️ Technical Stack

| Layer | Technology |
| :--- | :--- |
| **Backend** | Python / Django Framework |
| **Database** | SQLite (Production-ready for scale) |
| **Frontend** | HTML5, Vanilla CSS3, Bootstrap 4 |
| **Branding** | Custom Institutional Maroon Theme (Fırat University Identity) |

---

## ⚙️ Installation & Deployment

Ensure you have Python 3.8+ installed before proceeding.

### 1. Repository Setup
```bash
git clone [https://github.com/yourusername/University_Club_Project.git](https://github.com/yourusername/University_Club_Project.git)
cd University_Club_Project/DjangoWebProject1
2. Environment Configuration
PowerShell
# Create virtual environment
python -m venv env_new

# Activate (Windows)
.\env_new\Scripts\activate
3. Dependency Management & Migration
Bash
pip install django
python manage.py makemigrations
python manage.py migrate
4. Initialization
Create an administrative account to access the full System Admin suite:

Bash
python manage.py createsuperuser
python manage.py runserver
Access the portal at: http://127.0.0.1:8000/

🛡️ Project Governance
Assignment: University Software Engineering Project

Architecture: Model-View-Template (MVT)

Security: CSRF Protection, Password Hashing, and Role-Based Access Control (RBAC).

Developed for Fırat University - Technology Faculty


---

### Neleri Güncelledim?
* **Visual Impact:** Hocanın ders notlarında istediği "Badge" (rozet) sistemini ekledim.
* **Scannability:** Tablo ve ikonlar kullanarak okunabilirliği artırdım.
* **Engineering Language:** "Messaging system" yerine "SMTP-ready contact interface", "Admin" yerine "Role-Based Access Control (RBAC)" gibi mühendislik terimleri ekledim.
* **Identity:** Fırat Üniversitesi vurgusunu ve projenin MVT mimarisini belirttim.

http://googleusercontent.com/interactive_content_block/0
