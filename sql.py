import sqlite3

# Connect to SQlite
connection = sqlite3.connect("student.db")
cursor = connection.cursor()


cursor.execute("DROP TABLE IF EXISTS SUBMISSION")
cursor.execute("DROP TABLE IF EXISTS ASSIGNMENT")
cursor.execute("DROP TABLE IF EXISTS ENROLLMENT")
cursor.execute("DROP TABLE IF EXISTS CLASS")
cursor.execute("DROP TABLE IF EXISTS INSTRUCTOR")
cursor.execute("DROP TABLE IF EXISTS COURSE")
cursor.execute("DROP TABLE IF EXISTS DEPARTMENT")
cursor.execute("DROP TABLE IF EXISTS STUDENT")


# Execute each CREATE TABLE statement immediately after defining it

# Create STUDENT table
cursor.execute("""
CREATE TABLE IF NOT EXISTS STUDENT(
    NAME VARCHAR(50) NOT NULL,
    COURSE VARCHAR(50) NOT NULL,
    DEGREE VARCHAR(50),
    SECTION VARCHAR(10),
    MARKS INTEGER,
    AGE INTEGER,
    EMAIL VARCHAR(100) UNIQUE,
    ENROLLMENT_DATE DATE
);
""")

# Create DEPARTMENT table
cursor.execute("""
CREATE TABLE IF NOT EXISTS DEPARTMENT(
    DEPT_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    DEPT_NAME VARCHAR(50) NOT NULL UNIQUE,
    BUILDING VARCHAR(50),
    BUDGET DECIMAL(12,2)
);
""")

# Create COURSE table
cursor.execute("""
CREATE TABLE IF NOT EXISTS COURSE(
    COURSE_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    COURSE_NAME VARCHAR(50) NOT NULL,
    DEPT_ID INTEGER,
    CREDITS INTEGER NOT NULL,
    DESCRIPTION TEXT,
    FOREIGN KEY (DEPT_ID) REFERENCES DEPARTMENT(DEPT_ID)
);
""")

# Create INSTRUCTOR table
cursor.execute("""
CREATE TABLE IF NOT EXISTS INSTRUCTOR(
    INSTRUCTOR_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    NAME VARCHAR(50) NOT NULL,
    DEPT_ID INTEGER,
    EMAIL VARCHAR(100) UNIQUE,
    PHONE VARCHAR(20),
    OFFICE VARCHAR(20),
    FOREIGN KEY (DEPT_ID) REFERENCES DEPARTMENT(DEPT_ID)
);
""")

# Create CLASS table
cursor.execute("""
CREATE TABLE IF NOT EXISTS CLASS(
    CLASS_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    COURSE_ID INTEGER NOT NULL,
    INSTRUCTOR_ID INTEGER NOT NULL,
    SEMESTER VARCHAR(20) NOT NULL,
    YEAR INTEGER NOT NULL,
    ROOM VARCHAR(20),
    SECTION VARCHAR(10),
    CAPACITY INTEGER,
    FOREIGN KEY (COURSE_ID) REFERENCES COURSE(COURSE_ID),
    FOREIGN KEY (INSTRUCTOR_ID) REFERENCES INSTRUCTOR(INSTRUCTOR_ID)
);
""")

# Create ENROLLMENT table
cursor.execute("""
CREATE TABLE IF NOT EXISTS ENROLLMENT(
    ENROLLMENT_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    STUDENT_EMAIL VARCHAR(100) NOT NULL,
    CLASS_ID INTEGER NOT NULL,
    ENROLLMENT_DATE DATE NOT NULL,
    GRADE VARCHAR(2),
    STATUS VARCHAR(20) DEFAULT 'Active',
    FOREIGN KEY (STUDENT_EMAIL) REFERENCES STUDENT(EMAIL),
    FOREIGN KEY (CLASS_ID) REFERENCES CLASS(CLASS_ID),
    UNIQUE(STUDENT_EMAIL, CLASS_ID)
);
""")

