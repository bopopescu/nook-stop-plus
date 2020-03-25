from telegram.ext import Updater
from telegram.ext import CommandHandler
import datetime
import json
import codecs
import mysql.connector

with codecs.open("config.json") as config_file:
    config = json.load(config_file)

updater = Updater(token = config["bot_id"], use_context = True)
dispatcher = updater.dispatcher
my_bot = dispatcher.bot
db = mysql.connector.connect(
    host = config["db_host"],
    database = config["db_name"],
    user = config["db_user"],
    passwd = config["db_password"]
)
db_cursor = db.cursor()
today = datetime.date.today()


def record_turnips_price(update, context):
    context.bot.send_message(chat_id = update.effective_chat.id, text = update.message.from_user["first_name"])


def c_record(update, context):
    record_turnips_price(update, context)


# insert doesn't work
def c_start(update, context):
    db_cursor.execute("SELECT * FROM users WHERE telegram_id = " + str(update.effective_chat.id))
    results = db_cursor.fetchall()
    if len(results) == 0:
        query = "INSERT INTO users(telegram_id, username, start_date, last_active_date) VALUES(%s, %s, $s, $s)"
        values = (str(update.effective_chat.id), update.message.from_user["first_name"], today.strftime("%Y-%m-%d"), today.strftime("%Y-%m-%d"))
        db_cursor.execute(query, values)
        db.commit()
        context.bot.send_message(chat_id = update.effective_chat.id, text = "I will help you in the turnips stock market!")
    else:
        context.bot.send_message(chat_id = update.effective_chat.id, text = "Welcome back " + results["username"])


if __name__ == "__main__":
    dispatcher.add_handler(CommandHandler('start', c_start))
    dispatcher.add_handler(CommandHandler('record', c_record))
    updater.start_polling()
    updater.idle()
