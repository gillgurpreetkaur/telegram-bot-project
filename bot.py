from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from datetime import datetime, timedelta
import asyncio

# Global dictionary to store user data
user_data = {}

# Define commands
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Display menu options
    menu_keyboard = [['Share Social Handle', 'View Viral Content'],
                     ['Start 21-Day Challenge', 'Guide'],
                     ['Content Creator 2025']]
    reply_markup = ReplyKeyboardMarkup(menu_keyboard, one_time_keyboard=True)
    await update.message.reply_text(
        "Hello! Welcome to the Createathon Bot. Please select an option from the menu below:",
        reply_markup=reply_markup
    )

async def share_handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Please share your social handle (or type 'None' if you don't have one):")

async def view_viral_content(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Please share your most viral content and its view count (or type 'None' if you don't have any):")

async def guide(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    guide_text = """**Guide to Content Creation:**
1. **Select a Niche**: Focus on topics you're passionate about (e.g., tech, fitness, art).
2. **Find Unique Ideas**: Use tools like Google Trends, Pinterest, or brainstorming.
3. **Plan Content**: Draft scripts or designs before creating.
4. **Be Consistent**: Post regularly to build an audience.
5. **Engage with Followers**: Respond to comments and messages.

More advanced guides will be added soon!
"""
    await update.message.reply_text(guide_text, parse_mode="Markdown")

async def content_creator_2025(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    guide_text = """**How to Be a Content Creator in 2025:**
- Focus on authenticity and community engagement.
- Leverage AI tools for video editing, content ideas, and audience analysis.
- Diversify income streams (e.g., courses, brand deals, merchandise).
- More tips will be added soon!
"""
    await update.message.reply_text(guide_text, parse_mode="Markdown")

async def start_challenge(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id
    user_data[chat_id] = {'challenge_start_date': datetime.now(), 'daily_updates': []}
    await update.message.reply_text(
        "Your 21-day Createathon Challenge has started! Each day, I’ll send you a message asking for a content link and view count. Let's get started!"
    )
    await send_daily_message(context, chat_id)

async def handle_message(update, context):
    chat_id = update.effective_chat.id
    user_message = update.message.text
    user_data = context.user_data

    # Check if the user's data exists
    if chat_id not in user_data:
        user_data[chat_id] = {}  # Initialize user's data

    # Check if 'daily_updates' exists, if not initialize it as an empty list
    if 'daily_updates' not in user_data[chat_id]:
        user_data[chat_id]['daily_updates'] = []

    # Append the message to 'daily_updates'
    user_data[chat_id]['daily_updates'].append(user_message)

    # Respond to the user
    await update.message.reply_text(f"Message received: {user_message}")


async def send_daily_message(context, chat_id: int) -> None:
    for day in range(1, 22):  # 21 days
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"Day {day}: Please share your content link and its view count!"
        )
        await asyncio.sleep(86400)  # Wait for a day (in seconds)

# Main function to run the bot
def main():
    TOKEN = "7664542527:AAGx-Np_vmlK4CujRJTMJJx1q6ZtoNG55-M"

    # Create the bot application
    application = Application.builder().token(TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("share_handle", share_handle))
    application.add_handler(CommandHandler("view_viral_content", view_viral_content))
    application.add_handler(CommandHandler("guide", guide))
    application.add_handler(CommandHandler("content_creator_2025", content_creator_2025))
    application.add_handler(CommandHandler("start_challenge", start_challenge))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Run the bot
    application.run_polling()

if __name__ == "__main__":
    main()
