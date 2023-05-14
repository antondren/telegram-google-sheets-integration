from datetime import datetime

from configuration import *
from google_sheets_api import GoogleSpreadSheetHandler
from telegram_api import TelegramApiHandler

LAST_TIME_SENT = datetime.now()


def is_minute_passed() -> bool:
    current_minute = datetime.now().minute
    if current_minute == LAST_TIME_SENT.minute:
        return False
    return current_minute % TIMEFRAME_FOR_ID_COLLECTION == 0


def callback(id_counter: {}) -> None:
    global LAST_TIME_SENT
    if is_minute_passed():
        GOOGLE_API.save_users_ids_to_sheets(id_counter)
        LAST_TIME_SENT = datetime.now()


def main():
    GOOGLE_API.init_connection()
    telegram_bot = TelegramApiHandler(TELEGRAM_BOT_TOKEN, callback)
    telegram_bot.run_bot()


if __name__ == '__main__':
    LAST_TIME_SENT = datetime.now()
    GOOGLE_API = GoogleSpreadSheetHandler(SPREADSHEET_ID, SHEET_NAME)
    main()
