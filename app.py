# import flask libraries
import json
from flask import Flask, jsonify, request, render_template
import pymongo
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient()
db = client.test_database
students = db.students

import pprint

# Dummy/existing data
studentData = [
    {
        'FirstName': 'John',
        'LastName': 'Doe',
        'ID': '00001',
        'GPA': 4.0,
        'Class': '10A',
        'Age': 16,
        'LateAbsent' : 2,
        'Description':'Participates in the Computer Science Club and is the President of the Web Development Club.',
    },
    {
        'FirstName': 'Jane',
        'LastName': 'Doe',
        'ID': '00002',
        'GPA': 3.8,
        'Class': '10C',
        'Age': 16,
        'LateAbsent' : 4,
        'Description':'Participates in the Biology Club, Child Welfare Club, and is the Vice President of the Math Club.',
    },
]

# Adds all the database to the dict studentData
for s in students.find():
    studentData.append(s)

# Redirects to home route
@app.route("/")
def home():
    return render_template('home.html', data = studentData)

@app.route('/studentdata/<firstname>_<lastname>', methods = ['GET', 'PUT', 'DELETE'])
def get_or_update_or_delete_student(firstname,lastname):
    if request.method == 'GET':
        for index, student in enumerate(studentData):
            if student['FirstName'] == firstname and student['LastName'] == lastname:
                return studentData[index]
        return jsonify('Cannot find specified student')
    elif request.method == 'PUT':
        update = request.get_json()
        for index, student in enumerate(studentData):
            if student['FirstName'] == firstname and student['LastName'] == lastname:
                studentData[index] = update
                return jsonify({'Successful Update' : request.get_json()})
        return jsonify({'Unsuccessful Update'})
    else:
        for index, student in enumerate(studentData):
            if student['FirstName'] == firstname and student['LastName'] == lastname:
                del studentData[index]
                db.students.delete_one({'FirstName': firstname, 'LastName':lastname})
                return jsonify({'Deleted': firstname + " " + lastname})
        return jsonify({'Delete Failed'})

# Get request for all the student data in json format
@app.route('/studentdata', methods = ['GET'])
def get_all_student_data():
    return jsonify({'All Students': studentData})

@app.route('/studentdata/<id>', methods = ['GET', 'PUT', 'DELETE'])
def get_student_by_id(id):
    if request.method == 'GET':
        for index, student in enumerate(studentData):
            if student['ID'] == id:
                return studentData[index]
        return jsonify({'Cannot find specified student'})
    elif request.method == 'PUT':
        update = request.get_json()
        for index, student in enumerate(studentData):
            if student['ID'] == id:
                studentData[index] = update
                return jsonify({'Successful Update' : request.get_json()})
        return jsonify({'Unsuccessful Update'})
    else:
        for index, student in enumerate(studentData):
            if student['ID'] == id:
                del studentData[index]
                db.students.delete_one({'ID': id})
                return jsonify({'Deleted': id})
        return jsonify({'Delete Failed'})
    
@app.route('/studentdata', methods = ['POST'])
def add_student():
    new_student = request.get_json()
    id_to_use = new_student['ID']
    if does_id_exist(new_student['ID']):
        id_to_use = get_new_id(id_to_use)
    studentToAdd = {
        "FirstName": new_student['FirstName'],
        "LastName": new_student['LastName'],
        "ID": id_to_use,
        "GPA":new_student['GPA'],
        "Class":new_student['Class'],
        "Age": new_student['Age'],
        "LateAbsent": new_student['LateAbsent'],
        "Description": new_student['Description']
    }
    studentData.append(studentToAdd)
    students.insert_one(studentToAdd)
    new_student['ID'] = id_to_use
    return jsonify({'New Student':new_student})

# Gets a new ID for the student if it already exists by adding one to the largest ID in the database
def get_new_id(id):
    max_id = 0
    for student in studentData:
        if int(student['ID']) > max_id:
            max_id = int(student['ID'])
    max_id = max_id +1
    string_id = str(max_id)
    if len(str(max_id)) < 5:
        num_to_add = 5 - len(str(max_id))
        for i in range(0,num_to_add):
            string_id = '0' + string_id
    return string_id

# Checks if an ID already exists in the database
def does_id_exist(id):
    for student in studentData:
        if int(student['ID']) == int(id):
            return True
    return False