# Create ASSIGNMENT table
cursor.execute("""
CREATE TABLE IF NOT EXISTS ASSIGNMENT(
    ASSIGNMENT_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    CLASS_ID INTEGER NOT NULL,
    TITLE VARCHAR(100) NOT NULL,
    DESCRIPTION TEXT,
    DUE_DATE DATETIME NOT NULL,
    MAX_SCORE INTEGER NOT NULL,
    FOREIGN KEY (CLASS_ID) REFERENCES CLASS(CLASS_ID)
);
""")

# Create SUBMISSION table
cursor.execute("""
CREATE TABLE IF NOT EXISTS SUBMISSION(
    SUBMISSION_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    ASSIGNMENT_ID INTEGER NOT NULL,
    STUDENT_EMAIL VARCHAR(100) NOT NULL,
    SUBMISSION_DATE DATETIME,
    SCORE DECIMAL(5,2),
    FEEDBACK TEXT,
    STATUS VARCHAR(20) DEFAULT 'Submitted',
    FOREIGN KEY (ASSIGNMENT_ID) REFERENCES ASSIGNMENT(ASSIGNMENT_ID),
    FOREIGN KEY (STUDENT_EMAIL) REFERENCES STUDENT(EMAIL)
);
""")

# Insert into DEPARTMENT
cursor.execute('''INSERT INTO DEPARTMENT VALUES(1, 'Computer Science', 'Engineering Building', 500000)''')
cursor.execute('''INSERT INTO DEPARTMENT VALUES(2, 'Data Science', 'Science Building', 450000)''')
cursor.execute('''INSERT INTO DEPARTMENT VALUES(3, 'Cyber Security', 'Engineering Building', 400000)''')
cursor.execute('''INSERT INTO DEPARTMENT VALUES(4, 'DEVOPS', 'Technology Building', 350000)''')

# Insert into COURSE
cursor.execute('''INSERT INTO COURSE VALUES(1, 'Introduction to Programming', 1, 3, 'Basic programming concepts')''')
cursor.execute('''INSERT INTO COURSE VALUES(2, 'Database Systems', 1, 4, 'Relational database design')''')
cursor.execute('''INSERT INTO COURSE VALUES(3, 'Machine Learning', 2, 4, 'Fundamentals of ML algorithms')''')
cursor.execute('''INSERT INTO COURSE VALUES(4, 'Network Security', 3, 3, 'Cybersecurity fundamentals')''')
cursor.execute('''INSERT INTO COURSE VALUES(5, 'Cloud Infrastructure', 4, 3, 'DevOps tools and practices')''')

# Insert into INSTRUCTOR
cursor.execute('''INSERT INTO INSTRUCTOR VALUES(1, 'Dr. Smith', 1, 'smith@university.edu', '555-1001', 'ENG-201')''')
cursor.execute('''INSERT INTO INSTRUCTOR VALUES(2, 'Prof. Johnson', 2, 'johnson@university.edu', '555-1002', 'SCI-105')''')
cursor.execute('''INSERT INTO INSTRUCTOR VALUES(3, 'Dr. Lee', 3, 'lee@university.edu', '555-1003', 'ENG-205')''')
cursor.execute('''INSERT INTO INSTRUCTOR VALUES(4, 'Prof. Brown', 4, 'brown@university.edu', '555-1004', 'TECH-302')''')

# Insert into CLASS
cursor.execute('''INSERT INTO CLASS VALUES(1, 1, 1, 'Fall', 2023, 'ENG-101', 'A', 30)''')
cursor.execute('''INSERT INTO CLASS VALUES(2, 1, 1, 'Fall', 2023, 'ENG-102', 'B', 25)''')
cursor.execute('''INSERT INTO CLASS VALUES(3, 2, 2, 'Fall', 2023, 'SCI-201', 'A', 20)''')
cursor.execute('''INSERT INTO CLASS VALUES(4, 3, 3, 'Fall', 2023, 'ENG-203', 'A', 25)''')
cursor.execute('''INSERT INTO CLASS VALUES(5, 4, 4, 'Fall', 2023, 'TECH-301', 'B', 20)''')

