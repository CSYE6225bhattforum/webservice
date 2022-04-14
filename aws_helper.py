import json
from multiprocessing.connection import Client
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
import datetime

from app_config import config
from app_logger import logger


class S3Client:

    ALLOWED_EXTENSIONS = ["png", "jpg", "jpeg"]

    def __init__(self):
        self.s3 = boto3.client('s3')

    def allowed_extension(self, filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in self.ALLOWED_EXTENSIONS

    def upload_file(self, file, path):
        try:
            if not file:
                return "File was not found", 404

            if self.allowed_extension(path):
                self.s3.upload_fileobj(file, config.BUCKET, path)
                url = f"https://{config.BUCKET}.s3.amazonaws.com/{path}"
                return url, 200
            else:
                return "Extension not allowed", 400
        except FileNotFoundError:
            return "File was not found", 404
        except NoCredentialsError:
            return "Credentials not available", 500
        except Exception as e:
            return f"failed uploading image: {e}", 500

    def delete_image(self, path):
        try:
            self.s3.delete_object(Bucket=config.BUCKET, Key=path)
            return "Deleted", 204
        except Exception as e:
            return f"failed deleting image: {e}", 500


class SNSClient:

    TOPICARN = None

    def __init__(self, topicarn=None):
        self.topicarn = topicarn if topicarn else config.SNS_TOPIC_ARN
        self.sns = boto3.client('sns', region_name="us-east-1")

    def publish_message(self, message):
        try:
            return self.sns.publish(
                TopicArn=self.topicarn,
                Message=json.dumps(message),
                MessageStructure='string'
            )
        except ClientError:
            logger.exception(f'failed to publish message')
            raise
        except Exception as e:
            logger.exception(f'failed to publish message: {e}')
            raise


class DynamoDBClient:

    def __init__(self, tablename=None):
        
        if not tablename:
            tablename = config.DYNAMODB_USER_TABLE
        
        self.dynamodb = boto3.resource('dynamodb', region_name="us-east-1")
        self.table = self.dynamodb.Table(tablename)

    def set_user_key(self, username):
        self.user_key = {'username': username}

    def get_user_item(self):
        item = self.table.get_item(Key=self.user_key)
        return item.get("Items", {})

    def put_user_item(self, token):
        # if not self.get_user_item():
        #     return False

        put_key = self.user_key
        put_key["token"] = token
        # put_key["ttl"] = datetime.datetime.now() + datetime.timedelta(minutes=5)
        return self.table.put_item(Item=put_key)

    def delete_user_item(self):
        self.table.delete_item(Key=self.user_key)