import os
import json
import logging
import settings
from lib import  connection,rotator

logging.basicConfig(filename=os.environ["OUTPUT_DIR"]+ 'rotator.log' , filemode='a',level=logging.INFO, format='%(asctime)s: %(levelname)s: %(message)s' ,datefmt='%m/%d/%Y %H:%M:%S')

logging.getLogger().setLevel(logging.INFO)

try:
    print("main started")
    iam_client = connection.get_client('iam')
    creds_file = os.environ["creds_file"]
    creds_profile = os.environ["creds_profile"]
    logging.info("Rotating user with credential profile {}".format(creds_profile))
    rotator.rotate_keys(iam_client,creds_profile,creds_file)
    print("main failed")
except Exception as e:
    logging.error("Failing in main file with {}".format(e))
    raise e