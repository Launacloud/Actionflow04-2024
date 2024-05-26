import os
import requests
import json
import xml.etree.ElementTree as ET

# Get environment variables
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN_PALAVRADODIA')
RSS_FEED_URL = os.getenv('RSS_FEED_URLPALAVRADODIA')
CHAT_ID = os.getenv('TELEGRAM_CHAT_IDPALAVRADODIA')

def send_message(message):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    data = {'chat_id': CHAT_ID, 'text': message}
    response = requests.post(url, data=data)
    return response.json()

def fetch_and_send_rss():
    response = requests.get(RSS_FEED_URL)
    if response.status_code == 200:
        content_type = response.headers['content-type']
        if 'application/json' in content_type:
            data = response.json()
            for item in data:
                title = item.get('title')
                link = item.get('link')
                message = f"{title}\n{link}"
                send_message(message)
        elif 'application/xml' in content_type:
            root = ET.fromstring(response.content)
            for item in root.findall('.//item'):
                title = item.find('title').text
                link = item.find('link').text
                message = f"{title}\n{link}"
                send_message(message)
        else:
            send_message("Unsupported content type.")
    else:
        send_message("Failed to fetch RSS feed.")

# Main function to run the script
def main():
    fetch_rss_and_print()

if __name__ == "__main__":
    main()
