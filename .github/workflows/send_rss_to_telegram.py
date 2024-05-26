import requests
import os
import feedparser
from datetime import datetime

# Telegram API credentials
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

def fetch_rss_feed(url):
    return feedparser.parse(url)

def send_to_telegram(chat_id, message):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    payload = {'chat_id': chat_id, 'text': message, 'parse_mode': 'HTML'}
    requests.post(url, data=payload)

def main():
    rss_chat_map = dict(item.split(":") for item in os.getenv('RSS_FEEDS_CHAT_IDS').split(','))
    
    for feed_url, chat_id in rss_chat_map.items():
        feed = fetch_rss_feed(feed_url.strip())
        
        for entry in feed.entries:
            title = entry.title
            link = entry.link
            published = entry.get('published', 'No publication date')
            description = entry.get('description', 'No description')
            # Format the message with HTML
            message = (f"<b>Title:</b> {title}\n"
                       f"<b>Link:</b> <a href='{link}'>{link}</a>\n"
                       f"<b>Published:</b> {published}\n"
                       f"<b>Description:</b> {description}")
            send_to_telegram(chat_id.strip(), message)

if __name__ == '__main__':
    main()
