import json

from flask import Flask, json, request
from flask_cors import CORS

from server.phishing.schema import Text
from server.phishing.service import Service as service

app = Flask(__name__)
CORS(app)


@app.route("/phishing/text", methods=["POST"])
def processText():
    text = Text().load(json.loads(request.data))
    print(text)
    payload = text.data
    print(payload)
    print(payload.get('email_address'))
    if payload.get('errors'):
        return json_response({'error': text.errors}, 422)
    response = None
    if payload.get('email_address'):
        response = service.processEmail(payload)
    else:
        response = service.processText(payload)
    print(response)
    return json_response(response)


def json_response(payload, status=200):
    return json.dumps(payload), status, {'content-type': 'application/json'}
