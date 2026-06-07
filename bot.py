import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ChatMemberHandler, ContextTypes

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot token from BotFather
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command for direct bot interactions"""
    user = update.effective_user
    logger.info(f"User {user.id} ({user.username}) started the bot")
    
    await update.message.reply_text(
        "👋 Hello! Add me to a group or channel to receive its ID.\n\n"
        "Once added, I'll send you a private message with the group/channel ID.\n\n"
        "Use /chatid to get the current chat ID.\n"
        "Use /myid to get your numeric user ID anytime."
    )

async def chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /chatid command to return the current chat ID"""
    chat = update.effective_chat
    user = update.effective_user
    
    logger.info(f"User {user.id} requested chat ID for chat {chat.id} ({chat.type})")
    
    if chat.type == "private":
        await update.message.reply_text(
            "ℹ️ This is a private chat.\n\n"
            f"Chat ID: <code>{chat.id}</code>\n"
            f"User ID: <code>{user.id}</code>\n\n"
            "In private chats, chat ID and user ID are the same.\n"
            "Add me to a group or channel to get its group/channel ID!",
            parse_mode='HTML'
        )
    else:
        chat_type = "Channel" if chat.type == "channel" else "Group"
        chat_name = chat.title or "Unknown"
        
        await update.message.reply_text(
            f"📊 {chat_type} Information\n\n"
            f"📝 Name: {chat_name}\n"
            f"🆔 Chat ID: <code>{chat.id}</code>\n\n"
            f"Tap the ID to copy it.",
            parse_mode='HTML'
        )

async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Backward-compatible alias for /getid"""
    await chat_id(update, context)

async def my_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /myid command to return the numeric user ID"""
    user = update.effective_user

    logger.info(f"User {user.id} requested their numeric ID")

    await update.message.reply_text(
        f"👤 Your numeric user ID is:\n\n"
        f"<code>{user.id}</code>\n\n"
        f"Tap it to copy.",
        parse_mode='HTML'
    )

async def track_chat_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle bot being added to groups/channels"""
    result = update.my_chat_member
    
    # Check if bot was added (not removed or banned)
    if result.new_chat_member.status in ['member', 'administrator']:
        chat = result.chat
        user = result.from_user
        
        # Group/channel information
        chat_type = "Channel" if chat.type == "channel" else "Group"
        chat_name = chat.title or "Unknown"
        chat_id = chat.id
        
        logger.info(f"Bot added to {chat_type} '{chat_name}' (ID: {chat_id}) by user {user.id}")
        
        # Message to send to user
        message = (
            f"✅ {chat_type} added successfully!\n\n"
            f"📝 Name: {chat_name}\n"
            f"🆔 ID: <code>{chat_id}</code>\n\n"
            f"You can copy the ID by tapping it.\n"
            f"Use /getid inside the {chat_type.lower()} anytime!"
        )
        
        try:
            # Send private message to user who added the bot
            await context.bot.send_message(
                chat_id=user.id,
                text=message,
                parse_mode='HTML'
            )
            logger.info(f"Notification sent successfully to user {user.id}")
        except Exception as e:
            # If unable to send privately (user hasn't started the bot)
            logger.warning(f"Failed to send message to user {user.id}: {e}")

def main():
    """Start the bot"""
    # Create application
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("chatid", chat_id))
    app.add_handler(CommandHandler("getid", get_id))
    app.add_handler(CommandHandler("myid", my_id))
    app.add_handler(ChatMemberHandler(track_chat_member, ChatMemberHandler.MY_CHAT_MEMBER))
    
    # Start bot
    logger.info("🤖 Bot started and polling for updates ...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
