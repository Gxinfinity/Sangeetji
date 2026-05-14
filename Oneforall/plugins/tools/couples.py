import os
import random
from datetime import datetime

from PIL import Image, ImageDraw
from pyrogram import filters
from pyrogram.enums import ChatType, ButtonStyle
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from telegraph import upload_file
from Oneforall import app

#━━━━━━━━━━━━━━━━━━━━━━━━━━━#
# SAFE PATHS
#━━━━━━━━━━━━━━━━━━━━━━━━━━━#

PLUGIN_DIR = os.path.dirname(os.path.abspath(__file__))

BASE_DIR = os.path.abspath(
    os.path.join(PLUGIN_DIR, "../../")
)

ASSETS_DIR = os.path.join(BASE_DIR, "assets")

DOWNLOADS_DIR = os.path.join(BASE_DIR, "downloads")

os.makedirs(DOWNLOADS_DIR, exist_ok=True)

UPIC = os.path.join(ASSETS_DIR, "upic.png")

BG_IMAGES = [
    os.path.join(ASSETS_DIR, "cppicbranded.jpg"),
    os.path.join(ASSETS_DIR, "goku.jpg"),
]

#━━━━━━━━━━━━━━━━━━━━━━━━━━━#
# AUTO CREATE FALLBACK IMAGE
#━━━━━━━━━━━━━━━━━━━━━━━━━━━#

if not os.path.exists(UPIC):

    fallback = Image.new("RGB", (500, 500), (25, 25, 25))
    fallback.save(UPIC)

#━━━━━━━━━━━━━━━━━━━━━━━━━━━#
# PREMIUM BUTTON FUNCTION
#━━━━━━━━━━━━━━━━━━━━━━━━━━━#

def btn(text, emoji_id, style=ButtonStyle.DEFAULT, **kwargs):

    try:
        return InlineKeyboardButton(
            text=text,
            icon_custom_emoji_id=emoji_id,
            style=style,
            **kwargs
        )

    except Exception:

        return InlineKeyboardButton(
            text=text,
            **kwargs
        )

#━━━━━━━━━━━━━━━━━━━━━━━━━━━#
# RANDOM COLORS
#━━━━━━━━━━━━━━━━━━━━━━━━━━━#

COUPLE_COLORS = [
    ("❤️ Red Couple", "5465665476971471368"),
    ("💜 Purple Couple", "6026236216079290036"),
    ("💚 Green Couple", "5395463497783983254"),
    ("💙 Blue Couple", "5386367538735104399"),
    ("🖤 Dark Couple", "5447644880824181073"),
    ("🤍 White Couple", "5222102095323814345"),
]

#━━━━━━━━━━━━━━━━━━━━━━━━━━━#
# BUTTON PANEL
#━━━━━━━━━━━━━━━━━━━━━━━━━━━#

def couple_panel():

    random_color = random.choice(COUPLE_COLORS)

    buttons = [
        [
            btn(
                " ᴍʏ ᴄᴜᴛᴇ ᴅᴇᴠᴇʟᴏᴘᴇʀ ",
                5224681093990478312,
                url="https://t.me/Roohi_Queen_Bot?start=_tgr_yN-6yUs4ZmRh",
                style=ButtonStyle.SUCCESS,
            ),
        ],
        [
            btn(
                random_color[0],
                random_color[1],
                callback_data="couple_color",
                style=ButtonStyle.PRIMARY,
            ),
            btn(
                " ᴍᴀᴋᴇ ɴᴇᴡ ",
                5210952531676504517,
                callback_data="new_couple",
                style=ButtonStyle.DANGER,
            ),
        ],
    ]

    return InlineKeyboardMarkup(buttons)

#━━━━━━━━━━━━━━━━━━━━━━━━━━━#
# DATE
#━━━━━━━━━━━━━━━━━━━━━━━━━━━#

def dt():
    now = datetime.now()
    return now.strftime("%d/%m/%Y %H:%M").split(" ")

def dt_tom():
    day = int(dt()[0].split("/")[0]) + 1
    month = dt()[0].split("/")[1]
    year = dt()[0].split("/")[2]
    return f"{day}/{month}/{year}"

