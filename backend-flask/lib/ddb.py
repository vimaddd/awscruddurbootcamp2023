import boto3
import sys
from datetime import datetime, timedelta, timezone
import uuid
import os
import botocore.exceptions

class Ddb:
  def client():
    endpoint_url = os.getenv("https://dynamodb.us-east-1.amazonaws.com")
    if endpoint_url:
      attrs = { 'endpoint_url': endpoint_url }
    else:
      attrs = {}
    dynamodb = boto3.client(
      'dynamodb',
      **attrs,
      region_name='us-east-1',
      aws_access_key_id="[REMOVED]",
      aws_secret_access_key="[REMOVED]")
    return dynamodb
  def list_message_groups(client,my_user_uuid):
    year = str(datetime.now().year)
    table_name = 'cruddur-message'
    query_params = {
      'TableName': table_name,
      'KeyConditionExpression': 'pk = :pk ',
      'ScanIndexForward': False,
      'Limit': 20,
      'ExpressionAttributeValues': {
        ':pk': {'S': 'GRP#3c92c388-b40f-4de9-8c06-c1994f70fdee'}
      }
    }
    print('query-params:',query_params)
    print(query_params)
    # query the table
    response = client.query(**query_params)
    items = response['Items']
    results = []
    for item in items:
      last_sent_at = item['sk']['S']
      results.append({
        'uuid': item['message_group_uuid']['S'],
        'display_name': item['user_display_name']['S'],
        'handle': item['user_handle']['S'],
        'message': item['message']['S'],
        'created_at': last_sent_at
      })
    return results
  def list_messages(client,message_group_uuid):
      current_year = datetime.now().year
      table_name = 'cruddur-message'
      query_params = {
        'TableName': table_name,
        'KeyConditionExpression': 'pk = :pk ',
        'ScanIndexForward': False,
        'Limit': 40,
        'ExpressionAttributeValues': {
          ':pk': {'S': "MSG#5ae290ed-55d1-47a0-bc6d-fe2bc2700399"}
        }
      }

      response = client.query(**query_params)
      items = response['Items']
      items.reverse()
      
      results = []
      for item in items:
        created_at = item['sk']['S']
        results.append({
          'uuid': item['message_uuid']['S'],
          'display_name': item['user_display_name']['S'],
          'handle': item['user_handle']['S'],
          'message': item['message']['S'],
          'created_at': created_at
        })
      print("EEE")
      print(results)
      return results
  def create_message(client,message_group_uuid, message, my_user_uuid, my_user_display_name, my_user_handle):
    now = datetime.now(timezone.utc).astimezone().isoformat()
    created_at = now
    message_uuid = str(uuid.uuid4())

    record = {
      'pk':   {'S': f"MSG#{message_group_uuid}"},
      'sk':   {'S': created_at },
      'message': {'S': message},
      'message_uuid': {'S': message_uuid},
      'user_uuid': {'S': my_user_uuid},
      'user_display_name': {'S': my_user_display_name},
      'user_handle': {'S': my_user_handle}
    }
    # insert the record into the table
    table_name = 'cruddur-messages'
    response = client.put_item(
      TableName=table_name,
      Item=record
    )
    # print the response
    print(response)

    return {
      'message_group_uuid': message_group_uuid,
      'uuid': my_user_uuid,
      'display_name': my_user_display_name,
      'handle':  my_user_handle,
      'message': message,
      'created_at': created_at
    }    