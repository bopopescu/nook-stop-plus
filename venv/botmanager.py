from telegram.ext import Updater
from telegram.ext import CommandHandler
import json
import codecs

with codecs.open("config.json") as config_file:
    config = json.load(config_file)

updater = Updater(token = config["bot_id"], use_context = True)
dispatcher = updater.dispatcher
my_bot = dispatcher.bot
# my_bot.send_message(chat_id = config["test_user_id"], text = "Testing!");