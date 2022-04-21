import os
# from dotenv import load_dotenv

# load_dotenv(override=True)

class AppConfig:

    DEBUG = True
    FLASK_ENV = os.environ.get("FLASK_ENV")

    DB_HOST = os.environ.get("DB_HOST")
    DB_USERNAME = os.environ.get("DB_USERNAME")
    DB_PASSWORD = os.environ.get("DB_PASSWORD")
    DB_DATABASENAME = os.environ.get("DB_DATABASE")
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://csye6225:{DB_PASSWORD}@{DB_HOST}/csye6225?ssl_ca=/tmp/certs/global-bundle.pem'
    #SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://csye6225:Foram711@csye6225.cavjyta1ysgv.us-east-1.rds.amazonaws.com'

    #SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://root:root@localhost/test'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MYSQL_DATABASE_USER = DB_USERNAME
    # MYSQL_DATABASE_PASSWORD = 'Foram711' #use when no using local and connecting to aws ec2
    MYSQL_DATABASE_PASSWORD = DB_PASSWORD #use when using/testing to local
    MYSQL_DATABASE_DB = DB_DATABASENAME
    # MYSQL_DATABASE_HOST = 'localhost'
    MYSQL_DATABASE_HOST = DB_HOST

    # AWS
    BUCKET = os.environ.get("AWS_BUCKET_NAME")
    ACCESS_KEY_ID = os.environ.get("ACCESS_KEY_ID")
    SECRET_ACCESS_KEY = os.environ.get("SECRET_ACCESS_KEY")

    # AWS SNS
    # AWS_REGION = os.environ.get("AWS_REGION")
    AWS_REGION = "us-east-1"
    SNS_TOPIC_ARN = "arn:aws:sns:us-east-1:927025957594:csye6225-myTopic"
    DYNAMODB_USER_TABLE = "Account"


config = AppConfig
