-- =============================================================
--  setup.sql  –  Student Management System database setup
--  Run:  mysql -u root -p < setup.sql
-- =============================================================

-- Create & select the database
CREATE DATABASE IF NOT EXISTS student_management
    DEFAULT CHARACTER SET utf8mb4
    DEFAULT COLLATE utf8mb4_unicode_ci;

USE student_management;

-- Students table
CREATE TABLE IF NOT EXISTS students (
    student_id     INT           AUTO_INCREMENT PRIMARY KEY,
    name           VARCHAR(100)  NOT NULL,
    age            INT           NOT NULL CHECK (age BETWEEN 1 AND 120),
    gender         VARCHAR(10),
    course         VARCHAR(100),
    email          VARCHAR(100)  UNIQUE,
    phone          VARCHAR(15),
    address        TEXT,
    admission_date DATE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ── Sample data (optional – remove if not needed) ─────────────
INSERT INTO students
    (name, age, gender, course, email, phone, address, admission_date)
VALUES
    ('Alice Johnson',  21, 'Female', 'Computer Science',       'alice@example.com',  '9876543210', '12 Oak Street, Springfield',   '2024-07-01'),
    ('Bob Smith',      23, 'Male',   'Information Technology', 'bob@example.com',    '9123456780', '45 Maple Ave, Shelbyville',     '2024-07-15'),
    ('Carol Martinez', 20, 'Female', 'Business Administration','carol@example.com',  '9988776655', '78 Pine Road, Capitol City',    '2024-08-01'),
    ('David Lee',      22, 'Male',   'Mechanical Engineering', 'david@example.com',  '9001122334', '99 Elm Blvd, Ogdenville',       '2024-08-10'),
    ('Eva Chen',       19, 'Female', 'Mathematics',            'eva@example.com',    '9445566778', '23 Birch Lane, North Haverbrook','2024-09-01');

SELECT CONCAT('Setup complete. Students inserted: ', COUNT(*)) AS status
FROM students;