tomorrow = str(dt_tom())

#━━━━━━━━━━━━━━━━━━━━━━━━━━━#
# MAIN FUNCTION
#━━━━━━━━━━━━━━━━━━━━━━━━━━━#

async def send_couple(message):

    cid = message.chat.id

    users = []

    async for member in app.get_chat_members(message.chat.id, limit=100):

        if not member.user.is_bot:
            users.append(member.user.id)

    if len(users) < 2:
        return await message.reply_text(
            "❌ ɴᴏᴛ ᴇɴᴏᴜɢʜ ᴜsᴇʀs ɪɴ ɢʀᴏᴜᴘ."
        )

    # RANDOM USERS

    c1_id = random.choice(users)
    c2_id = random.choice(users)

    while c1_id == c2_id:
        c2_id = random.choice(users)

    # USER DATA

    user1 = await app.get_users(c1_id)
    user2 = await app.get_users(c2_id)

    N1 = user1.mention
    N2 = user2.mention

    # USER PHOTOS

    photo1 = user1.photo
    photo2 = user2.photo

    # SAFE DOWNLOAD

    try:

        if photo1:

            p1 = await app.download_media(
                photo1.big_file_id,
                file_name=os.path.join(
                    DOWNLOADS_DIR,
                    f"pfp1_{cid}.png"
                ),
            )

        else:
            p1 = UPIC

    except Exception:
        p1 = UPIC

    try:

        if photo2:

            p2 = await app.download_media(
                photo2.big_file_id,
                file_name=os.path.join(
                    DOWNLOADS_DIR,
                    f"pfp2_{cid}.png"
                ),
            )

        else:
            p2 = UPIC

    except Exception:
        p2 = UPIC

    # SAFE IMAGE OPEN

    try:
        img1 = Image.open(p1).convert("RGBA")

    except Exception:
        img1 = Image.open(UPIC).convert("RGBA")

    try:
        img2 = Image.open(p2).convert("RGBA")

    except Exception:
        img2 = Image.open(UPIC).convert("RGBA")

    # RANDOM BG

    existing_bg = [x for x in BG_IMAGES if os.path.exists(x)]

    if not existing_bg:
        existing_bg = [UPIC]

    bg = random.choice(existing_bg)

    img = Image.open(bg).convert("RGBA")

    # RESIZE

    img1 = img1.resize((437, 437))
    img2 = img2.resize((437, 437))

    # ROUND IMAGE 1

    mask1 = Image.new("L", img1.size, 0)
    draw1 = ImageDraw.Draw(mask1)
    draw1.ellipse((0, 0) + img1.size, fill=255)

    # ROUND IMAGE 2

    mask2 = Image.new("L", img2.size, 0)
    draw2 = ImageDraw.Draw(mask2)
    draw2.ellipse((0, 0) + img2.size, fill=255)

    img1.putalpha(mask1)
    img2.putalpha(mask2)

    # PASTE

    img.paste(img1, (116, 160), img1)
    img.paste(img2, (789, 160), img2)

    # OUTPUT

    output = os.path.join(
        DOWNLOADS_DIR,
        f"couple_{cid}.png"
    )

    img.save(output)

    # RANDOM TEXT

    lolipop = random.choice([
        "🍭 ʟᴏʟʟɪᴘᴏᴘ ᴘʀᴇᴍɪᴜᴍ ᴄᴏᴜᴘʟᴇ 🍭",
        "💞 ᴄᴜᴛᴇ ᴄᴏᴜᴘʟᴇ ᴏꜰ ᴛʜᴇ ᴅᴀʏ 💞",
        "✨ ꜱᴛᴀʀ ᴄᴏɴɴᴇᴄᴛᴇᴅ ᴄᴏᴜᴘʟᴇ ✨",
        "🥀 ʀᴏᴏʜɪ x ᴍᴜꜱɪᴄ ᴄᴏᴜᴘʟᴇ 🥀",
    ])

    TXT = f"""
꧁｡･ﾟ🌷 ˹Tᴏᴅᴀʏ’ꜱ Cᴜᴛᴇ Cᴏᴜᴘʟᴇ˼ 🌷ﾟ･｡꧂

      {N1}  ♡  {N2}
           💚✨

> ꜱᴏᴍᴇ ᴄᴏɴɴᴇᴄᴛɪᴏɴꜱ ᴀʀᴇ
> ᴡʀɪᴛᴛᴇɴ ɪɴ ꜱᴛᴀʀꜱ ✨💫

🎀 ɴᴇxᴛ ᴄᴏᴜᴘʟᴇ :
🌸 {tomorrow}

🧸 ᴋᴇᴇᴘ ꜱᴍɪʟɪɴɢ & ʟᴏᴠɪɴɢ 💕

{lolipop}
"""

    # SEND PHOTO

    await message.reply_photo(
        photo=output,
        caption=TXT,
        reply_markup=couple_panel(),
    )

    # TELEGRAPH

    try:
        upload_file(output)

    except Exception:
        pass

    # CLEANUP

    cleanup = [
        p1,
        p2,
        output,
    ]

    for file in cleanup:

        try:

            if (
                file != UPIC
                and os.path.exists(file)
            ):
                os.remove(file)

        except Exception:
            pass

