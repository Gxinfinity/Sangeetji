import os
import random
from datetime import datetime

from PIL import Image, ImageDraw
from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegraph import upload_file

from Oneforall import app

#━━━━━━━━━━━━━━━━━━━━━━━━━━━#
# BUTTONS
#━━━━━━━━━━━━━━━━━━━━━━━━━━━#

POLICE = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text="<tg-emoji emoji-id='5224681093990478312'>🍭</tg-emoji> ᴍʏ ᴄᴜᴛᴇ ᴅᴇᴠᴇʟᴏᴘᴇʀ 🍭",
                url="https://t.me/Roohi_Queen_Bot?start=_tgr_yN-6yUs4ZmRh",
            )
        ],
        [
            InlineKeyboardButton(
                text="💜 ᴄᴏᴜᴘʟᴇ ᴄᴏʟᴏʀ 💜",
                callback_data="couple_color",
            ),
            InlineKeyboardButton(
                text="<tg-emoji emoji-id='5210952531676504517'>❌</tg-emoji> ʙᴀᴄᴋ",
                callback_data="close_couple",
            ),
        ],
    ]
)

#━━━━━━━━━━━━━━━━━━━━━━━━━━━#
# DATE FUNCTIONS
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
today = str(dt()[0])

#━━━━━━━━━━━━━━━━━━━━━━━━━━━#
# COUPLES CMD
#━━━━━━━━━━━━━━━━━━━━━━━━━━━#


@app.on_message(filters.command("couples"))
async def couples(_, message):
    cid = message.chat.id

    if message.chat.type == ChatType.PRIVATE:
        return await message.reply_text(
            "❌ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴏɴʟʏ ᴡᴏʀᴋs ɪɴ ɢʀᴏᴜᴘs."
        )

    try:
        msg = await message.reply_text(
            "💞 ɢᴇɴᴇʀᴀᴛɪɴɢ ᴄᴜᴛᴇ ᴄᴏᴜᴘʟᴇ..."
        )

        users = []

        async for member in app.get_chat_members(message.chat.id, limit=50):
            if not member.user.is_bot:
                users.append(member.user.id)

        if len(users) < 2:
            return await msg.edit(
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

        # PROFILE PHOTOS
        photo1 = user1.photo
        photo2 = user2.photo

        try:
            p1 = await app.download_media(
                photo1.big_file_id,
                file_name="downloads/pfp1.png",
            )
        except Exception:
            p1 = "Oneforall/assets/upic.png"

        try:
            p2 = await app.download_media(
                photo2.big_file_id,
                file_name="downloads/pfp2.png",
            )
        except Exception:
            p2 = "Oneforall/assets/upic.png"

        # OPEN IMAGES
        img1 = Image.open(p1).convert("RGBA")
        img2 = Image.open(p2).convert("RGBA")

        # BACKGROUND IMAGE
        img = Image.open(
            "Oneforall/assets/cppicbranded.jpg"
        ).convert("RGBA")

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

        # PASTE IMAGES
        img.paste(img1, (116, 160), img1)
        img.paste(img2, (789, 160), img2)

        # SAVE IMAGE
        output = f"test_{cid}.png"
        img.save(output)

        # CAPTION
        TXT = f"""
꧁｡･ﾟ🌷 ˹Tᴏᴅᴀʏ’ꜱ Cᴜᴛᴇ Cᴏᴜᴘʟᴇ˼ 🌷ﾟ･｡꧂

      {N1}  ♡  {N2}
           💚✨

> ꜱᴏᴍᴇ ᴄᴏɴɴᴇᴄᴛɪᴏɴꜱ ᴀʀᴇ  
> ᴡʀɪᴛᴛᴇɴ ɪɴ ꜱᴛᴀʀꜱ ✨💫

🎀 ɴᴇxᴛ ᴄᴏᴜᴘʟᴇ :
🌸 {tomorrow}

🧸 ᴋᴇᴇᴘ ꜱᴍɪʟɪɴɢ & ʟᴏᴠɪɴɢ 💕

<tg-emoji emoji-id="5224681093990478312">🍭</tg-emoji> ʟᴏʟʟɪᴘᴏᴘ ᴘʀᴇᴍɪᴜᴍ ᴄᴏᴜᴘʟᴇ 🍭
"""

        # SEND PHOTO
        await message.reply_photo(
            photo=output,
            caption=TXT,
            reply_markup=POLICE,
        )

        await msg.delete()

        # TELEGRAPH UPLOAD
        try:
            uploaded = upload_file(output)
            for x in uploaded:
                img_link = "https://graph.org/" + x
                print(img_link)
        except Exception:
            pass

    except Exception as e:
        print(f"COUPLES ERROR : {e}")

    finally:
        # CLEANUP
        files = [
            "downloads/pfp1.png",
            "downloads/pfp2.png",
            output if 'output' in locals() else None,
        ]

        for file in files:
            try:
                if file and os.path.exists(file):
                    os.remove(file)
            except Exception:
                pass


#━━━━━━━━━━━━━━━━━━━━━━━━━━━#
# CALLBACKS
#━━━━━━━━━━━━━━━━━━━━━━━━━━━#

@app.on_callback_query(filters.regex("couple_color"))
async def couple_color(_, query):
    colors = [
        "❤️ Red Love",
        "💙 Blue Love",
        "💚 Green Love",
        "💜 Purple Love",
        "🖤 Dark Love",
        "🤍 White Love",
    ]

    await query.answer(
        random.choice(colors),
        show_alert=True,
    )


@app.on_callback_query(filters.regex("close_couple"))
async def close_couple(_, query):
    try:
        await query.message.delete()
    except Exception:
        pass


#━━━━━━━━━━━━━━━━━━━━━━━━━━━#
# HELP
#━━━━━━━━━━━━━━━━━━━━━━━━━━━#

__mod__ = "COUPLES"

__help__ = """
❍ /couples - Get Today's Cute Couples 💞
"""