from flask import Flask, render_template, request, send_file
from pymysql import connections
import os
import boto3
from config import *

app = Flask(__name__)

bucket = custombucket
region = customregion

db_conn = connections.Connection(
    host=customhost,
    port=3306,
    user=customuser,
    password=custompass,
    db=customdb

)
output = {}
table = 'Student'

@app.route("/studProfile/<stud_id>", methods=['GET', 'POST'])
def GetStudInfo(stud_id):
    # Fetch student information from the database
    cursor = db_conn.cursor()
    cursor.execute(f"SELECT * FROM Student WHERE stud_id = {stud_id}")
    student_data = cursor.fetchone()
    cursor.close()

    if student_data:
        # Extract student information
        stud_id, stud_name, stud_gender, stud_IC, stud_email, stud_HP, stud_address, stud_programme, stud_resume = student_data

        # Create a link to download the resume
        resume_link = f"/preview/{stud_id}"

        return render_template('studProfile.html', stud_id=stud_id, stud_name=stud_name, stud_gender=stud_gender,
                               stud_IC=stud_IC, stud_email=stud_email, stud_HP=stud_HP, stud_address=stud_address,
                               stud_programme=stud_programme, resume_link=resume_link)

    return "Student not found"

@app.route("/preview/<stud_id>")
def preview_file(stud_id):
    # Fetch the resume BLOB from the database
    cursor = db_conn.cursor()
    cursor.execute(f"SELECT stud_resume FROM Student WHERE stud_id = {stud_id}")
    resume_data = cursor.fetchone()
    cursor.close()

    if resume_data:
        # Save the resume to a temporary file
        resume_blob = resume_data[0]
        temp_file_path = f"temp_resume_{stud_id}.pdf"

        with open(temp_file_path, 'wb') as file:
            file.write(resume_blob)

        # Send the file for download
        return send_file(temp_file_path, as_attachment=True)
    else:
        return "Resume not found"