# Insert into STUDENT (continuing your existing format)
cursor.execute('''INSERT INTO STUDENT VALUES('Ali', 'Computer Science', 'Undergraduate', 'A', 92, 19, 'ali.cs@university.edu', '2023-09-01')''')
cursor.execute('''INSERT INTO STUDENT VALUES('Zara', 'Data Science', 'Graduate', 'B', 89, 23, 'zara.ds@university.edu', '2022-09-15')''')
cursor.execute('''INSERT INTO STUDENT VALUES('Hamza', 'Computer Science', 'Undergraduate', 'A', 95, 20, 'hamza.cs@university.edu', '2023-09-01')''')
cursor.execute('''INSERT INTO STUDENT VALUES('Ayesha', 'DEVOPS', 'Undergraduate', 'A', 60, 21, 'ayesha.devops@university.edu', '2022-09-15')''')
cursor.execute('''INSERT INTO STUDENT VALUES('Fahad', 'DEVOPS', 'Graduate', 'B', 45, 24, 'fahad.devops@university.edu', '2021-09-01')''')
cursor.execute('''INSERT INTO STUDENT VALUES('Noor', 'Data Science', 'Undergraduate', 'B', 78, 19, 'noor.ds@university.edu', '2023-09-01')''')
cursor.execute('''INSERT INTO STUDENT VALUES('Bilal', 'Cyber Security', 'Undergraduate', 'A', 85, 20, 'bilal.cs@university.edu', '2022-09-15')''')
cursor.execute('''INSERT INTO STUDENT VALUES('Fatima', 'Cyber Security', 'Graduate', 'B', 80, 23, 'fatima.cs@university.edu', '2021-09-01')''')
cursor.execute('''INSERT INTO STUDENT VALUES('Usman', 'DEVOPS', 'Undergraduate', 'C', 38, 22, 'usman.devops@university.edu', '2022-09-15')''')
cursor.execute('''INSERT INTO STUDENT VALUES('Sara', 'Data Science', 'Undergraduate', 'A', 88, 20, 'sara.ds@university.edu', '2023-09-01')''')
cursor.execute('''INSERT INTO STUDENT VALUES('Hassan', 'DEVOPS', 'Graduate', 'B', 54, 25, 'hassan.devops@university.edu', '2021-09-01')''')
cursor.execute('''INSERT INTO STUDENT VALUES('Laiba', 'Data Science', 'Undergraduate', 'C', 72, 21, 'laiba.ds@university.edu', '2022-09-15')''')
cursor.execute('''INSERT INTO STUDENT VALUES('Tariq', 'Cyber Security', 'Undergraduate', 'A', 91, 19, 'tariq.cs@university.edu', '2023-09-01')''')
cursor.execute('''INSERT INTO STUDENT VALUES('Anaya', 'Data Science', 'Graduate', 'B', 81, 24, 'anaya.ds@university.edu', '2022-09-15')''')
cursor.execute('''INSERT INTO STUDENT VALUES('Ahmed', 'Cyber Security', 'Undergraduate', 'C', 68, 20, 'ahmed.cs@university.edu', '2023-09-01')''')
cursor.execute('''INSERT INTO STUDENT VALUES('Sana', 'Computer Science', 'Undergraduate', 'A', 75, 20, 'sana.cs@university.edu', '2023-09-01')''')
cursor.execute('''INSERT INTO STUDENT VALUES('Omar', 'Data Science', 'Undergraduate', 'B', 83, 19, 'omar.ds@university.edu', '2023-09-01')''')
cursor.execute('''INSERT INTO STUDENT VALUES('Hina', 'DEVOPS', 'Graduate', 'A', 65, 23, 'hina.devops@university.edu', '2022-09-15')''')
cursor.execute('''INSERT INTO STUDENT VALUES('Imran', 'Cyber Security', 'Undergraduate', 'B', 70, 21, 'imran.cs@university.edu', '2022-09-15')''')
cursor.execute('''INSERT INTO STUDENT VALUES('Zainab', 'Computer Science', 'Undergraduate', 'C', 90, 19, 'zainab.cs@university.edu', '2023-09-01')''')
cursor.execute('''INSERT INTO STUDENT VALUES('Kamran', 'Data Science', 'Graduate', 'A', 87, 24, 'kamran.ds@university.edu', '2021-09-01')''')
cursor.execute('''INSERT INTO STUDENT VALUES('Emaan', 'DEVOPS', 'Undergraduate', 'B', 58, 20, 'emaan.devops@university.edu', '2023-09-01')''')
cursor.execute('''INSERT INTO STUDENT VALUES('Rizwan', 'Cyber Security', 'Undergraduate', 'A', 79, 21, 'rizwan.cs@university.edu', '2022-09-15')''')
cursor.execute('''INSERT INTO STUDENT VALUES('Asma', 'Computer Science', 'Graduate', 'B', 82, 25, 'asma.cs@university.edu', '2021-09-01')''')
cursor.execute('''INSERT INTO STUDENT VALUES('Junaid', 'Data Science', 'Undergraduate', 'C', 71, 20, 'junaid.ds@university.edu', '2023-09-01')''')
cursor.execute('''INSERT INTO STUDENT VALUES('Sadia', 'DEVOPS', 'Undergraduate', 'A', 49, 22, 'sadia.devops@university.edu', '2022-09-15')''')
cursor.execute('''INSERT INTO STUDENT VALUES('Usama', 'Cyber Security', 'Graduate', 'B', 88, 23, 'usama.cs@university.edu', '2022-09-15')''')
cursor.execute('''INSERT INTO STUDENT VALUES('Minahil', 'Computer Science', 'Undergraduate', 'A', 93, 19, 'minahil.cs@university.edu', '2023-09-01')''')
cursor.execute('''INSERT INTO STUDENT VALUES('Danish', 'Data Science', 'Undergraduate', 'B', 76, 20, 'danish.ds@university.edu', '2023-09-01')''')

