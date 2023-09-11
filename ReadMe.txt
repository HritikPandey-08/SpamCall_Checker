StepUp the DATABASE Settings.
1. I am using postgreSQL so in settings.py make changes accordingly
example:-
 'ENGINE': 'django.db.backends.postgresql',  # Specify the database engine
        'NAME': 'your_database_name',  # Replace with your actual database name
        'USER': 'your_database_user',  # Replace with your actual database username
        'PASSWORD': 'your_database_password',  # Replace with your actual database password
        'HOST': 'localhost',  # Replace with your actual database host
        'PORT': '5432',  # Replace with your actual database port

2. know trigger the api 
a. for create user
http://127.0.0.1:8000/api/user/register/
add body 
{
  "name": "jackson",
  "email_address": "jackson@test.net",
  "phone_number": "9012345678",
  "password": "pass1234"
}

b. login user
http://127.0.0.1:8000/api/user/login/
add body 
{
  "phone_number":"9012345678",
  "password":"pass1234"
}

here in output you will get the access token copy that <token> somewhere we will user that in spam marking

c. to mark a number spam 
in header add
Authorization: Bearer <token>

add body
{
  "phone_number":"0987654321"
}

d. to check a spam number list
in header add
Authorization: Bearer <token>

add body
{
  "phone_number":"0987654321"
}

