from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allows browser-based graders to call this endpoint

API_KEY = "ak_mqstxggts397vqf50xb313n6"
EMAIL = "23f3000791@ds.study.iitm.ac.in"  # Replace this!

@app.route("/analytics", methods=["POST"])
def analytics():
    # 1. Check authentication
    provided_key = request.headers.get("X-API-Key")

    if provided_key != API_KEY:
        return jsonify({"error": "Unauthorized"}), 401

    # 2. Read the event batch
    body = request.get_json(silent=True)

    if not body or "events" not in body:
        return jsonify({"error": "Invalid request body"}), 400

    events = body["events"]

    # 3. Calculate the required analytics
    total_events = len(events)

    users = set()
    revenue = 0.0
    positive_totals = {}

    for event in events:
        user = event.get("user")
        amount = event.get("amount", 0)

        if user is not None:
            users.add(user)

        if isinstance(amount, (int, float)) and amount > 0:
            revenue += amount
            positive_totals[user] = positive_totals.get(user, 0) + amount

    unique_users = len(users)

    # The grader guarantees no tie, so max() is safe
    top_user = max(positive_totals, key=positive_totals.get)

    # 4. Return the response
    return jsonify({
        "email": EMAIL,
        "total_events": total_events,
        "unique_users": unique_users,
        "revenue": revenue,
        "top_user": top_user
    })
