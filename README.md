# Expense Tracker API

A simple **Expense Tracker REST API** built with **Python (Flask)**.  
It supports creating, reading, updating, deleting, and reporting expenses with category filters.

---

## 🚀 Features
- Add, update, delete expenses
- List all expenses
- Fetch expense by ID
- Filter expenses by category (Case Insensitive)
- Expense summary (by category)
- JSON responses
- SQLite database (default)

---

## 📂 Project Structure
expense-tracker/

│── app/ #Application factory

│── config/ # Configuration settings

│── expenses/ # Expense blueprint (routes, logic)

│── models/ # Database models

│── routes/ # Route definitions

│── test_app/ # Unit tests

│── venv/ # Virtual environment (ignored in Git)

│── pycache/ # Python cache files (ignored in Git)

│── .gitignore

│── README.md


## ⚙️ Setup Instructions

### 1. Clone Repository
##```bash

git clone https://github.com/PriankaMitha/Expense-Tracker-API.git

cd Expense-Tracker-API

### 2. Create Virtual Environment & Install Dependencies
python -m venv venv

venv\Scripts\activate   # On Windows

source venv/bin/activate # On Mac/Linux

pip install -r requirements.txt

### 3. Run the App
flask run

API will be available at: http://127.0.0.1:5000/

### 📌 API Endpoints
Add Expense
 
  http
  POST /add

Get Expense by ID
 
  http
  GET /expense/<id>

List All Expenses
  
  http
  GET /expenses

Get Expense by Category
  
  http
  GET /expense/category/<category>

Update Expense
  
  http
  PUT /expense/<id>

Delete Expense
  
  http
  DELETE /expense/<id>

Expense Summary
  
  http
  GET /report
  
  🧪 Running Tests

bash

pytest
