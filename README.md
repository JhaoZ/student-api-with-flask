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

![Home Page](images/home.png)

To launch, use ```flask run -h localhost -p {whichever port you want}``` and then open ```localhost:{port}```

Made originally during UIUC SOSP 2022