#━━━━━━━━━━━━━━━━━━━━━━━━━━━#
# COMMAND
#━━━━━━━━━━━━━━━━━━━━━━━━━━━#

@app.on_message(filters.command("couples"))
async def couples(_, message):

    if message.chat.type == ChatType.PRIVATE:

        return await message.reply_text(
            "❌ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴏɴʟʏ ᴡᴏʀᴋs ɪɴ ɢʀᴏᴜᴘs."
        )

    msg = await message.reply_text(
        "💞 ɢᴇɴᴇʀᴀᴛɪɴɢ ᴘʀᴇᴍɪᴜᴍ ᴄᴏᴜᴘʟᴇ..."
    )

    try:

        await send_couple(message)

        await msg.delete()

    except Exception as e:

        await msg.edit(
            f"❌ Error : {e}"
        )

#━━━━━━━━━━━━━━━━━━━━━━━━━━━#
# NEW COUPLE
#━━━━━━━━━━━━━━━━━━━━━━━━━━━#

@app.on_callback_query(filters.regex("new_couple"))
async def new_couple(_, query):

    try:

        await query.answer(
            "💞 ɢᴇɴᴇʀᴀᴛɪɴɢ ɴᴇᴡ ᴄᴏᴜᴘʟᴇ...",
            cache_time=1
        )

        await send_couple(query.message)

    except Exception as e:

        print(
            f"NEW COUPLE ERROR: {e}"
        )

#━━━━━━━━━━━━━━━━━━━━━━━━━━━#
# COLOR BUTTON
#━━━━━━━━━━━━━━━━━━━━━━━━━━━#

@app.on_callback_query(filters.regex("couple_color"))
async def couple_color(_, query):

    colors = [
        "❤️ ʀᴇᴅ ʟᴏᴠᴇ ᴄᴏᴜᴘʟᴇ ❤️",
        "💜 ᴘᴜʀᴘʟᴇ ʜᴇᴀʀᴛ ᴄᴏᴜᴘʟᴇ 💜",
        "💚 ɢʀᴇᴇɴ ᴀᴇꜱᴛʜᴇᴛɪᴄ ᴄᴏᴜᴘʟᴇ 💚",
        "💙 ʙʟᴜᴇ ꜱᴋʏ ᴄᴏᴜᴘʟᴇ 💙",
        "🖤 ᴅᴀʀᴋ ʀᴏᴍᴀɴᴄᴇ ᴄᴏᴜᴘʟᴇ 🖤",
    ]

    await query.answer(
        random.choice(colors),
        show_alert=True,
    )

#━━━━━━━━━━━━━━━━━━━━━━━━━━━#
# HELP
#━━━━━━━━━━━━━━━━━━━━━━━━━━━#

__mod__ = "COUPLES"

__help__ = """
❍ /couples - Get Today's Premium Couples 💞
"""