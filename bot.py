import os
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, ContextTypes, filters

TOKEN = os.environ.get("TOKEN")
ADMIN_ID = int(os.environ.get("ADMIN_ID", "123456789"))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ বট চালু হয়েছে!")

async def forward_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    message_text = update.message.text

    forward_text = f"✉️ নতুন মেসেজ:\n\n👤 User: {user.username or user.id}\n📩 Message: {message_text}"
    await context.bot.send_message(chat_id=ADMIN_ID, text=forward_text)
    await update.message.reply_text("📤 মেসেজ পাঠানো হয়েছে!")

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, forward_message))

print("🤖 Bot is running...")
app.run_polling()
