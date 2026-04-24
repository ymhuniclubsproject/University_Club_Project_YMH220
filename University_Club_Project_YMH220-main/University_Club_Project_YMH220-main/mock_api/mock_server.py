from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os

app = Flask(__name__)
# Enable CORS for frontend integration
CORS(app)

# Load mock data
data_path = os.path.join(os.path.dirname(__file__), "mock_data.json")
with open(data_path, "r") as f:
    db = json.load(f)

# --- Authentication ---
@app.route("/api/v1/auth/register", methods=["POST"])
def register():
    data = request.json
    return jsonify({"id": 99, "email": data.get("email"), "full_name": data.get("full_name"), "role": "student"}), 201

@app.route("/api/v1/auth/login", methods=["POST"])
def login():
    return jsonify({"access_token": "mock-jwt-token-123", "token_type": "bearer"}), 200

@app.route("/api/v1/auth/me", methods=["GET"])
def me():
    return jsonify({"id": 1, "email": "student@university.edu", "full_name": "John Doe", "role": "student"}), 200

# --- Clubs ---
@app.route("/api/v1/clubs", methods=["GET", "POST"])
def manage_clubs():
    if request.method == "GET":
        return jsonify(db["clubs"]), 200
    elif request.method == "POST":
        new_club = request.json
        new_club["id"] = len(db["clubs"]) + 1
        db["clubs"].append(new_club)
        return jsonify(new_club), 201

@app.route("/api/v1/clubs/<int:club_id>", methods=["GET", "PUT", "DELETE"])
def club_detail(club_id):
    club = next((c for c in db["clubs"] if c["id"] == club_id), None)
    if not club:
        return jsonify({"error": "Club not found"}), 404
        
    if request.method == "GET":
        return jsonify(club), 200
    elif request.method == "PUT":
        club.update(request.json)
        return jsonify(club), 200
    elif request.method == "DELETE":
        db["clubs"].remove(club)
        return jsonify({"status": "deleted"}), 204

# --- Events ---
@app.route("/api/v1/events", methods=["GET", "POST"])
def manage_events():
    if request.method == "GET":
        return jsonify(db["events"]), 200
    elif request.method == "POST":
        new_event = request.json
        new_event["id"] = len(db["events"]) + 1
        db["events"].append(new_event)
        return jsonify(new_event), 201

@app.route("/api/v1/events/<int:event_id>", methods=["GET", "PUT", "DELETE"])
def event_detail(event_id):
    event = next((e for e in db["events"] if e["id"] == event_id), None)
    if not event:
        return jsonify({"error": "Event not found"}), 404
        
    if request.method == "GET":
        return jsonify(event), 200
    elif request.method == "PUT":
        event.update(request.json)
        return jsonify(event), 200
    elif request.method == "DELETE":
        db["events"].remove(event)
        return jsonify({"status": "deleted"}), 204

# --- User Points ---
@app.route("/api/v1/users/<int:user_id>/points", methods=["GET", "POST"])
def user_points(user_id):
    points = next((p for p in db["points"] if p["user_id"] == user_id), {"user_id": user_id, "total_points": 0, "history": []})
    
    if request.method == "GET":
        return jsonify(points), 200
    elif request.method == "POST":
        awarded = request.json
        points["total_points"] += awarded.get("amount", 0)
        points["history"].append(awarded)
        return jsonify(points), 201

if __name__ == "__main__":
    print("Mock Server running on http://127.0.0.1:8080")
    app.run(port=8080, debug=True)
