# 🎓 Student Management System

A professional desktop CRUD application built with **Python 3**, **Tkinter**, and **MySQL**.

---

## ✨ Features

| Feature | Details |
|---------|---------|
| **Add Student** | Validated form with all fields, parameterized INSERT |
| **View Students** | Sortable Treeview with alternating row colours |
| **Update Student** | Select a row → edit fields → save changes |
| **Delete Student** | Confirmation dialog before permanent removal |
| **Search** | Search by Name (partial match) or by Student ID |
| **Sort columns** | Click any column header to sort ascending / descending |
| **Input validation** | Required fields, age range, email format, phone length |
| **Error handling** | try/except blocks with user-friendly message boxes |

---

## 📁 Project Structure

```
student_management_system/
├── main.py          # Tkinter GUI + event handlers
├── database.py      # Database class – all MySQL operations
├── student.py       # Student model + validation helpers
├── setup.sql        # DB + table creation script (with sample data)
├── requirements.txt # Python dependencies
└── README.md        # This file
```

---

## ⚙️ Prerequisites

| Requirement | Version |
|-------------|---------|
| Python | 3.8 or higher |
| MySQL Server | 5.7 / 8.x |
| mysql-connector-python | ≥ 8.0.33 |

---

## 🚀 Step-by-Step Setup

### 1 – Install Python dependencies

```bash
pip install -r requirements.txt
```

### 2 – Start MySQL and create the database

**Option A – use the SQL script:**

```bash
mysql -u root -p < setup.sql
```

**Option B – manual setup in MySQL Workbench / CLI:**

```sql
CREATE DATABASE IF NOT EXISTS student_management;
USE student_management;

CREATE TABLE IF NOT EXISTS students (
    student_id     INT AUTO_INCREMENT PRIMARY KEY,
    name           VARCHAR(100) NOT NULL,
    age            INT NOT NULL,
    gender         VARCHAR(10),
    course         VARCHAR(100),
    email          VARCHAR(100) UNIQUE,
    phone          VARCHAR(15),
    address        TEXT,
    admission_date DATE
);
```

> **Tip:** The application also auto-creates the database and table on first run
> (as long as the MySQL user has `CREATE` privileges).

### 3 – Configure your MySQL credentials

Open **`database.py`** and update the `Database.__init__` defaults:

```python
def __init__(
    self,
    host="localhost",
    user="root",       # ← your MySQL username
    password="",       # ← your MySQL password
    database="student_management"
):
```

### 4 – Run the application

```bash
python main.py
```

---

## 🖥️ Usage Guide

### Adding a student
1. Fill in **Name** and **Age** (required fields, marked with `*`).
2. Fill in optional fields (gender, course, email, phone, address, admission date).
3. Click **➕ Add Student**.

### Editing a student
1. Click a row in the table to load its data into the form.
2. Modify any field.
3. Click **✏️ Update**.

### Deleting a student
1. Select a row in the table.
2. Click **🗑️ Delete** and confirm the dialog.

### Searching
1. Type a name or ID in the search box.
2. Choose the search type (Name / ID) using the radio buttons.
3. Click **🔍 Search** or press **Enter**.
4. Click **Show All** to reset.

### Sorting
Click any column header in the table to sort. Click again to reverse order.

---

## 🛡️ Security Notes

- All SQL queries use **parameterized placeholders** (`%s`) — no string
  concatenation — preventing SQL injection.
- Email addresses must be **unique** (enforced at the database level).
- Passwords are not stored in this demo application.

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|---------|
| `Can't connect to MySQL` | Ensure MySQL service is running (`mysql.server start` or `net start MySQL`) |
| `Access denied for user` | Check credentials in `database.py` |
| `ModuleNotFoundError: mysql` | Run `pip install mysql-connector-python` |
| `Duplicate entry for email` | Each student must have a unique email address |

---

## 📄 License

MIT – free for personal and educational use.
