# python send_rss_palavra_to_telegram.py
import os
import requests
import xml.etree.ElementTree as ET

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN_PALAVRADODIA')
RSS_FEED_URL = os.getenv('RSS_FEED_URL')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'HTML'
    }
    response = requests.post(url, data=payload)
    return response.json()

def parse_rss_feed(url):
    response = requests.get(url)
    root = ET.fromstring(response.content)
    items = []
    for item in root.findall('./channel/item'):
        title = item.find('title').text
        link = item.find('link').text
        description = item.find('description').text
        items.append({
            'title': title,
            'link': link,
            'description': description
        })
    print(f"Parsed {len(items)} items from RSS feed: {url}")
    return items

def parse_json_feed(url):
    response = requests.get(url)
    data = response.json()
    items = []
    for item in data['items']:
        title = item.get('title', 'No title')
        link = item.get('url', item.get('link', 'No link'))
        description = item.get('summary', item.get('description', 'No description'))
        items.append({
            'title': title,
            'link': link,
            'description': description
        })
    print(f"Parsed {len(items)} items from JSON feed: {url}")
    return items

def main():
    print(f"Processing feed: {RSS_FEED_URL} for chat ID: {CHAT_ID}")
    if RSS_FEED_URL.endswith('.json'):
        items = parse_json_feed(RSS_FEED_URL)
    else:
        items = parse_rss_feed(RSS_FEED_URL)
    
    for item in items:
        message = f"<b>{item['title']}</b>\n{item['link']}\n{item['description']}"
        print(f"Sending message to chat ID {CHAT_ID}: {message}")
        send_message(CHAT_ID, message)

if __name__ == '__main__':
    main()
