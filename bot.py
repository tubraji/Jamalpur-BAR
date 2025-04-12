import os
from telegram import Update, Message
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.environ.get("TOKEN")
ADMIN_ID = int(os.environ.get("ADMIN_ID", "123456789"))

# ইউজার আইডি মেপ রাখবো — msg_id: user_id
message_map = {}

# /start হ্যান্ডলার
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✉️ হ্যালো! আপনি এখন গোপনে মেসেজ পাঠাতে পারেন।")

# ইউজার → অ্যাডমিন
async def user_to_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    user_id = user.id
    msg = update.message.text

    # Forward টু Admin
    sent: Message = await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"📩 মেসেজ এসেছে:\n\n{msg}"
    )

    # ম্যাপ রাখি: অ্যাডমিনের মেসেজ আইডি -> ইউজারের আইডি
    message_map[sent.message_id] = user_id

    # ইউজারকে acknowledge করি
    await update.message.reply_text("✅ মেসেজ পাঠানো হয়েছে।")

# অ্যাডমিন → ইউজার (reply দিলে)
async def admin_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message and update.message.chat_id == ADMIN_ID:
        original_msg_id = update.message.reply_to_message.message_id
        reply_text = update.message.text

        # ম্যাপে ইউজার খুঁজি
        user_id = message_map.get(original_msg_id)
        if user_id:
            await context.bot.send_message(chat_id=user_id, text=f"👤 অ্যাডমিন:\n{reply_text}")
            await update.message.reply_text("📤 পাঠানো হয়েছে ইউজারকে।")
        else:
            await update.message.reply_text("⚠️ ইউজার খুঁজে পাওয়া যায়নি।")

# অ্যাপ চালু করি
app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))

# অ্যাডমিন যদি reply করে
app.add_handler(MessageHandler(filters.TEXT & filters.User(ADMIN_ID), admin_reply))

# সাধারণ ইউজারের মেসেজ
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, user_to_admin))

print("🤖 Secret Chat Bot is running...")
app.run_polling()
