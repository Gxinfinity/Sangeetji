import logging
from googlesearch import search
from pyrogram import filters
from SafoneAPI import SafoneAPI
from Oneforall import app

logging.basicConfig(level=logging.INFO)


# GOOGLE SEARCH
@app.on_message(filters.command(["google", "gle"]))
async def google_search(client, message):

    if len(message.command) < 2 and not message.reply_to_message:

        return await message.reply_text(
            "**Example:**\n`/google roohi`"
        )

    if (
        message.reply_to_message
        and message.reply_to_message.text
    ):

        query = message.reply_to_message.text

    else:

        query = " ".join(message.command[1:])

    msg = await message.reply_text(
        "🔎 Searching Google..."
    )

    try:

        # SIMPLE SEARCH
        results = list(
            search(
                query,
                num_results=5
            )
        )

        if not results:

            return await msg.edit(
                "❌ No results found."
            )

        text = (
            f"🔍 **Google Results For:**\n"
            f"`{query}`\n\n"
        )

        for index, link in enumerate(
            results,
            start=1
        ):

            text += (
                f"{index}. {link}\n\n"
            )

        await msg.edit(
            text,
            disable_web_page_preview=True
        )

    except Exception as e:

        logging.exception(e)

        await msg.edit(
            f"❌ Error:\n`{e}`"
        )

# PLAY STORE SEARCH
@app.on_message(filters.command(["app", "apps"]))
async def playstore_search(client, message):

    if len(message.command) < 2 and not message.reply_to_message:
        return await message.reply_text(
            "**Example:**\n`/app Free Fire`"
        )

    if message.reply_to_message and message.reply_to_message.text:
        query = message.reply_to_message.text
    else:
        query = " ".join(message.command[1:])

    msg = await message.reply_text(
        "**📱 Searching on Play Store...**"
    )

    try:
        data = await SafoneAPI().apps(query, 1)

        if not data or "results" not in data:
            return await msg.edit("❌ No app found.")

        result = data["results"][0]

        title = result.get("title", "Unknown")
        developer = result.get("developer", "Unknown")
        description = result.get("description", "No description")
        link = result.get("link", "")
        icon = result.get("icon", "")
        app_id = result.get("id", "Unknown")

        caption = (
            f"**📱 Title:** [{title}]({link})\n"
            f"**🆔 ID:** `{app_id}`\n"
            f"**👨‍💻 Developer:** {developer}\n\n"
            f"**📝 Description:**\n{description}"
        )

        if icon:
            await message.reply_photo(
                photo=icon,
                caption=caption
            )
        else:
            await message.reply_text(
                caption,
                disable_web_page_preview=True
            )

        await msg.delete()

    except Exception as e:
        logging.exception(e)
        await msg.edit(f"❌ Error:\n`{e}`")