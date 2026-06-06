"""
database.py - Database connection and operations for Student Management System
Handles all MySQL database interactions using OOP principles.
"""

import mysql.connector
from mysql.connector import Error
from datetime import date


class Database:
    """Manages MySQL database connection and CRUD operations for students."""

    def __init__(self, host="localhost", user="root", password="root", database="student_management"):
        """Initialize database connection parameters."""
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

    def connect(self):
        """Establish a connection to the MySQL database."""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                self.cursor = self.connection.cursor()
                return True
        except Error as e:
            raise ConnectionError(f"Failed to connect to database: {e}")
        return False

    def disconnect(self):
        """Close the database connection safely."""
        if self.cursor:
            self.cursor.close()
        if self.connection and self.connection.is_connected():
            self.connection.close()

    def setup_database(self):
        """Create the database and students table if they don't exist."""
        try:
            # Connect without specifying a database first
            temp_conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password
            )
            temp_cursor = temp_conn.cursor()

            # Create database if not exists
            temp_cursor.execute(
                f"CREATE DATABASE IF NOT EXISTS {self.database}"
            )
            temp_conn.commit()
            temp_cursor.close()
            temp_conn.close()

            # Now connect to the database and create table
            self.connect()
            create_table_query = """
                CREATE TABLE IF NOT EXISTS students (
                    student_id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    age INT NOT NULL,
                    gender VARCHAR(10),
                    course VARCHAR(100),
                    email VARCHAR(100) UNIQUE,
                    phone VARCHAR(15),
                    address TEXT,
                    admission_date DATE
                )
            """
            self.cursor.execute(create_table_query)
            self.connection.commit()
            return True

        except Error as e:
            raise RuntimeError(f"Database setup failed: {e}")

    # ─────────────────────────────────────────────
    # CREATE
    # ─────────────────────────────────────────────

    def add_student(self, name, age, gender, course, email, phone, address, admission_date):
        """Insert a new student record using a parameterized query."""
        try:
            query = """
                INSERT INTO students
                    (name, age, gender, course, email, phone, address, admission_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (name, age, gender, course, email, phone, address, admission_date)
            self.cursor.execute(query, values)
            self.connection.commit()
            return self.cursor.lastrowid
        except Error as e:
            self.connection.rollback()
            raise RuntimeError(f"Failed to add student: {e}")

    # ─────────────────────────────────────────────
    # READ
    # ─────────────────────────────────────────────

    def view_students(self):
        """Fetch all student records ordered by name."""
        try:
            query = "SELECT * FROM students ORDER BY name ASC"
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Error as e:
            raise RuntimeError(f"Failed to fetch students: {e}")

    def search_by_id(self, student_id):
        """Find a student by their numeric ID."""
        try:
            query = "SELECT * FROM students WHERE student_id = %s"
            self.cursor.execute(query, (student_id,))
            return self.cursor.fetchall()
        except Error as e:
            raise RuntimeError(f"Search by ID failed: {e}")

    def search_by_name(self, name):
        """Find students whose name contains the given string (case-insensitive)."""
        try:
            query = "SELECT * FROM students WHERE name LIKE %s"
            self.cursor.execute(query, (f"%{name}%",))
            return self.cursor.fetchall()
        except Error as e:
            raise RuntimeError(f"Search by name failed: {e}")

    # ─────────────────────────────────────────────
    # UPDATE
    # ─────────────────────────────────────────────

    def update_student(self, student_id, name, age, gender, course,
                       email, phone, address, admission_date):
        """Update an existing student record by ID."""
        try:
            query = """
                UPDATE students SET
                    name = %s, age = %s, gender = %s, course = %s,
                    email = %s, phone = %s, address = %s, admission_date = %s
                WHERE student_id = %s
            """
            values = (name, age, gender, course, email, phone,
                      address, admission_date, student_id)
            self.cursor.execute(query, values)
            self.connection.commit()
            return self.cursor.rowcount
        except Error as e:
            self.connection.rollback()
            raise RuntimeError(f"Failed to update student: {e}")

    # ─────────────────────────────────────────────
    # DELETE
    # ─────────────────────────────────────────────

    def delete_student(self, student_id):
        """Delete a student record by ID."""
        try:
            query = "DELETE FROM students WHERE student_id = %s"
            self.cursor.execute(query, (student_id,))
            self.connection.commit()
            return self.cursor.rowcount
        except Error as e:
            self.connection.rollback()
            raise RuntimeError(f"Failed to delete student: {e}")
