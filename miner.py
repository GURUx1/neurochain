import time, json, random, hashlib, requests, os

SERVER_URL = "https://your-render-url.onrender.com/submit"  # 🔹 Replace with your Render URL later

def sign_data(data, secret):
    raw = json.dumps(data) + secret
    return hashlib.sha256(raw.encode()).hexdigest()

def mine_focus_block(username, secret):
    word = random.choice(["neuro", "focus", "wave", "quantum", "mind", "chain"])
    print("\nNeuroChain Focus Task ===")
    print(f"Type the shown word as fast and exactly as you see it:\n>>> {word}")

    start = time.time()
    typed = input("-> ")
    rt = round(time.time() - start, 2)

    if typed.strip() != word:
        print("❌ Incorrect! Try again.")
        return None

    print(f"✅ Focus Proof Completed in {rt}s")
    data = {
        "miner": username,
        "focus": word,
        "rt": rt
    }
    data["sig"] = sign_data(data, secret)

    try:
        r = requests.post(SERVER_URL, json=data, timeout=5)
        print("🧾 Block submitted:", r.json())
    except Exception as e:
        print("⚠️ Offline mode. Block saved locally:", e)
        ledger = json.load(open("ledger.json")) if os.path.exists("ledger.json") else {"blocks": []}
        ledger["blocks"].append(data)
        json.dump(ledger, open("ledger.json", "w"), indent=2)

def main():
    print("=== NeuroChain Miner ===")
    username = input("Enter your miner name: ")
    secret = input("Create a device secret (type something safe): ")

    while True:
        mine_focus_block(username, secret)
        time.sleep(3)

if __name__ == "__main__":
    main()
