# Telegram-Google Sheets Integration

This project is a Python script that integrates a Telegram bot with Google Sheets. It listens to messages from groups where the bot is present and counts unique senders within a certain time frame, then logs this information to a Google Sheet.

## Environment Setup

1. Python 3.6+ is required for this script.

2. You need to install the following Python packages if they are not already installed:
    ```
    pip install python-telegram-bot google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
    ```

3. You need to set up a Google Sheets API and download the `credentials.json` file. Place this file in the same directory as the scripts. For detailed instructions, follow this guide: https://developers.google.com/sheets/api/guides/authorizing

4. Set up a Telegram Bot and get the API token. Replace the `TELEGRAM_BOT_TOKEN` in the `configuration.py` file with your bot's token.

5. Update the `SPREADSHEET_ID` in the `configuration.py` file to your Google Sheets document ID, and `SHEET_NAME` to the name of the sheet you want to modify.

6. The `TIMEFRAME_FOR_ID_COLLECTION` value in `configuration.py` is the time interval (in minutes) at which the bot will log information to the Google Sheet. Modify this as per your requirement.
