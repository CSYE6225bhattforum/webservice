Assignment01
# webservice 
<b> Prerequisities for building and deploying application: </b>

You will require Python installed, with an IDE of your choice and POSTMAN to test the API endpoint.
# Install Dependencies

```bash
$ python3 -m venv env
$ source env/bin/activate
(env) $ pip install -r requirements.txt
```

# Run Application

```bash
(env) $ flask run
```

# Run Application

```bash
(env) $ pytest
```

# Access Health Check via POSTMAN

Set it to GET and enter the URL below

GET - http://127.0.0.1:5000/healthz

# Github Workflow Actions

Code under `.github/workflows/python-app.yml`

It installs dependencies and run the test on commit on `main` branch

You can check the status on github portal and "Actions" Tab