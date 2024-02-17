import argparse
import os
import logging

from telegram import Update, Message, Chat
from telegram.ext import filters, MessageHandler, MessageReactionHandler, ApplicationBuilder, CommandHandler, ContextTypes

import pandas as pd

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)

message_list = list()
reaction_list = list()

# Define a function to handle messages
async def message_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message
    logging.info("New message: {}".format(update.message))

    # Add message to the message list
    message_list.append(
            (message.date, message.chat.title, message.id, message.from_user.username, message.text)
            )
    message_df = pd.DataFrame(message_list, columns=["date", "chat", "message", "user", "text"])
    message_df.to_csv("messages.csv", index=False, mode="a", header=not os.path.exists("messages.csv"))
    message_list.clear()

async def reaction_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reaction = update.message_reaction
    logging.info("New reaction: {}".format(reaction))
    
    reaction_list.append(
            (reaction.date, reaction.chat.title, reaction.message_id, reaction.user.username, reaction.new_reaction[0].emoji)
            )
    reaction_df = pd.DataFrame(reaction_list, columns=["date", "chat", "message", "user", "emoji"])
    reaction_df.to_csv("reactions.csv", index=False, mode="a", header=not os.path.exists("reactions.csv"))
    reaction_list.clear()

def main():

    parser = argparse.ArgumentParser(prog="telegram-reaction-bot")
    parser.add_argument("token", type=str, help="Telegram bot token")
    args = parser.parse_args()

    application = ApplicationBuilder().token(args.token).build()

    # Register a reaction handler
    reaction_handler = MessageReactionHandler(reaction_callback)
    application.add_handler(reaction_handler)

    # Register a generic message handler
    message_handler = MessageHandler(filters.ALL & ~filters.COMMAND, message_callback)
    application.add_handler(message_handler)

    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
