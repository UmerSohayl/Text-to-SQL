from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import sqlite3
import groq

groq_api_key = os.getenv("GROQ_API_KEY")

def get_groq_response(question, prompt):
    client = groq.Groq(api_key=groq_api_key)
    response = client.chat.completions.create(
        model="llama3-8b-8192",  # or another Groq-supported model
        messages=[
            {"role": "system", "content": prompt[0]},
            {"role": "user", "content": question}
        ],
        max_tokens=150,
        temperature=0
    )
    return response.choices[0].message.content.strip()

def read_query(sqll,db):
    con=sqlite3.connect(db)
    cur=con.cursor()
    cur.execute(sqll)
    rows=cur.fetchall()
    con.commit()
    con.close()
    for row in rows:
        print(row)
    return rows


prompt=[
    """
    INSTRUCTION: Generate ONLY the SQL query. No explanations, formatting, or commentary.
DATABASE SCHEMA
Tables

STUDENT: NAME, COURSE, DEGREE, SECTION, MARKS, AGE, EMAIL(PK), ENROLLMENT_DATE
DEPARTMENT: DEPT_ID(PK), DEPT_NAME, BUILDING, BUDGET
COURSE: COURSE_ID(PK), COURSE_NAME, DEPT_ID(FK), CREDITS, DESCRIPTION
INSTRUCTOR: INSTRUCTOR_ID(PK), NAME, DEPT_ID(FK), EMAIL, PHONE, OFFICE
CLASS: CLASS_ID(PK), COURSE_ID(FK), INSTRUCTOR_ID(FK), SEMESTER, YEAR, ROOM, SECTION, CAPACITY
ENROLLMENT: ENROLLMENT_ID(PK), STUDENT_EMAIL(FK), CLASS_ID(FK), ENROLLMENT_DATE, GRADE, STATUS
SUBMISSION: SUBMISSION_ID(PK), ASSIGNMENT_ID(FK), STUDENT_EMAIL(FK), SUBMISSION_DATE, SCORE, FEEDBACK, STATUS

Key Relationships

Student ↔ Class: via ENROLLMENT table
Course ↔ Department: COURSE.DEPT_ID = DEPARTMENT.DEPT_ID
Instructor ↔ Department: INSTRUCTOR.DEPT_ID = DEPARTMENT.DEPT_ID
Class ↔ Course: CLASS.COURSE_ID = COURSE.COURSE_ID
Class ↔ Instructor: CLASS.INSTRUCTOR_ID = INSTRUCTOR.INSTRUCTOR_ID

TERM MAPPINGS
Student Data: "student/name" → STUDENT.NAME | "contact/ID" → STUDENT.EMAIL | "roll" → STUDENT.EMAIL
Academic: "grade/score/result" → ENROLLMENT.GRADE or STUDENT.MARKS | "course/subject" → COURSE.COURSE_NAME | "class/section" → CLASS.CLASS_ID | "degree/program" → STUDENT.DEGREE | "department" → DEPARTMENT.DEPT_NAME | "instructor/professor/teacher" → INSTRUCTOR.NAME
Temporal: "current/recent" → ENROLLMENT_DATE > DATE('now','-1 year') | "semester" → CLASS.SEMESTER | "newest" → ORDER BY ENROLLMENT_DATE DESC
QUERY RULES

Use explicit JOINs with table aliases (s=STUDENT, c=COURSE, etc.)
Student-class relationships must use ENROLLMENT table
Format dates as 'YYYY-MM-DD'
Use standard SQL (SQLite dialect)
Return ONLY the SQL query

EXAMPLES
Input: "Find computer science students with marks above 80"
Output:


**Convert this question:**
{user_question}
    """
]


st.set_page_config(page_title="Retrieve Any SQL query")
st.header("Text 2 SQL App")


# Show schema images
st.image("schema1.png", caption="Database Schema 1", use_container_width=True)
st.image("schema2.png", caption="Database Schema 2", use_container_width=True)

question=st.text_input("Input: ",key="input")

submit=st.button("Ask the question")


if submit:
    sql_query = get_groq_response(question, prompt)
    print(sql_query)
    st.subheader("Generated SQL Query")
    st.code(sql_query, language="sql")

    # Execute the query and get both rows and columns
    con = sqlite3.connect("student.db")
    cur = con.cursor()
    try:
        cur.execute(sql_query)
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        if rows:
            import pandas as pd
            df = pd.DataFrame(rows, columns=columns)
            st.subheader("The Response is")
            st.dataframe(df, use_container_width=True)
        else:
            st.subheader("The Response is")
            st.write("No results found.")
    except Exception as e:
        st.error(f"Error executing query: {e}")
    finally:
        con.close()