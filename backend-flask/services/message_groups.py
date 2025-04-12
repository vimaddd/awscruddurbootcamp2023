from datetime import datetime, timedelta, timezone
from lib.db import db
import os
import sys

current_path = os.path.dirname(os.path.abspath(__file__))
parent_path = os.path.abspath(os.path.join(current_path,'..'))
sys.path.append(parent_path)

from lib.ddb import Ddb
import boto3
import sys
from datetime import datetime, timedelta, timezone
import uuid
import os
import botocore.exceptions

class MessageGroups:
  def run(cognito_user_id):
    model = {
        'errors': None,
        'data': None
      }
    sql = db.template('users','uuid_from_cognito_user_id')
 

    ddb = Ddb.client()

    
    response = Ddb.list_message_groups(ddb,"3c92c388-b40f-4de9-8c06-c1994f70fdee")
    data = response
    print(response)
    model['data'] = data
    return data