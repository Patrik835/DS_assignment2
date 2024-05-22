## Distributed Systems Assignment 2 - RESTful API by Samuel Kollár and Patrik Palenčár

We used Flask python framework for this project, because python is the most natural language for both of us and we already had some experience with flask framework before. We have created two services: auth_service and master_data_service. The auth_service is responsible for user authentication and token generation, while the master_data_service is responsible for managing the jobs and results in the database. The services are running on different ports and are communicating with each other using HTTP requests. 
We use sqlalchemy for database management and sqlite database.

### auth_service/auth.py
This file includes authentication part of the application, POST method for verfiying user credentials and generating token (random string:user role:expiration time) and GET method for verifying that the token is not expired and is still valid.

### client.py
We use this file as a test client, containing the client-side logic. It is responsible for making requests to the servers and handling the responses. It contains one call for each of the method of each service. GET and POST methods are used for the auth service, and GET, POST, PUT methods are used for the master data service.

### create_db.py
This script is used to create the database for our application. It creates a SQLite database with two tables defined in master_data.py: Jobs and Results. 

### master_data_service/master_data.py
This file defines the data models `Jobs` and `Results` and also the API endpoint for the application. It also includes a `verify_login` function that is used to verify user credentials. The API endpoint is /jobs and it supports GET, POST and PUT methods to manipulate the Jobs and Results tables. GET method fetches all the jobs from the database, POST method adds a new job to the database and PUT method updates the status of a job in the database and adds to Results.

### instance/storage.db
This file contains the database with the tables Jobs and Results. It is created by running the create_db.py script.



We collaborated on the project using GitHub. Our public repository is available at https://github.com/Patrik835/DS_assignment2 .
