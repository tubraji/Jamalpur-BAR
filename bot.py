import os
from dotenv import load_dotenv
from telegram import Update, Message
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from telegram.error import Forbidden

# .env লোড করি
load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

# ইউজার ম্যাপ
message_map = {}

# /start হ্যান্ডলার
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 বটে স্বাগতম! এখন আপনি মেসেজ পাঠাতে পারেন।")

# ইউজার → অ্যাডমিন
async def user_to_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    msg = update.message.text

    # ইউজার ইনফোসহ পাঠাই
    info = f"👤 *From:* {user.full_name} (@{user.username})\n🆔 ID: `{user.id}`\n\n💬 {msg}"

    try:
        sent: Message = await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=info,
            parse_mode="Markdown"
        )
        message_map[sent.message_id] = user.id
        await update.message.reply_text("✅ মেসেজ পাঠানো হয়েছে।")
    except Forbidden:
        await update.message.reply_text("❌ অ্যাডমিন বটকে ব্লক করে রেখেছে।")

# অ্যাডমিন → ইউজার (reply দিলে)
async def admin_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message and update.message.chat_id == ADMIN_ID:
        original_msg_id = update.message.reply_to_message.message_id
        reply_text = update.message.text

        user_id = message_map.get(original_msg_id)
        if user_id:
            try:
                await context.bot.send_message(chat_id=user_id, text=f"👮‍♂️ অ্যাডমিন:\n{reply_text}")
                await update.message.reply_text("📤 ইউজারকে পাঠানো হয়েছে।")
            except Forbidden:
                await update.message.reply_text("❌ ইউজার বটকে ব্লক করে রেখেছে।")
        else:
            await update.message.reply_text("⚠️ ইউজার খুঁজে পাওয়া যায়নি।")

# এরর হ্যান্ডলার
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    print(f"⚠️ Error: {context.error}")

# অ্যাপ রেজিস্টার করি
app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & filters.User(ADMIN_ID), admin_reply))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, user_to_admin))
app.add_error_handler(error_handler)

print("🚀 Bot is running...")
app.run_polling()
