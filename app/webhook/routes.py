from flask import Blueprint, jsonify, request
from app.extensions import mongo


webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')

def push(payload):
    return {
        "request_id": payload["head_commit"]["id"],
        "author": payload["pusher"]["name"],
        "action": "PUSH",
        "from_branch": None,  
        "to_branch": payload["ref"].split("/")[-1],
        "timestamp": payload["head_commit"]["timestamp"]
    }

def pull_request(payload):
    pr = payload["pull_request"]
    is_merged = pr.get("merged", False)
    action_type = payload.get("action")

    return {
        "request_id": str(pr["id"]),
        "author": pr["user"]["login"],
        "action": "MERGE" if is_merged else "PULL_REQUEST",
        "from_branch": pr["head"]["ref"],
        "to_branch": pr["base"]["ref"],
        "timestamp": pr["created_at"] if action_type == "opened" else pr.get("merged_at")
    }

@webhook.route('/receiver', methods=["POST"])
def receiver():
    payload = request.json
    event = request.headers.get('X-GitHub-Event')

    if event == "push":
        doc = push(payload)
    elif event == "pull_request":
        doc = pull_request(payload)
    else:
        return jsonify({"status": "ignored"}), 200


    mongo.db.events.insert_one(doc)
    return jsonify({"status": "stored"}), 200

@webhook.route('/events', methods=["GET"])
def get_events():
    events = list(mongo.db.events.find({}, {"_id": 0}).sort("timestamp", -1))
    return jsonify(events)