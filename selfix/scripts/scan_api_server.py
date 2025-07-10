from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/api/scan', methods=['POST'])
def scan():
    # Simulate scan trigger logic
    print("[🧪] Scan triggered.")
    return jsonify({"status": "Scan started"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
