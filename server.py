from flask import Flask, request, jsonify
import json, time, os

app = Flask(__name__)

LEDGER_FILE = "ledger.json"

# Load or create ledger
if not os.path.exists(LEDGER_FILE):
    with open(LEDGER_FILE, "w") as f:
        json.dump({"blocks": []}, f, indent=2)

def load_ledger():
    with open(LEDGER_FILE, "r") as f:
        return json.load(f)

def save_ledger(data):
    with open(LEDGER_FILE, "w") as f:
        json.dump(data, f, indent=2)

@app.route("/submit", methods=["POST"])
def submit_block():
    data = request.json
    ledger = load_ledger()
    block = {
        "miner": data.get("miner"),
        "sig": data.get("sig"),
        "ts": time.time(),
        "focus": data.get("focus"),
        "rt": data.get("rt")
    }
    ledger["blocks"].append(block)
    save_ledger(ledger)
    return jsonify({"status": "success", "blocks": len(ledger["blocks"])})

@app.route("/ledger", methods=["GET"])
def get_ledger():
    return jsonify(load_ledger())

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "NeuroChain Node Running", "blocks": len(load_ledger()["blocks"])})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
