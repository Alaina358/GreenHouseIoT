from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler

# Replace with your actual bot token
TOKEN = "7799675291:AAHaX7G0SmnlMVTM4ku7KCBbx4sjdc-jVRM"

async def start(update: Update, context):
    """
    Handles the /start command and sends a welcome message.
    
    Args:
        update (telegram.Update): The incoming Telegram update.
        context: The callback context for the command.
    """
    await update.message.reply_text("Hello! I am your sensor monitoring bot.")

async def show_chat_id(update: Update, context):
    """
    Handles the /chatid command and sends the user's chat ID.
    
    Args:
        update (telegram.Update): The incoming Telegram update.
        context: The callback context for the command.
    """
    chat_id = update.effective_chat.id
    await update.message.reply_text(f"Your Chat ID is: {chat_id}")
    print(f"Received Chat ID: {chat_id}")

# Initialize the bot
app = ApplicationBuilder().token(TOKEN).build()

# Add command handlers
# Uncomment the following line to enable the /start command
# app.add_handler(CommandHandler("start", start))

# Add a command to retrieve the Chat ID
app.add_handler(CommandHandler("chatid", show_chat_id))

# Run the bot
if __name__ == "__main__":
    app.run_polling()

# Notes:
# - Add the bot to a group or use it directly in private chat.
# - Any user who sends the /chatid command will cause the script to print their Chat ID.
