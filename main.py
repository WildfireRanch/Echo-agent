import requests
import time
import hashlib
import hmac

@app.route("/phemex/account", methods=["GET"])
def phemex_account():
    try:
        # Load API credentials from environment variables
        api_key = os.getenv("PHEMEX_API_KEY")
        api_secret = os.getenv("PHEMEX_API_SECRET")

        # Set up the API request
        timestamp = str(int(time.time() * 1000))
        endpoint = "/accounts/accountPositions"
        signature_payload = f"{timestamp}GET{endpoint}".encode()
        signature = hmac.new(api_secret.encode(), signature_payload, hashlib.sha256).hexdigest()

        url = f"https://api.phemex.com{endpoint}"
        headers = {
            "x-phemex-access-token": api_key,
            "x-phemex-request-signature": signature,
            "x-phemex-request-expiry": timestamp,
        }

        response = requests.get(url, headers=headers)
        data = response.json()

        return jsonify({"status": "success", "account_data": data})
    except Exception as e:
        return jsonify({"error": str(e)})
