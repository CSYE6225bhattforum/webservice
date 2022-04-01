from flask import Flask

from flask import Flask, request, Blueprint
from flask_httpauth import HTTPBasicAuth

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from email_validator import validate_email, EmailNotValidError
from password_validation import PasswordPolicy

from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates

app = Flask(__name__)

# Connection credentials
db_user = 'root'

# database config
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Foram@711'
app.config['MYSQL_DATABASE_DB'] = 'test'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

db = SQLAlchemy(app)

# serializer
ma = Marshmallow(app)

# flask auth supporter
auth = HTTPBasicAuth()

# password hashing
bcrypt = Bcrypt()


# User Database Model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
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


# Health check GET API
@app.route("/health", methods=['GET'])
def health():
    return "200: Service is healthy and running ", 200


if __name__ == '__main__':
    #app.run(debug=True,host="0.0.0.0",port="8080")
    app.run(debug=True,host='0.0.0.0', port=8080)
