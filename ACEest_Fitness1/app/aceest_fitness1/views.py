from flask import Blueprint, jsonify, request, abort, current_app

main_bp = Blueprint('main', __name__)

# In-memory data store (mock DB)
members = [
    {"id": 1, "name": "Alice", "membership": "premium"},
    {"id": 2, "name": "Bob", "membership": "standard"}
]

@main_bp.route("/")
def index():
    return jsonify({
        "service": "ACEest Fitness API",
        "version": current_app.config.get("VERSION", "v1.0")
    })

@main_bp.route("/members", methods=["GET"])
def list_members():
    return jsonify(members)

@main_bp.route("/members/<int:mid>", methods=["GET"])
def get_member(mid):
    for m in members:
        if m["id"] == mid:
            return jsonify(m)
    abort(404, description="Member not found")

@main_bp.route("/members", methods=["POST"])
def add_member():
    if not request.is_json:
        abort(400, description="JSON required")
    data = request.get_json()
    if "name" not in data or "membership" not in data:
        abort(400, description="name and membership required")
    new_id = max([m["id"] for m in members]) + 1
    m = {"id": new_id, "name": data["name"], "membership": data["membership"]}
    members.append(m)
    return jsonify(m), 201
