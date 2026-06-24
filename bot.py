from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import random

from config import *

app = Client(
    "anitoon_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# -------------------
# SETTINGS
# -------------------
bot_status = True

reactions = {
    "👍": 50,
    "😂": 30,
    "❤️": 20
}

# -------------------
# REACTION ENGINE
# -------------------
def get_reaction():
    items = list(reactions.items())
    emojis = [i[0] for i in items]
    weights = [i[1] for i in items]
    return random.choices(emojis, weights=weights)[0]

# -------------------
# PANEL UI
# -------------------
def panel():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎭 Reactions", callback_data="react")],
        [InlineKeyboardButton("⚙ Toggle Bot", callback_data="toggle")],
        [InlineKeyboardButton("📊 Status", callback_data="status")]
    ])

# -------------------
# START COMMAND
# -------------------
@app.on_message(filters.command("start"))
def start(client, message):
    message.reply(
        f"""
🤖 AniToon’s ReactionX Bot

👋 Hello {message.from_user.first_name}

⚡ Auto Reaction System: ACTIVE
📊 Control Panel Ready
""",
        reply_markup=panel()
    )

# -------------------
# AUTO REACTIONS
# -------------------
@app.on_message(filters.group & filters.text)
def react(client, message):
    global bot_status
    if not bot_status:
        return

    try:
        emoji = get_reaction()
        message.react(emoji)
    except:
        pass

# -------------------
# JOIN REQUEST ACCEPT
# -------------------
@app.on_chat_join_request()
def join_request(client, request):
    try:
        client.approve_chat_join_request(
            request.chat.id,
            request.from_user.id
        )

        client.send_message(
            OWNER_ID,
            f"✅ Join Approved: {request.from_user.first_name}"
        )
    except:
        pass

# -------------------
# BUTTON HANDLER
# -------------------
@app.on_callback_query()
def callback(client, query):
    global bot_status

    try:
        query.message.delete()
    except:
        pass

    data = query.data

    if data == "react":
        query.message.reply_text(
            f"🎭 Reactions:\n{reactions}",
            reply_markup=panel()
        )

    elif data == "toggle":
        bot_status = not bot_status
        state = "ON" if bot_status else "OFF"
        query.message.reply_text(
            f"⚙ Bot is {state}",
            reply_markup=panel()
        )

    elif data == "status":
        query.message.reply_text(
            f"""
📊 BOT STATUS

Status: {bot_status}
Reactions: {reactions}
""",
            reply_markup=panel()
        )

# -------------------
# RUN BOT
# -------------------
app.run()
