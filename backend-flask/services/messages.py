from datetime import datetime, timedelta, timezone
from lib.ddb import Ddb
from lib.db import db

class Messages:
  def run(message_group_uuid,cognito_user_id):
    model = {
      'errors': None,
      'data': None
    }


    # TODO: we're suppose to check that we have permission to access
    # this message_group_uuid, its missing in our access pattern.

    ddb = Ddb.client()
    data = Ddb.list_messages(ddb, message_group_uuid)
    print("list_messages:",data)

    model['data'] = data
    return model