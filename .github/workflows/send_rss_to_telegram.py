name: RSS to Telegram

on:
  schedule:
    - cron: '*/15 * * * *'  # Runs every 15 minutes
  workflow_dispatch:
  push:  # This triggers the workflow on push events

jobs:
  send_rss_to_telegram:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout repository
      uses: actions/checkout@v2

    - name: Set up Python
      uses: actions/setup-python@v4  # Updated to v4 for latest compatibility
      with:
        python-version: '3.x'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install feedparser requests

    - name: Run script
      env:
        TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
        RSS_FEEDS_CHAT_IDS: ${{ secrets.RSS_FEEDS_CHAT_IDS }}  # Ensure this secret contains a JSON string
      run: python send_rss_to_telegram.py

  build_actionsflow:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v2

      - name: Use Node.js 14.x
        uses: actions/setup-node@v2
        with:
          node-version: '14.x'

      - name: Cache Node.js modules
        uses: actions/cache@v2
        with:
          path: ~/.npm
          key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
          restore-keys: |
            ${{ runner.os }}-node-

      - name: Install dependencies
        run: npm install

      - name: Build Actionsflow
        run: npx actionsflow build --include -f false --verbose false --json-secrets '${{ secrets.YOUR_SECRETS_HERE }}' --json-github '${{ toJson(github) }}'
