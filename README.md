CSYE 6225 Assignment Cloud Computing
# webservice 
<b> Prerequisities for building and deploying application: </b>

You will require Python installed, with an IDE of your choice and POSTMAN to test the API endpoint.
# Install Dependencies

```bash
$ python3 -m venv env
$ cd env/Scripts/
$ . activate
$ cd ../..
(env) $ pip install -r requirements.txt
(env) $ pip install mysql-connector-python or pip install mysql pymysql
(env) $ pip install Flask-UUID
```

# Run Application

```bash
(env) $ flask run
or
(env) $ python app.py
```

# Run Application

```bash
(env) $ pytest
```

# Access Health Check via POSTMAN

Set it to GET and enter the URL below

GET - http://127.0.0.1:5000/healthz [OLD]
GET - http://10.110.254.15:8080/healthz [NEW]

## Access User APIs

1. POST - http://127.0.0.1:5000/v1/user [OLD]
   POST - http://10.110.254.15:8080/v1/user [NEW]

```bash
{
  "first_name": "Jane",
  "last_name": "Doe",
  "password": "skdjfhskdfjhg",
  "username": "jane.doe@example.com"
}
```

2. GET - http://127.0.0.1:5000//v1/user/self (*Protected) [OLD]
2. GET - http://10.0.0.172:5000//v1/user/self/pic (*Protected) [NEW]


Use basic auth for authorization. Add username and password of user used during user creation.

3. PUT - http://127.0.0.1:5000//v1/user/self (*Protected)

```bash
{
  "first_name": "Joan",
  "last_name": "Doe",
  "password": "skdjfhskdfjhg",
  "username": "joan.doe@example.com"
}
```

# Github Workflow Actions

Code under `.github/workflows/python-app.yml`

It installs dependencies and run the test on commit on `main` branch

You can check the status on github portal and "Actions" Tab
