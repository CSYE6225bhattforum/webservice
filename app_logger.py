import logging


logger = logging.getLogger()
#logging.basicConfig(filename='C:/Users/foram/OneDrive/Desktop/csye6225.log', encoding='utf-8', level=logging.INFO)
logging.basicConfig(
    filename='/home/ec2-user/csye6225.log', 
    level=logging.INFO,
    format='%(asctime)s: %(levelname)s: %(message)s'
)