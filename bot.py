from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import random
from pymongo import MongoClient
from config import *

mongo = MongoClient(MONGO_URL)
db = mongo["anitoon_bot"]
collection = db["settings"]

from config import *

app = Client(
    "anitoon_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# -------------------
# MEMORY STORAGE
# -------------------
reactions = {"👍": 50, "😂": 30, "❤️": 20}
bot_status = True

# -------------------
# WEIGHTED REACTION
# -------------------
def get_reaction():
    items = list(reactions.items())
    emojis = [i[0] for i in items]
    weights = [i[1] for i in items]
    return random.choices(emojis, weights=weights)[0]

# -------------------
# CONTROL PANEL
# -------------------
def panel():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎭 Reactions", callback_data="react")],
        [InlineKeyboardButton("⚙ Toggle Bot", callback_data="toggle")],
        [InlineKeyboardButton("📊 Status", callback_data="status")]
    ])

# -------------------
# /START COMMAND
# -------------------
@app.on_message(filters.command("start"))
def start(client, message):
    text = f"""
🤖 AniToon’s ReactionX Bot

👋 Hello {message.from_user.first_name}

⚡ Auto Reaction Bot is ready
🎯 Join Auto Accept: Active
📊 Control Panel below
"""
    message.reply(text, reply_markup=panel())

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
# AUTO JOIN ACCEPT
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
            f"✅ Join Approved:\nUser: {request.from_user.first_name}"
        )
    except:
        pass

# -------------------
# BUTTON CALLBACKS
# -------------------
@app.on_callback_query()
def callback(client, query):
    global bot_status

    data = query.data

    try:
        query.message.delete()  # remove old panel
    except:
        pass

    if data == "react":
        query.message.reply_text(
            f"🎭 Reactions:\n{reactions}",
            reply_markup=panel()
        )

    elif data == "toggle":
        bot_status = not bot_status
        status = "ON" if bot_status else "OFF"
        query.message.reply_text(
            f"⚙ Bot is {status}",
            reply_markup=panel()
        )

    elif data == "status":
        query.message.reply_text(
            f"""
📊 STATUS REPORT

Bot: {bot_status}
Reactions: {reactions}
""",
            reply_markup=panel()
        )

# -------------------
# RUN BOT
# -------------------
app.run()
