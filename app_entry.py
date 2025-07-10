#!/usr/bin/env python3

from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import stripe

# === Load environment variables ===
load_dotenv("/opt/SELFIX/.env")  # Load your .env file
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# === Initialize Flask App ===
app = Flask(__name__)
CORS(app)

# === SYSTEM STATUS ===
@app.route("/", methods=["GET"])
def root():
    return jsonify({"message": "SELFIX backend is running and connected"})

@app.route("/api/healthz", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"})

# === STRIPE PAYMENT ENDPOINT ===
@app.route("/api/pay", methods=["POST"])
def create_payment():
    data = request.get_json()

    required_fields = ["email", "amount", "payment_method_id"]
    if not all(data.get(field) for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        amount_cents = int(float(data["amount"]) * 100)

        intent = stripe.PaymentIntent.create(
            amount=amount_cents,
            currency="usd",
            payment_method=data["payment_method_id"],
            confirmation_method="manual",
            confirm=True,
            receipt_email=data["email"],
        )

        return jsonify({
            "status": "success",
            "payment_intent": intent.id,
            "client_secret": intent.client_secret
        })

    except stripe.error.CardError as e:
        return jsonify({"status": "failed", "error": e.user_message}), 402
    except Exception as e:
        return jsonify({"status": "failed", "error": str(e)}), 500

# === START SERVER ===
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
