import os
import json
import requests
from telegram import Bot

API_EVENTS = "https://api.coingecko.com/api/v3/events"
STATE_FILE = "seen_airdrops.json"
BOT = Bot(token=os.getenv('TG_BOT_TOKEN'))
CHAT_ID = os.getenv('TG_CHAT_ID')

if os.path.exists(STATE_FILE):
    with open(STATE_FILE, 'r') as f:
        seen = set(json.load(f))
else:
    seen = set()

resp = requests.get(API_EVENTS, params={'type': 'airdrop'})
data = resp.json().get('data', [])

new_ids = []
for ev in data:
    ev_id = ev.get('id')
    if ev_id not in seen:
        new_ids.append(ev_id)
        title = ev.get('title')
        date = ev.get('start_date')
        link = ev.get('website') or ev.get('twitter_event_url') or ''
        msg = f"🚀 ایردراپ جدید:\n*{title}*\n📅 شروع: {date}\n🔗 {link}"
        BOT.send_message(chat_id=CHAT_ID, text=msg, parse_mode='Markdown')

if new_ids:
    seen.update(new_ids)
    with open(STATE_FILE, 'w') as f:
        json.dump(list(seen), f)
