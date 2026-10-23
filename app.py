from flask import Flask, request
import os
import requests

app = Flask(__name__)

VERIFY_TOKEN = "jos_perfume_verify_2024"
PAGE_ACCESS_TOKEN = os.environ.get("PAGE_ACCESS_TOKEN", "")

PERFUMES = [
    {"id": 1, "name": "Dior Sauvage", "price": "₦15,000", "stock": 20},
    {"id": 2, "name": "Bleu de Chanel", "price": "₦18,000", "stock": 15},
    {"id": 3, "name": "Creed Aventus", "price": "₦25,000", "stock": 10},
    {"id": 4, "name": "Oud Wood", "price": "₦20,000", "stock": 12},
    {"id": 5, "name": "Acqua Di Gio", "price": "₦16,500", "stock": 18},
]

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if mode == "subscribe" and token == VERIFY_TOKEN:
            print("WEBHOOK VERIFIED!")
            return challenge, 200
        return "Verification failed", 403
    
    # POST - receive messages
    data = request.get_json()
    if data and data.get('object') == 'page':
        for entry in data.get('entry', []):
            for event in entry.get('messaging', []):
                if 'message' in event:
                    sender_id = event['sender']['id']
                    text = event['message'].get('text','').lower()
                    handle_message(sender_id, text)
    return "ok", 200

def handle_message(sender_id, text):
    if any(x in text for x in ["perfume", "list", "buy", "hi", "hello"]):
        reply = "🌸 *Jos Perfumes - Available Now:*\n\n"
        for p in PERFUMES:
            reply += f"{p['id']}. {p['name']} - {p['price']} ({p['stock']} left)\n"
        reply += "\nReply with number to order, e.g. '1'"
    else:
        reply = "Hi! Welcome to Jos Perfumes 😊 Type 'perfumes' to see our list."
    send_message(sender_id, reply)

def send_message(recipient_id, message_text):
    if not PAGE_ACCESS_TOKEN:
        print("No PAGE_ACCESS_TOKEN set")
        return
    url = f"https://graph.facebook.com/v19.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"
    payload = {"recipient": {"id": recipient_id}, "message": {"text": message_text}}
    requests.post(url, json=payload)

@app.route('/', methods=['GET'])
def home():
    return "Jos Perfume Bot Live - Ready for Facebook", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
