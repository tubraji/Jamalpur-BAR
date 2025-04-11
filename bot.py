from telegram import Update
from telegram.ext import Application, MessageHandler, filters, CommandHandler

# তোমার Bot Token এখানে বসাও
TOKEN = "YOUR_BOT_TOKEN"

# তোমার Telegram ID (যেখানে মেসেজ ফরোয়ার্ড হবে)
ADMIN_ID = 123456789  

async def start(update: Update, context):
    await update.message.reply_text("✅ বট চালু হয়েছে! এখন মেসেজ পাঠাতে পারো।")

async def forward_message(update: Update, context):
    user = update.message.from_user
    message_text = update.message.text

    # মেসেজ ফরোয়ার্ড করা হবে
    forward_text = f"✉️ নতুন মেসেজ:\n\n👤 User: {user.username or user.id}\n📩 Message: {message_text}"
    
    # তোমার কাছে মেসেজ পাঠাবে
    await context.bot.send_message(chat_id=ADMIN_ID, text=forward_text)

    # ইউজারকে কনফার্মেশন দিবে
    await update.message.reply_text("📤 মেসেজ পাঠানো হয়েছে!")

async def reply_to_user(update: Update, context):
    """তুমি যখন রিপ্লাই পাঠাবে, তখন ইউজারকে মেসেজ যাবে"""
    if update.message.reply_to_message:
        original_message = update.message.reply_to_message.text.split("\n")
        user_id = int(original_message[1].split(":")[1].strip())

        # ইউজারকে মেসেজ পাঠানো হবে
        await context.bot.send_message(chat_id=user_id, text=update.message.text)

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, forward_message))

print("🤖 Bot is running...")
app.run_polling()
