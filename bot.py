from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import random

API_ID = 123456
API_HASH = "API_HASH"
BOT_TOKEN = "BOT_TOKEN"

OWNER_ID = 123456789

app = Client("anitoon_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# --------------------
# DATABASE (simple memory version)
# --------------------
reactions = {"👍": 50, "😂": 30, "❤️": 20}
bot_status = True
panel_message_ids = {}

# --------------------
# WEIGHTED REACTION PICK
# --------------------
def get_reaction():
    items = list(reactions.items())
    emojis = [i[0] for i in items]
    weights = [i[1] for i in items]
    return random.choices(emojis, weights=weights)[0]

# --------------------
# CONTROL PANEL UI
# --------------------
def panel():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎛 Reaction Settings", callback_data="react")],
        [InlineKeyboardButton("⚙ Toggle Bot", callback_data="toggle")],
        [InlineKeyboardButton("📊 View Status", callback_data="status")]
    ])

# --------------------
# START COMMAND
# --------------------
@app.on_message(filters.command("start"))
def start(client, message):
    msg = message.reply("🤖 AniToon’s ReactionX Bot Panel", reply_markup=panel())
    panel_message_ids[message.chat.id] = msg.id

# --------------------
# AUTO REACT SYSTEM
# --------------------
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

# --------------------
# AUTO JOIN REQUEST ACCEPT
# --------------------
@app.on_chat_join_request()
def join(client, request):
    client.approve_chat_join_request(
        request.chat.id,
        request.from_user.id
    )

    client.send_message(
        OWNER_ID,
        f"👤 Join Approved:\nUser: {request.from_user.first_name}"
    )

# --------------------
# INLINE CALLBACK HANDLER
# --------------------
@app.on_callback_query()
def cb(client, query):
    global bot_status

    data = query.data

    # DELETE OLD PANEL MESSAGE
    try:
        query.message.delete()
    except:
        pass

    # NEW PANEL
    if data == "react":
        query.message.reply(
            f"🎭 Current Reactions: {reactions}",
            reply_markup=panel()
        )

    elif data == "toggle":
        bot_status = not bot_status
        status = "ON" if bot_status else "OFF"
        query.message.reply(f"⚙ Bot is now {status}", reply_markup=panel())

    elif data == "status":
        query.message.reply(
            f"📊 Bot Status: {bot_status}\nReactions: {reactions}",
            reply_markup=panel()
        )

# --------------------
# RUN BOT
# --------------------
app.run()