# Corrected ENROLLMENT inserts (specifying columns and omitting STATUS to use default)
cursor.execute('''INSERT INTO ENROLLMENT (ENROLLMENT_ID, STUDENT_EMAIL, CLASS_ID, ENROLLMENT_DATE, GRADE)
               VALUES(1, 'ali.cs@university.edu', 1, '2023-09-01', 'A')''')
cursor.execute('''INSERT INTO ENROLLMENT (ENROLLMENT_ID, STUDENT_EMAIL, CLASS_ID, ENROLLMENT_DATE, GRADE)
               VALUES(2, 'hamza.cs@university.edu', 1, '2023-09-01', 'A')''')
cursor.execute('''INSERT INTO ENROLLMENT (ENROLLMENT_ID, STUDENT_EMAIL, CLASS_ID, ENROLLMENT_DATE, GRADE)
               VALUES(3, 'zara.ds@university.edu', 3, '2023-09-01', 'B+')''')
cursor.execute('''INSERT INTO ENROLLMENT (ENROLLMENT_ID, STUDENT_EMAIL, CLASS_ID, ENROLLMENT_DATE, GRADE)
               VALUES(4, 'noor.ds@university.edu', 3, '2023-09-01', 'B')''')
cursor.execute('''INSERT INTO ENROLLMENT (ENROLLMENT_ID, STUDENT_EMAIL, CLASS_ID, ENROLLMENT_DATE, GRADE)
               VALUES(5, 'bilal.cs@university.edu', 4, '2023-09-01', 'A-')''')
cursor.execute('''INSERT INTO ENROLLMENT (ENROLLMENT_ID, STUDENT_EMAIL, CLASS_ID, ENROLLMENT_DATE, GRADE)
               VALUES(6, 'sara.ds@university.edu', 3, '2023-09-01', 'B+')''')
cursor.execute('''INSERT INTO ENROLLMENT (ENROLLMENT_ID, STUDENT_EMAIL, CLASS_ID, ENROLLMENT_DATE, GRADE)
               VALUES(7, 'tariq.cs@university.edu', 4, '2023-09-01', 'A')''')
