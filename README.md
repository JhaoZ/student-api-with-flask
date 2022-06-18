# student-api-with-flask
A Student API demonstration created with flask

This is a demonstration on how to use APIs. Programmed in flask with libraries like jinja, it also provides front-end support. You can either manually edit the data through front end or use an API call to do so (for example, by Postman). The posts are saved in a database so they won't erase after restarting the server.

Several libraries/databases are needed for this:
```
Jinja,
Flask,
pymongo,
A mongodb installation
```
### GUI

![Home Page](/images/home.PNG)
The home page with 2 examples of students. The home page is where you can view all the students. Note: The home page will be empty when you first open it, because there is no initial data, you will have to add your own.

The add a student button leads you to a form where you can add students.

![Add Student Page](/images/AddStudentPage.PNG)

Filling out this form and clicking the submit button will add the the student to the home page and the database.

### API CALLS

API calls to this are done through a different link. You must use the link ```localhost:{port number}/studentdata``` to manipulate the student data through API calls.
To send requests, postman (https://web.postman.co/) can be used. 

To access all of the students in JSON format, you can send a GET request to ```localhost:{port number}/studentdata```.

To access one of the students in JSON format, you can send a GET request to ```localhost:{port number}/studentdata/<id>```, where ```id``` stands for student ID (student IDs cannot be repeated, each student has a unique ID).

To add a student, you send a POST request to ```localhost:{port number}/studentdata```, with the format being
```{"FirstName": [put the first name here], "LastName": [put the last name here], "ID": [put student ID here], "GPA": [put student GPA here], "Class": [put class here], "Age": [put student age here], "LateAbsent": [put the number of tardies and absents for the student here], "Description": [put a description here]}```

To edit/delete a student, send a PUT/DELETE request (respectively) to ```localhost:{port number}/studentdata/<id>```. For editing a student, you must send a PUT request with the JSON format of a student shown above.

### HOW TO USE

To launch, use ```flask run -h localhost -p {whichever port you want}``` and then open ```localhost:{port}``` in your browser. Alternativly, open postman and use the API calls to access the website data.

Made originally during UIUC SOSP 2022
