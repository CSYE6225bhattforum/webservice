CSYE 6225 Assignment01 
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

GET - http://127.0.0.1:5000/healthz

## Access User APIs

1. POST - http://127.0.0.1:5000/v1/user

```bash
{
  "first_name": "Jane",
  "last_name": "Doe",
  "password": "skdjfhskdfjhg",
  "username": "jane.doe@example.com"
}
```

2. GET - http://127.0.0.1:5000//v1/user/self (*Protected)

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