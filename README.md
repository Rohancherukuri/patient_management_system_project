🏥 Patient Management System

A full-stack Patient Management System built with FastAPI, SurrealDB, and Flet (Python UI).
It provides a robust backend API for managing patients and a modern frontend dashboard with charts, tables, and forms.

🚀 Features
✅ Backend (FastAPI + SurrealDB)

CRUD API for patients (/create, /view, /patient/{id}, /edit/{id}, /delete/{id})

Sorting & Filtering patients by age, height, weight, or BMI

JSON + SurrealDB persistence (keeps local file + database in sync)

Validation with Pydantic models (Patient, PatientUpdate)

Async DB operations with connection pooling

✅ Frontend (Flet)

Dashboard (total patients, verdict distribution, gender split, city stats)

Patient List (sortable, searchable table)

Patient Form (add or edit patient records)

Patient Detail View (view, edit, delete actions)

Navigation System (multi-page UI)

📂 Project Structure
.
├── backend/
│   ├── api.py                # FastAPI routes + APIClient
│   ├── database.py           # SurrealDB wrapper
│   ├── orm.py                # Pydantic models
│   ├── patients.json         # Initial patient data
│   └── main.py               # FastAPI entrypoint
│
├── frontend/
│   ├── app.py                # Flet entrypoint
│   ├── utils/
│   │   ├── constants.py      # Page configuration
│   │   └── api_client.py     # Backend API calls
│   ├── components/
│   │   └── navigation.py     # Navigation manager
│   ├── pages/
│   │   ├── home_page.py      # Dashboard
│   │   ├── about_page.py     # About app
│   │   ├── patients_page.py  # Patients list
│   │   ├── patient_form_page.py # Create/Edit
│   │   └── patient_detail_page.py # Detail view
│
├── surrealdb.log             # Database logs
├── README.md                 # 📖 You are here
└── requirements.txt          # Dependencies

⚡ Installation
1️⃣ Clone Repository
git clone https://github.com/Rohancherukuri/patient-management-system.git
cd patient_management_system

2️⃣ Setup Python Environment
conda create -n fastapi_env python=3.11
conda activate fastapi_env

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Start SurrealDB

Download SurrealDB from surrealdb.com
 and run:

surreal start --log debug memory


(or use surreal start file:mydb.db to persist data)

5️⃣ Run APP 
python main.py

🔑 API Endpoints
Method	Endpoint	Description
GET	/	Welcome message
GET	/about	About API info
GET	/view	Get all patients
GET	/patient/{id}	Get single patient by ID
GET	/sort?sort_by=bmi	Sort patients (by age, bmi, etc.)
POST	/create	Create a new patient
PUT	/edit/{id}	Update existing patient
DELETE	/delete/{id}	Delete a patient
📊 Example Patient Data
{
  "P001": {
    "name": "Ananya Verma",
    "city": "Guwahati",
    "age": 28,
    "gender": "female",
    "height": 1.65,
    "weight": 90.0,
    "bmi": 33.06,
    "verdict": "Obese"
  }
}

📷 Screenshots (Frontend Preview)

Dashboard → Patient stats + charts

Patient List → Table view

Patient Form → Add / Edit form

Detail Page → Patient info + delete/edit buttons

🛠️ Tech Stack

Backend: FastAPI, Pydantic

Database: SurrealDB (async)

Frontend: Flet (Python UI toolkit)

Language: Python 3.11+