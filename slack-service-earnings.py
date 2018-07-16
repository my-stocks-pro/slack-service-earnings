from flask import Flask, request
from flask_cors import CORS
from classSlack import SlackEarningsService
import json

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route("/slack/earnings", methods=['POST'])
def slack_service():
    data = json.loads(request.data)
    # slack.push(location, idi, description)

    location = data.get("location")
    idi = data.get("id")
    description = data.get("description")
    slack.push_test(location, idi, description)

    return "Success"


if __name__ == '__main__':
    slack = SlackEarningsService("config.yaml")
    # slack.message("START -> slack-earnings-service")
    app.run(host=slack.host, port=slack.port)
