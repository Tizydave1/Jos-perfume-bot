from flask import Flask, request
import requests

app = Flask(__name__)

VERIFY_TOKEN = "josperfume123"
PAGE_ACCESS_TOKEN = "YOUR_FACEBOOK_PAGE_TOKEN_HERE"
WHATSAPP_NUMBER = "2348084831989"
SHOP_NAME = "Jos Perfume Shop"

SHOP_ADDRESS = """📍 BRANCH 1 (Main): ECWA Plaza, Challenge Bookshop Junction, Opp Medical Students Hostel, by the Railway, Jos
📍 BRANCH 2: Area 1 Junction, Rayfield, Jos"""

PRODUCTS = f"""
🔥 {SHOP_NAME} - Available Now:

1. Dior Sauvage - N25,000
2. Bleu de Chanel - N24,000
3. Lattafa Asad - N18,000
4. Oud Wood - N20,000
5. Aventus Creed - N30,000

{SHOP_ADDRESS}
⏰ Open: 9AM - 6PM Daily
🚚 Delivery in Jos: N1,500 (Same Day)

To order, chat us on WhatsApp!
"""

def send_message(recipient_id, text):
    url = f"https://graph.facebook.com/v18.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"
    payload = {"recipient": {"id": recipient_id}, "message": {"text": text}}
    requests.post(url, json=payload)

@app.route("/webhook", methods=["GET"])
def verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    return "Forbidden", 403

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    if data['object'] == 'page':
        for entry in data['entry']:
            for ev in entry.get('messaging', []):
                if 'message' in ev:
                    sender_id = ev['sender']['id']
                    txt = ev['message'].get('text','').lower()
                    if any(w in txt for w in ['hi','hello','price','perfume','menu','how much','location','address','open','branch','rayfield','challenge']):
                        reply = f"Hello! Welcome to {SHOP_NAME} 😊\n\n{PRODUCTS}\n\nWhatsApp: https://wa.me/{WHATSAPP_NUMBER}"
                    else:
                        reply = f"{PRODUCTS}\n\nOrder via WhatsApp: https://wa.me/{WHATSAPP_NUMBER}"
                    send_message(sender_id, reply)
    return "OK", 200

@app.route("/")
def home():
    return "Jos Perfume Bot is Live! 2 Branches"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
