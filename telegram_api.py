from telegram import Update
from telegram.ext import ApplicationBuilder, filters, MessageHandler, ContextTypes


class TelegramApiHandler:
    def __init__(self, token: str, callback_function):
        self.token = token
        self.callback = callback_function
        self.id_counter = {}

    def run_bot(self) -> None:
        app = ApplicationBuilder().token(self.token).build()
        app.add_handler(MessageHandler(filters.ALL, self.__hello))
        app.run_polling()
        print("Telegram bot is running.")

    async def __hello(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        message = update.effective_message
        user_id = message.from_user.id
        group_name = message.chat.title
        users_ids = self.id_counter.setdefault(group_name, set())
        users_ids.add(user_id)
        self.callback(self.id_counter)


