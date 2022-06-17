# import flask libraries
import json
from django.shortcuts import render
from flask import Flask, jsonify, request, render_template, redirect, url_for
import pymongo
from random import choice
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient()
db = client.test_database
students = db.students

import pprint

# Dummy/existing data
studentData = []

# Adds all the database to the dict studentData
for s in students.find():
    studentData.append(s)

# Redirects to home route
@app.route("/")
def home():
    return render_template('home.html', data = studentData)

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
                students.delete_one({'ID': id})
                return jsonify({'Deleted': id})
        return jsonify({'Delete Failed'})

@app.route('/data/<id>', methods = ['GET', 'POST'])
def student_id_methods(id):
    if request.method == 'GET':
        for index, student in enumerate(studentData):
            if student['ID'] == id:
                return studentData[index]
        return jsonify({'Cannot find specified student'})
    else:
        update = request.form.to_dict()
        for index, student in enumerate(studentData):
            if student['ID'] == id:
                students.delete_one({'ID': id})
                students.insert_one(update)
                id_to_use = update['ID']
                if does_id_exist(update['ID']):
                    id_to_use = get_new_id(id_to_use)
                update['ID'] = id_to_use
                studentData[index] = update
                return redirect(url_for('home'))
        return jsonify({'Unsuccessful Update'})

# Adds a student through POST
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

@app.route('/<id>')
def go_to_profile(id):
    for index, student in enumerate(studentData):
        if student['ID'] == id:
            data = studentData[index]
            return render_template('profile.html', student = data)
    return jsonify('This student does not exist')

# Deleting a profile through GUI
@app.route('/<id>/delete', methods = ['POST'])
def delete_profile(id):
    if request.method == 'POST':
        for index, student in enumerate(studentData):
            if student['ID'] == id:
                data = studentData[index]
                del studentData[index]
                students.delete_one({'ID': id})
                return redirect(url_for('home'))
    else:
        return jsonify('Something went wrong')


# Returns a view of a form to update a post
@app.route('/<id>/edit')
def go_to_edit(id):
    data = 0
    for index, student in enumerate(studentData):
        if student['ID'] == id:
            data = studentData[index]
    if not data == 0:
        return render_template('edit.html', student = data)
    else:
        return jsonify('This student does not exist')

@app.route('/add')
def add_a_student_link():
    return render_template('add.html')

# Adds a new student through GUI
@app.route('/addstudent', methods = ['POST'])
def add_profile():
    to_add = request.form.to_dict()
    id_to_use = to_add['ID']
    if does_id_exist(to_add['ID']):
        id_to_use = get_new_id(id_to_use)
    to_add['ID'] = id_to_use
    students.insert_one(to_add)
    studentData.append(to_add)
    return redirect(url_for('home'))

# Gets a random student
@app.route('/rng')
def random_student():
    ids = []
    for index, student in enumerate(studentData):
        ids.append(student['ID'])
    selection = choice(ids)
    return redirect(url_for('go_to_profile', id = selection))

# Goes to the guide
@app.route('/guide')
def go_to_guide():
    return render_template('guide.html')
