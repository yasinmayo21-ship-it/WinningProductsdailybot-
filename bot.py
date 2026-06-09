import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.environ.get("TOKEN")

PAID_USERS = []

FREE_PRODUCT = """
🆓 *Free Alert — Sample Product*

🛍️ *Product:* Magnetic Phone Car Mount
💰 Buy Price: $2.50
🏷️ Sell Price: $14.99
📈 Profit: ~$10
🎯 Target: Car owners, commuters USA/UK

⭐ Upgrade to Premium for daily alerts!
"""

PREMIUM_PRODUCT = """
🔥 *Premium Alert — Today's Winning Product*

🛍️ *Product:* LED Sunset Lamp
💰 Buy Price: $4.00
🏷️ Sell Price: $29.99
📈 Profit: ~$22
🎯 Target: Home decor lovers, gift buyers
📣 Ad Angle: Turn any room into a sunset
📦 Shipping: 7–12 days
🏆 Trend Score: 9/10 — Viral on TikTok
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🆓 Free Product Alert", callback_data='free')],
        [InlineKeyboardButton("🔥 Premium Alerts Info", callback_data='premium_info')],
        [InlineKeyboardButton("💳 Subscribe — $9.99/month", callback_data='subscribe')],
        [InlineKeyboardButton("✅ I Already Paid", callback_data='check_access')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "👋 Welcome to *WinningProducts Daily!*\n\n"
        "Daily winning products for USA/UK dropshippers.\n\n"
        "🆓 Free: 1 product/week\n"
        "🔥 Premium: Daily alerts + full details\n",
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if query.data == 'free':
        await query.edit_message_text(FREE_PRODUCT, parse_mode='Markdown')

    elif query.data == 'premium_info':
        await query.edit_message_text(
            "🔥 *Premium — $9.99/month*\n\n"
            "✅ Daily winning product alert\n"
            "✅ Supplier link + buy price\n"
            "✅ Profit margin included\n"
            "✅ TikTok ad angle\n"
            "✅ Target audience breakdown\n"
            "✅ Trend score\n\n"
            "Tap Subscribe to get started.",
            parse_mode='Markdown'
        )

    elif query.data == 'subscribe':
        await query.edit_message_text(
            "💳 *How to Subscribe:*\n\n"
            "Send $9.99 to:\n"
            "💰 Payoneer: your@email.com\n"
            "💰 Wise: your@email.com\n\n"
            "After payment send screenshot to @yourusername\n"
            "✅ Access granted within 1 hour.",
            parse_mode='Markdown'
        )

    elif query.data == 'check_access':
        if user_id in PAID_USERS:
            await query.edit_message_text(PREMIUM_PRODUCT, parse_mode='Markdown')
        else:
            await query.edit_message_text(
                "❌ No premium access found.\n\n"
                "If you just paid, send your screenshot to @yourusername.\n"
                "Press /start to go back."
            )

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.run_polling()
