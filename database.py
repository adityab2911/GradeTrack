import sqlite3
import json


DATABASE_NAME = "gradetrack.db"


def get_connection():
    return sqlite3.connect(DATABASE_NAME)



def initialize_database():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll_number TEXT UNIQUE NOT NULL,
            batch TEXT,
            department TEXT,
            course TEXT,
            college TEXT,
            semester INTEGER,
            email TEXT,

            cgpa REAL,
            attendance REAL,
            target_cgpa REAL,
            target_attendance REAL,

            completed_credits INTEGER,
            remaining_credits INTEGER,

            semesters TEXT
        )
    """)

    connection.commit()
    connection.close()


def save_student(student_data, old_roll_number=None):

    connection = get_connection()
    cursor = connection.cursor()

    # If the roll number was changed while editing,
    # update the existing student's roll number first.
    if old_roll_number and old_roll_number != student_data["roll_number"]:

        cursor.execute(
            """
            UPDATE students
            SET
                name = ?,
                roll_number = ?,
                batch = ?,
                department = ?,
                course = ?,
                college = ?,
                semester = ?,
                email = ?,
                cgpa = ?,
                attendance = ?,
                target_cgpa = ?,
                target_attendance = ?,
                completed_credits = ?,
                remaining_credits = ?,
                semesters = ?
            WHERE roll_number = ?
            """,
            (
                student_data["name"],
                student_data["roll_number"],
                student_data["batch"],
                student_data["department"],
                student_data["course"],
                student_data["college"],
                student_data["semester"],
                student_data["email"],
                student_data["academic"]["cgpa"],
                student_data["academic"]["attendance"],
                student_data["academic"]["target_cgpa"],
                student_data["academic"]["target_attendance"],
                student_data["academic"]["completed_credits"],
                student_data["academic"]["remaining_credits"],
                json.dumps(student_data["academic"]["semesters"]),
                old_roll_number
            )
        )

    else:

        cursor.execute(
            """
            INSERT INTO students (
                name,
                roll_number,
                batch,
                department,
                course,
                college,
                semester,
                email,
                cgpa,
                attendance,
                target_cgpa,
                target_attendance,
                completed_credits,
                remaining_credits,
                semesters
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

            ON CONFLICT(roll_number) DO UPDATE SET

                name = excluded.name,
                batch = excluded.batch,
                department = excluded.department,
                course = excluded.course,
                college = excluded.college,
                semester = excluded.semester,
                email = excluded.email,
                cgpa = excluded.cgpa,
                attendance = excluded.attendance,
                target_cgpa = excluded.target_cgpa,
                target_attendance = excluded.target_attendance,
                completed_credits = excluded.completed_credits,
                remaining_credits = excluded.remaining_credits,
                semesters = excluded.semesters
            """,
            (
                student_data["name"],
                student_data["roll_number"],
                student_data["batch"],
                student_data["department"],
                student_data["course"],
                student_data["college"],
                student_data["semester"],
                student_data["email"],
                student_data["academic"]["cgpa"],
                student_data["academic"]["attendance"],
                student_data["academic"]["target_cgpa"],
                student_data["academic"]["target_attendance"],
                student_data["academic"]["completed_credits"],
                student_data["academic"]["remaining_credits"],
                json.dumps(student_data["academic"]["semesters"])
            )
        )

    connection.commit()
    connection.close()


def get_all_students():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM students
        ORDER BY name
    """)

    students = cursor.fetchall()

    connection.close()

    return students