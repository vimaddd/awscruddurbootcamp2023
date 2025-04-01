from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin
import os
import sys
from flask import Flask, request, jsonify  # jsonify eklenmeli

from services.home_activities import *
from services.notification_activities import *
from services.user_activities import *
from services.create_activity import *
from services.create_reply import *
from services.search_activities import *
from services.message_groups import *
from services.messages import *
from services.create_message import *
from services.show_activity import *
from flask_cors import CORS, cross_origin

from lib.cognito_verification_token import CognitoTokenVerification , extract_access_token, TokenVerifyError
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

 #X RAY----
""" from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware """
# Initialize tracing and an exporter that can send data to Honeycomb
provider = TracerProvider()
processor = BatchSpanProcessor(OTLPSpanExporter())
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)

app = Flask(__name__)

FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()


cognito_verification_token = CognitoTokenVerification(
  user_pool_id=os.getenv("AWS_COGNITO_USER_POOL_ID"),
  user_pool_client_id=os.getenv("AWS_COGNITO_USER_POOL_CLIENT_ID"),
  region="us-east-1"
)
""" xray_url = os.getenv("AWS_XRAY_URL")
xray_recorder.configure(service='backend-flask', dynamic_naming=xray_url)
XRayMiddleware(app, xray_recorder)
 """

frontend = os.getenv('FRONTEND_URL')
backend = os.getenv('BACKEND_URL')
origins = [frontend, backend]


@app.route("/api/message_groups", methods=['GET'])
def data_message_groups():
  user_handle  = 'andrewbrown'
  model = MessageGroups.run(user_handle=user_handle)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200

@app.route("/api/messages/@<string:handle>", methods=['GET'])
def data_messages(handle):
  user_sender_handle = 'andrewbrown'
  user_receiver_handle = request.args.get('user_reciever_handle')

  model = Messages.run(user_sender_handle=user_sender_handle, user_receiver_handle=user_receiver_handle)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200
  return

@app.route("/api/messages", methods=['POST','OPTIONS'])
@cross_origin()
def data_create_message():
  user_sender_handle = 'andrewbrown'
  user_receiver_handle = request.json['user_receiver_handle']
  message = request.json['message']

  model = CreateMessage.run(message=message,user_sender_handle=user_sender_handle,user_receiver_handle=user_receiver_handle)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200
  return

@app.route("/api/activities/home", methods=['GET','OPTIONS'])
@cross_origin(origin='*')
def data_home():
  app.logger.debug('Received request with headers: %s', request.headers)
  access_token = extract_access_token(request.headers)
  try:
    claims = cognito_verification_token.verify(access_token)
    print(claims)

  except TokenVerifyError as e:
    print(e)

    _ = request.data
  app.logger.debug(
  request.headers.get('Authorization'))
  print(

  request.headers.get('Authorization')
  )
  data = HomeActivities.run()
  return data, 200




@app.route("/api/activities/notifications", methods=['GET'])
def data_notifications():
  data = NotificationsActivities.run()
  return data, 200


@app.route("/api/activities/@<string:handle>", methods=['GET'])
def data_handle(handle):
  model = UserActivities.run(handle)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200

@app.route("/api/activities/search", methods=['GET'])
def data_search():
  term = request.args.get('term')
  model = SearchActivities.run(term)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200
  return

@app.route("/api/activities", methods=['POST','OPTIONS'])
@cross_origin()
def data_activities():
    print("DEBUG: /api/activities endpointine istek geldi")  # Debug log
    
    try:
        # 1. JSON verisi kontrolü
        if not request.is_json:
            print("DEBUG: Request is not JSON")
            return jsonify({"error": "Request must be JSON"}), 400
            
        data = request.get_json()
        print(f"DEBUG: Alınan veri: {data}")  # Gelen veriyi logla
        
        # 2. Zorunlu alan kontrolü
        required_fields = ['message', 'ttl']
        if not all(field in data for field in required_fields):
            missing = [f for f in required_fields if f not in data]
            print(f"DEBUG: Eksik alanlar: {missing}")
            return jsonify({"error": f"Missing required fields: {missing}"}), 400

        # 3. Aktivite oluşturma
        print("DEBUG: CreateActivity.run() çağrılıyor")
        model = CreateActivity.run(
            message=data['message'],
            user_handle='vimad',
            ttl=data['ttl']
        )
        print(f"DEBUG: Model döndü: {model}")

        # 4. Hata kontrolü
        if model.get('errors'):
            print(f"DEBUG: Model hataları: {model['errors']}")
            return jsonify({"errors": model['errors']}), 422
            
        # 5. Başarılı yanıt
        print("DEBUG: Aktivite başarıyla oluşturuldu")
        return jsonify(model.get('data', {})), 200
        
    except Exception as e:
        print(f"DEBUG: Beklenmeyen hata: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500
@app.route("/api/activities/<string:activity_uuid>", methods=['GET'])
def data_show_activity(activity_uuid):
  data = ShowActivity.run(activity_uuid=activity_uuid)
  return data, 200

@app.route("/api/activities/<string:activity_uuid>/reply", methods=['POST','OPTIONS'])
@cross_origin()
def data_activities_reply(activity_uuid):
  user_handle  = 'andrewbrown'
  message = request.json['message']
  model = CreateReply.run(message, user_handle, activity_uuid)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200
  return

if __name__ == "__main__":
  app.run(debug=True)