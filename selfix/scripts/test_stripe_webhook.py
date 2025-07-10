import json
import requests

# Replace this with your actual backend URL
WEBHOOK_URL = "http://localhost:8000/api/stripe-webhook"

# Simulated Stripe event payload
event_data = {
  "id": "evt_test_checkout_success",
  "object": "event",
  "type": "checkout.session.completed",
  "data": {
    "object": {
      "id": "cs_test_checkout_session",
      "object": "checkout.session",
      "customer_email": "client@example.com",
      "amount_total": 29900,
      "currency": "usd",
      "payment_status": "paid"
    }
  }
}

headers = {
    "Content-Type": "application/json",
    # Optional: you can include the Stripe signature if your backend verifies it
    # "Stripe-Signature": "t=...,v1=..."
}

print(f"📡 Sending test webhook to {WEBHOOK_URL}...")
response = requests.post(WEBHOOK_URL, data=json.dumps(event_data), headers=headers)

print("✅ Response:")
print(response.status_code)
print(response.text)