cursor.execute('''INSERT INTO ENROLLMENT (ENROLLMENT_ID, STUDENT_EMAIL, CLASS_ID, ENROLLMENT_DATE, GRADE)
               VALUES(8, 'zainab.cs@university.edu', 1, '2023-09-01', 'A-')''')
cursor.execute('''INSERT INTO ENROLLMENT (ENROLLMENT_ID, STUDENT_EMAIL, CLASS_ID, ENROLLMENT_DATE, GRADE)
               VALUES(9, 'minahil.cs@university.edu', 1, '2023-09-01', 'A')''')


# Insert into ASSIGNMENT
cursor.execute('''INSERT INTO ASSIGNMENT VALUES(1, 1, 'Programming Project 1', 'Basic Python program', '2023-10-15 23:59:00', 100)''')
cursor.execute('''INSERT INTO ASSIGNMENT VALUES(2, 1, 'Midterm Exam', 'Covers chapters 1-5', '2023-11-01 09:00:00', 100)''')
cursor.execute('''INSERT INTO ASSIGNMENT VALUES(3, 3, 'ML Lab 1', 'Linear regression implementation', '2023-10-20 23:59:00', 50)''')
cursor.execute('''INSERT INTO ASSIGNMENT VALUES(4, 4, 'Security Audit', 'Network vulnerability assessment', '2023-11-10 23:59:00', 80)''')


# Insert into SUBMISSION
cursor.execute('''INSERT INTO SUBMISSION (SUBMISSION_ID, ASSIGNMENT_ID, STUDENT_EMAIL, SUBMISSION_DATE, SCORE, FEEDBACK)
                  VALUES(1, 1, 'ali.cs@university.edu', '2023-10-14 18:30:00', 95, 'Excellent work!')''')
cursor.execute('''INSERT INTO SUBMISSION (SUBMISSION_ID, ASSIGNMENT_ID, STUDENT_EMAIL, SUBMISSION_DATE, SCORE, FEEDBACK)
                  VALUES(2, 1, 'hamza.cs@university.edu', '2023-10-15 15:45:00', 88, 'Good solution')''')
cursor.execute('''INSERT INTO SUBMISSION (SUBMISSION_ID, ASSIGNMENT_ID, STUDENT_EMAIL, SUBMISSION_DATE, SCORE, FEEDBACK)
                  VALUES(3, 3, 'zara.ds@university.edu', '2023-10-19 22:10:00', 45, 'Needs improvement')''')
cursor.execute('''INSERT INTO SUBMISSION (SUBMISSION_ID, ASSIGNMENT_ID, STUDENT_EMAIL, SUBMISSION_DATE, SCORE, FEEDBACK)
                  VALUES(4, 1, 'zainab.cs@university.edu', '2023-10-15 23:50:00', 92, 'Well documented')''')
cursor.execute('''INSERT INTO SUBMISSION (SUBMISSION_ID, ASSIGNMENT_ID, STUDENT_EMAIL, SUBMISSION_DATE, SCORE, FEEDBACK)
                  VALUES(5, 4, 'tariq.cs@university.edu', '2023-11-09 14:20:00', 78, 'Thorough analysis')''')


# Function to print table records with column headers
def print_table(table_name):
    print(f"\n{'-'*50}")
    print(f"Records in {table_name} table:")
    
    # Get column names
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [col[1] for col in cursor.fetchall()]
    print(" | ".join(columns))
    print("-"*len(" | ".join(columns)))
    
    # Get and print records
    cursor.execute(f'''SELECT * FROM {table_name}''')
    for row in cursor.fetchall():
        print(" | ".join(str(value) for value in row))

# Print all tables
print("\nDATABASE RECORDS:")
print_table('DEPARTMENT')
print_table('COURSE')
print_table('INSTRUCTOR')
print_table('CLASS')
print_table('STUDENT')
print_table('ENROLLMENT')
print_table('ASSIGNMENT')
print_table('SUBMISSION')

print("\nDatabase records printed successfully for all tables")
## Commit your changes int he databse
connection.commit()
connection.close()