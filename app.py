import uuid
import os

from flask import Flask


from flask import Flask, request
from flask_httpauth import HTTPBasicAuth

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from email_validator import validate_email, EmailNotValidError
from password_validation import PasswordPolicy

from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates

from config import AppConfig
from s3config import delete_image, upload_file
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config.from_object(AppConfig)

db = SQLAlchemy(app)

# serializer
ma = Marshmallow(app)

# flask auth supporter
auth = HTTPBasicAuth()

# password hashing
bcrypt = Bcrypt()


# User Database Model
class Users(db.Model):
    id = db.Column(
        db.String(255), primary_key=True, 
        index=True, unique=True, default=uuid.uuid4
    )
    username = db.Column(db.String(255), unique=True, index=True)
    _password = db.Column("password", db.String(128), nullable=False)

    first_name = db.Column(db.String(255), nullable=False, index=True)
    last_name = db.Column(db.String(255), nullable=False, index=True)

    account_created = db.Column(
        db.DateTime,
        default=db.func.current_timestamp()
    )
    account_updated = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )

    def __repr__(self):
        return f'<Users {self.username}>'

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        policy = PasswordPolicy()
        # validating password with password validator
        if not policy.validate(password):
            # password set against policy is weak password
            # https://pypi.org/project/Password-Validation/
            raise ValueError("Weak password")
        
        # generate hash for given plaintext password to store
        # in model hidden field _password
        self._password = self.generate_hash(password)

    @staticmethod
    def generate_hash(password):
        return bcrypt.generate_password_hash(password).decode("UTF-8")

    def check_password(self, password):
        # check given plaintext password against stored hashed password
        return bcrypt.check_password_hash(self._password, password)

    @validates("username")
    def check_email(self, key, username):
        try:
            valid = validate_email(username.strip())
            return valid.email

        except EmailNotValidError:
            raise ValueError("Invalid email")


class Images(db.Model):

    id = db.Column(
        db.String(255), primary_key=True, 
        index=True, default=uuid.uuid4
    )
    user_id = db.Column(db.String(255), nullable=False, index=True)
    filename = db.Column(db.String(255), nullable=False, index=True)
    url = db.Column(db.String(255), unique=True, index=True)
    upload_date = db.Column(db.Date, default=db.func.now())


# Create models in database
db.create_all()
db.session.commit()


# User Serializer
class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        # excludes the hidden password field
        # hybrid properties are not involved in serializer response 
        exclude = ("_password",)
        model = Users

user_schema = UserSchema()


# Flask HTTP authenticator
@auth.verify_password
def authenticate(username, password):
    # fetch user based on username sent in basic auth
    user = db.session.query(Users).filter_by(username=username).first()
    if user and user.check_password(password):
        # when user is found and the hased password is verified with
        # basic auth's password, it returns user object 
        return user
    # if above checks are failed, returning false here will return 
    # 401 - unauthorized access from login_required decorator
    return False


# Non-authenticated create user POST API
@app.route("/v1/user", methods=['POST'])
def create_user():
    """Returns created user or validation error message."""

    try:
        # creates user object
        user = Users(
            username=request.json['username'],
            first_name=request.json['first_name'],
            last_name=request.json['last_name'],
            password=request.json['password']
        )
        # add user object to database session
        db.session.add(user)
        # commit the object to database from session
        db.session.commit()
        return user_schema.dump(user), 201
    except KeyError as e:
        # validation error from missing request.json required fields
        return f"Required Field: {e}", 400
    except ValueError as e:
        # validation error from model (password, email)
        return f"Validation: {e}", 400
    except Exception as e:
        # generalized error
        return f"Bad Request: {e}", 400


# User authenticated GET, PUT API
@app.route("/v1/user/self", methods=['GET', 'PUT'])
# login wall/decorator to guide unauthorized access
@auth.login_required
def authenticated_user():
    """Returns authenticated stored or updated user details."""

    try:
        # current_user returns user object as returned from authenticator
        user = auth.current_user()
        if request.method == "PUT":
            # user can only edit these field
            allowed_edit_fields = ["first_name", "last_name", "password"]

            for key in request.json:
                if key in allowed_edit_fields:
                    # update db user object with new value from request body
                    setattr(user, key, request.json[key])

            # commit above changes to user in database
            db.session.commit()

        # Returns the user using model serializer
        return user_schema.dump(user), 200
    except Exception as e:
        return f"Bad Request: {e}", 400


# Image Serializer
class ImageSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Images

image_schema = ImageSchema()


# User Image authenticated GET API
@app.route("/v1/user/self/pic", methods=['GET'])
# login wall/decorator to guide unauthorized access
@auth.login_required
def get_user_image():
    """Returns authenticated stored user image details."""

    try:
        # current_user returns user object as returned from authenticator
        user = auth.current_user()
        image = db.session.query(Images).filter_by(user_id=user.id).first()
        if image:
            return image_schema.dump(image), 200
        return "Not Found", 404
    except Exception as e:
        return f"Bad Request: {e}", 400


# User Image authenticated POST API
@app.route("/v1/user/self/pic", methods=['POST'])
# login wall/decorator to guide unauthorized access
@auth.login_required
def create_user_image():
    """Returns uploaded user image details."""

    try:
        # current_user returns user object as returned from authenticator
        user = auth.current_user()

        # fetch file
        file = request.files['file']
        filename = secure_filename(file.filename)
        url, status = upload_file(file, f"{user.id}/{filename}")
        if status != 200:
            # then url var contains error message
            return url, status

        # get or create image object for database
        image = db.session.query(Images).filter_by(user_id=user.id).first()
        if not image:
            image = Images(user_id=user.id)
        else:
            message, status = delete_image(f"{user.id}/{image.filename}")
            db.session.delete(image)
            db.session.commit()
            image = Images(user_id=user.id)
        
        image.filename = filename
        image.url = url
        # add image object to database session
        db.session.add(image)
        # commit the object to database from session
        db.session.commit()
        return image_schema.dump(image), 201
    except Exception as e:
        # generalized error
        return f"Bad Request: {e}", 400


# User Image authenticated DELETE API
@app.route("/v1/user/self/pic", methods=['DELETE'])
# login wall/decorator to guide unauthorized access
@auth.login_required
def user_delete_image():
    """Returns user image delete confirmation."""

    try:
        # current_user returns user object as returned from authenticator
        user = auth.current_user()
        image = db.session.query(Images).filter_by(user_id=user.id).first()
        if not image:
            return "Not Found", 404
        
        message, status = delete_image(f"{user.id}/{image.filename}")
        if status != 204:
            return message, status
        if status ==204:
            #deleting image from database
            db.session.delete(image)
            db.session.commit()
            return message, status

    except Exception as e:
        return f"Bad Request: {e}", 400


# Health check GET API
@app.route("/healthz", methods=['GET'])
def health():
    return "200: Service is healthy and running ", 200


if __name__ == '__main__':
    #app.run(debug=True,host="0.0.0.0",port="8080")
    app.run(debug=True,host='0.0.0.0', port=8080)
