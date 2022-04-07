import boto3
from botocore.exceptions import NoCredentialsError

from config import BUCKET


ALLOWED_EXTENSIONS = ["png", "jpg", "jpeg"]


# function to create and return s3 client with config
def get_s3_client():
    return boto3.client('s3')

# function to check file extension
def allowed_extension(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def upload_file(file, path):
    try:
        if not file:
            return "File was not found", 404

        s3 = get_s3_client()
        if allowed_extension(path):
            s3.upload_fileobj(file, BUCKET, path)
            url = f"https://{BUCKET}.s3.amazonaws.com/{path}"
            return url, 200
        else:
            return "Extension not allowed", 400
    except FileNotFoundError:
        return "File was not found", 404
    except NoCredentialsError:
        return "Credentials not available", 500
    except Exception as e:
        return f"failed uploading image: {e}", 500


def delete_image(path):
    try:
        s3 = get_s3_client()
        s3.delete_object(Bucket=BUCKET, Key=path)
        return "Deleted", 204
    except Exception as e:
        return f"failed deleting image: {e}", 500