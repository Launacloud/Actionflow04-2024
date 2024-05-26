import os
import requests
import xml.etree.ElementTree as ET

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN_PALAVRADODIA')
RSS_FEED_URL = os.getenv('RSS_FEED_URLPALAVRADODIA')
CHAT_ID = os.getenv('TELEGRAM_CHAT_IDPALAVRADODIA')

# Function to send message to Telegram
def send_message(message):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    data = {'chat_id': CHAT_ID, 'text': message}
    response = requests.post(url, data=data)
    return response.json()

# Function to fetch RSS feed and print items to log
def fetch_rss_and_print():
    response = requests.get(RSS_FEED_URL)
    root = ET.fromstring(response.content)
    items = root.findall('.//item')
    for item in items:
        title = item.find('title').text
        link = item.find('link').text
        print(f'Title: {title}, Link: {link}')
        # You can also send each item as a message to Telegram if needed
        # send_message(f'Title: {title}, Link: {link}')

# Main function to run the script
def main():
    fetch_rss_and_print()

if __name__ == "__main__":
    main()
