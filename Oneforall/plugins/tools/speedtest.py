import asyncio
import json
import os
import requests

from pyrogram import filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait

from Oneforall import app
from Oneforall.misc import SUDOERS


# SAFE EDIT
async def safe_edit(msg, text):

    try:
        await msg.edit_text(text)

    except FloodWait as e:

        await asyncio.sleep(e.value)

        try:
            await msg.edit_text(text)
        except:
            pass

    except:
        pass


@app.on_message(
    filters.command(
        ["speedtest", "spt"]
    ) & SUDOERS
)
async def speedtest_command(
    client,
    message: Message
):

    msg = await message.reply_text(
        "⚡ Running Speed Test..."
    )

    image_path = "speedtest.png"

    try:

        process = await asyncio.create_subprocess_shell(

            "speedtest-cli --share --json",

            stdout=asyncio.subprocess.PIPE,

            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()

        if stderr:

            err = stderr.decode()

            if err.strip():

                return await safe_edit(
                    msg,
                    f"❌ Error:\n`{err}`"
                )

        data = json.loads(
            stdout.decode()
        )

        # SPEED
        download = round(
            data["download"] / 1024 / 1024,
            2
        )

        upload = round(
            data["upload"] / 1024 / 1024,
            2
        )

        ping = data["ping"]

        # CLIENT
        isp = data["client"]["isp"]

        country = data["client"]["country"]

        # SERVER
        server = data["server"]["host"]

        sponsor = data["server"]["sponsor"]

        # SHARE IMAGE
        share = data.get("share")

        if share:

            response = requests.get(
                share,
                timeout=30
            )

            with open(
                image_path,
                "wb"
            ) as f:

                f.write(response.content)

        caption = f"""
╭───────────────⭓
│ ⚡ SPEED TEST
├───────────────
│ 📥 Download: {download} Mbps
│ 📤 Upload: {upload} Mbps
│ 🏓 Ping: {ping} ms
├───────────────
│ 🌍 ISP: {isp}
│ 🇮🇳 Country: {country}
├───────────────
│ 🖥 Server: {server}
│ 🏢 Sponsor: {sponsor}
╰───────────────⭓
"""

        if (
            share
            and os.path.exists(
                image_path
            )
        ):

            await message.reply_photo(
                photo=image_path,
                caption=caption
            )

            os.remove(image_path)

        else:

            await message.reply_text(
                caption
            )

        try:
            await msg.delete()
        except:
            pass

    except Exception as e:

        await safe_edit(
            msg,
            f"❌ Error:\n`{e}`"
        )