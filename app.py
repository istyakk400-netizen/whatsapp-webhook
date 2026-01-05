from flask import Flask, request
import requests
import os

app = Flask(__name__)

VERIFY_TOKEN = "verifytoken123"
WHATSAPP_TOKEN = os.environ.get("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.environ.get("PHONE_NUMBER_ID")

@app.route("/webhook", methods=["GET", "POST"])
def webhook():

    if request.method == "GET":
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if mode == "subscribe" and token == VERIFY_TOKEN:
            return challenge, 200
        else:
            return "Forbidden", 403

    if request.method == "POST":
        data = request.get_json()
        try:
            entry = data["entry"][0]
            changes = entry["changes"][0]
            value = changes["value"]

            if "messages" in value:
                msg = value["messages"][0]
                text = msg["text"]["body"].lower()
                sender = msg["from"]

                if "auto" in text:
                    reply = "📘 1000+ WhatsApp Auto-Reply Templates (Hindi)\nPrice: ₹299\nReply BUY to get link"
                elif "hi" in text or "hello" in text:
                    reply = "👋 Namaste! AUTO likhiye details ke liye."
                else:
                    reply = "🙏 Thanks! AUTO likhiye details ke liye."

                send_message(sender, reply)

        except Exception as e:
            print(e)

        return "EVENT_RECEIVED", 200


def send_message(to, message):
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": message}
    }
    requests.post(url, headers=headers, json=payload)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
