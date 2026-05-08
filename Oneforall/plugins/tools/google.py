import asyncio
import logging
import random

from ddgs import DDGS
from googlesearch import search
from pyrogram import filters
from pyrogram.errors import FloodWait
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from SafoneAPI import SafoneAPI
from Oneforall import app

logging.basicConfig(level=logging.INFO)

# RANDOM USER AGENTS
USER_AGENTS = [

    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124.0 Safari/537.36",

    "Mozilla/5.0 (Linux; Android 14) Chrome/123.0 Mobile Safari/537.36",

    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) Safari/604.1",

    "Mozilla/5.0 (X11; Linux x86_64) Firefox/126.0",

    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Safari/605.1.15",
]


# SAFE EDIT
async def safe_edit(message, text, **kwargs):

    try:

        await message.edit_text(
            text,
            **kwargs
        )

    except FloodWait as e:

        await asyncio.sleep(
            e.value
        )

        await message.edit_text(
            text,
            **kwargs
        )

    except Exception as e:

        print(e)


# GOOGLE + MULTI SEARCH
@app.on_message(
    filters.command(
        ["google", "gle"]
    )
)
async def google_search(
    client,
    message
):

    if (
        len(message.command) < 2
        and not message.reply_to_message
    ):

        return await message.reply_text(
            "**Usage:**\n`/google roohi`"
        )

    # QUERY
    if (
        message.reply_to_message
        and message.reply_to_message.text
    ):

        query = (
            message.reply_to_message.text
        )

    else:

        query = " ".join(
            message.command[1:]
        )

    msg = await message.reply_text(
        "🔎 Searching All Engines..."
    )

    text = (
        "╭────────────────⭓\n"
        "│ 🔍 SEARCH RESULTS\n"
        "├────────────────\n"
        f"│ 📝 Query: `{query}`\n"
        "╰────────────────⭓\n\n"
    )

    found = False

    # GOOGLE
    try:

        google_results = list(
            search(
                query,
                num_results=5,
                sleep_interval=2,
                advanced=True
            )
        )

        if google_results:

            text += (
                "🌐 **GOOGLE**\n\n"
            )

            for i, r in enumerate(
                google_results,
                start=1
            ):

                try:

                    title = (
                        getattr(
                            r,
                            "title",
                            "Result"
                        )
                    )

                    url = (
                        getattr(
                            r,
                            "url",
                            str(r)
                        )
                    )

                    desc = (
                        getattr(
                            r,
                            "description",
                            ""
                        )
                    )

                    text += (
                        f"➤ [{title}]({url})\n"
                        f"└ `{desc}`\n\n"
                    )

                except:

                    text += (
                        f"➤ {r}\n\n"
                    )

            found = True

    except Exception as e:

        logging.exception(e)

    # DUCKDUCKGO + BING
    try:

        with DDGS() as ddgs:

            ddg_results = list(
                ddgs.text(
                    query,
                    max_results=8
                )
            )

        if ddg_results:

            text += (
                "🦆 **DUCKDUCKGO / BING**\n\n"
            )

            for r in ddg_results:

                title = r.get(
                    "title",
                    "No Title"
                )

                href = r.get(
                    "href",
                    ""
                )

                body = r.get(
                    "body",
                    ""
                )

                text += (
                    f"➤ [{title}]({href})\n"
                    f"└ `{body[:80]}`\n\n"
                )

            found = True

    except Exception as e:

        logging.exception(e)

    # YAHOO STYLE SEARCH
    try:

        with DDGS() as ddgs:

            news_results = list(
                ddgs.news(
                    query,
                    max_results=5
                )
            )

        if news_results:

            text += (
                "📰 **YAHOO / NEWS**\n\n"
            )

            for r in news_results:

                title = r.get(
                    "title",
                    "News"
                )

                url = r.get(
                    "url",
                    ""
                )

                text += (
                    f"➤ [{title}]({url})\n\n"
                )

            found = True

    except Exception as e:

        logging.exception(e)

    if not found:

        return await safe_edit(
            msg,
            "❌ No results found."
        )

    # LIMIT FIX
    if len(text) > 4000:

        text = text[:3900] + "\n\n..."

    buttons = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton(
                "🔍 Search Again",
                switch_inline_query_current_chat=""
            )
        ]]
    )

    await safe_edit(
        msg,
        text,
        disable_web_page_preview=True,
        reply_markup=buttons
    )


# PLAY STORE
@app.on_message(
    filters.command(
        ["app", "apps"]
    )
)
async def playstore_search(
    client,
    message
):

    if (
        len(message.command) < 2
        and not message.reply_to_message
    ):

        return await message.reply_text(
            "**Usage:**\n`/app Spotify`"
        )

    if (
        message.reply_to_message
        and message.reply_to_message.text
    ):

        query = (
            message.reply_to_message.text
        )

    else:

        query = " ".join(
            message.command[1:]
        )

    msg = await message.reply_text(
        "📱 Searching Play Store..."
    )

    try:

        data = await SafoneAPI().apps(
            query,
            1
        )

        if (
            not data
            or "results" not in data
        ):

            return await safe_edit(
                msg,
                "❌ No app found."
            )

        result = data["results"][0]

        title = result.get(
            "title",
            "Unknown"
        )

        developer = result.get(
            "developer",
            "Unknown"
        )

        description = result.get(
            "description",
            "No description"
        )

        link = result.get(
            "link",
            ""
        )

        icon = result.get(
            "icon",
            ""
        )

        app_id = result.get(
            "id",
            "Unknown"
        )

        caption = (
            "╭────────────────⭓\n"
            "│ 📱 PLAY STORE APP\n"
            "├────────────────\n"
            f"│ 🏷 Name: [{title}]({link})\n"
            f"│ 🆔 ID: `{app_id}`\n"
            f"│ 👨‍💻 Dev: {developer}\n"
            "╰────────────────⭓\n\n"
            f"📝 {description}"
        )

        buttons = InlineKeyboardMarkup(
            [[
                InlineKeyboardButton(
                    "📥 Open App",
                    url=link
                )
            ]]
        )

        if icon:

            await message.reply_photo(
                photo=icon,
                caption=caption,
                reply_markup=buttons
            )

        else:

            await message.reply_text(
                caption,
                reply_markup=buttons
            )

        await msg.delete()

    except FloodWait as e:

        await asyncio.sleep(
            e.value
        )

    except Exception as e:

        logging.exception(e)

        await safe_edit(
            msg,
            f"❌ Error:\n`{e}`"
        )