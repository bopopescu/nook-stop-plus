from telegram.ext import (Updater, CommandHandler, ConversationHandler, MessageHandler, Filters)
import datetime
import json
import codecs
import mysql.connector

RECORD_PRICE = 0

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
db_cursor = db.cursor(buffered = True, dictionary = True)


# TODO
# Check if already recorded price, if so, ask if user want to update it
# Insert price for the time and day on the database
def c_record(update, context):
    context.bot.send_message(chat_id = update.effective_chat.id, text = update.message.from_user["first_name"])
    return RECORD_PRICE


def price(update, context):
    context.bot.send_message(chat_id = update.effective_chat.id, text = "So your turnips sells for " + update.message.text + " huh? Noted!")
    return ConversationHandler.END


def cancel_registration_turnips(update, context):
    context.bot.send_message(chat_id = update.effective_chat.id, text = "Ok let's NOT do that then.")
    return ConversationHandler.END


def c_start(update, context):
    db_cursor.execute("SELECT * FROM users WHERE telegram_id = " + str(update.effective_chat.id))
    results = db_cursor.fetchone()
    if results is None:
        query = "INSERT INTO users(telegram_id, username, start_date, last_active_date) VALUES(%s, %s, CURDATE(), CURDATE())"
        values = (str(update.effective_chat.id), update.message.from_user["first_name"])
        db_cursor.execute(query, values)
        db.commit()
        context.bot.send_message(chat_id = update.effective_chat.id, text = "I will help you in the turnips stock market!")
    else:
        context.bot.send_message(chat_id = update.effective_chat.id, text = "Welcome back " + results["username"])


if __name__ == "__main__":
    register_turnips_price_handler = ConversationHandler(
        entry_points = [CommandHandler('record', c_record)],
        states = {
            RECORD_PRICE: [MessageHandler(Filters.regex('^[0-9]*$'), price)]
        },
        fallbacks = [CommandHandler('cancel', cancel_registration_turnips)]
    )

    dispatcher.add_handler(CommandHandler('start', c_start))
    dispatcher.add_handler(register_turnips_price_handler)
    updater.start_polling()
    updater.idle()
