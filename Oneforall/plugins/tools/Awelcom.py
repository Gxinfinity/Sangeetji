import os
import time
import random
import tempfile
import subprocess

import httpx
import edge_tts
import whisper

from pyrogram import filters
from pyrogram.enums import ChatAction
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery
)

from motor.motor_asyncio import AsyncIOMotorClient

from Oneforall import app

# ================= CONFIG =================

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
MODEL = "deepseek/deepseek-chat"

USER_COOLDOWN = {}

HTTP = httpx.AsyncClient(
    follow_redirects=True,
    timeout=45.0
)

# ================= DATABASE =================

mongo_client = AsyncIOMotorClient(MONGO_URL)

db = mongo_client["ChatBotDB"]

chats_col = db["chats"]


async def is_chatbot_on(chat_id):

    chat = await chats_col.find_one(
        {"chat_id": chat_id}
    )

    return chat.get("status", False) if chat else False


async def toggle_chatbot(chat_id, status):

    await chats_col.update_one(
        {"chat_id": chat_id},
        {"$set": {"status": status}},
        upsert=True
    )


# ================= AI =================

async def ask_ai(prompt):

    if not OPENROUTER_API_KEY:
        return "❌ OPENROUTER_API_KEY missing!"

    try:

        response = await HTTP.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": MODEL,
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "You are a cute smart Indian girl chatting naturally in Hindi. "
                            "Reply shortly, casually and naturally like a real human. "
                            "Never say you are AI or chatbot."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }
        )

        if response.status_code != 200:
            return f"❌ API Error: {response.status_code}"

        data = response.json()

        return data["choices"][0]["message"]["content"][:4000]

    except Exception as e:

        return f"❌ Error: {e}"


# ================= COOLDOWN =================

def cooldown(user_id):

    now = time.time()

    if now - USER_COOLDOWN.get(user_id, 0) < 3:
        return False

    USER_COOLDOWN[user_id] = now

    return True


# ================= CHATBOT PANEL =================

@app.on_message(filters.command("chatbot"))
async def chatbot_panel(_, message: Message):

    status = await is_chatbot_on(message.chat.id)

    text = (
        "🤖 **ChatBot Control Panel**\n\n"
        f"Status: {'✅ Enabled' if status else '❌ Disabled'}"
    )

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "Toggle ChatBot",
                    callback_data="toggle_chatbot"
                )
            ]
        ]
    )

    await message.reply_text(
        text,
        reply_markup=keyboard
    )


@app.on_callback_query(filters.regex("toggle_chatbot"))
async def toggle_callback(_, query: CallbackQuery):

    chat_id = query.message.chat.id

    current = await is_chatbot_on(chat_id)

    await toggle_chatbot(chat_id, not current)

    new_status = (
        "✅ Enabled"
        if not current
        else "❌ Disabled"
    )

    await query.message.edit_text(
        f"🤖 **ChatBot Control Panel**\n\nStatus: {new_status}",
        reply_markup=query.message.reply_markup
    )


# ================= /ASK =================

@app.on_message(filters.command("ask"))
async def ask_command(_, message: Message):

    if not message.from_user:
        return

    if not cooldown(message.from_user.id):

        return await message.reply_text(
            "✋ Slow down bro."
        )

    if len(message.command) < 2:

        return await message.reply_text(
            "Usage: /ask hello"
        )

    query = message.text.split(None, 1)[1]

    await app.send_chat_action(
        message.chat.id,
        ChatAction.TYPING
    )

    reply = await ask_ai(query)

    await message.reply_text(
        reply,
        disable_web_page_preview=True
    )

    await send_emotion_sticker(
        message,
        reply
    )


# ================= AUTO CHATBOT =================

@app.on_message(
    filters.text
    & ~filters.bot
    & ~filters.command(["ask", "chatbot"])
)
async def auto_chatbot(_, message: Message):

    if not message.from_user:
        return

    if not await is_chatbot_on(message.chat.id):
        return

    if not cooldown(message.from_user.id):
        return

    await app.send_chat_action(
        message.chat.id,
        ChatAction.TYPING
    )

    reply = await ask_ai(message.text)

    await message.reply_text(
        reply,
        disable_web_page_preview=True
    )

    await send_emotion_sticker(
        message,
        reply
    )


# ================= STICKERS =================

EMOTION_STICKERS = {

    "happy": [
        "CAACAgUAAxkBAAED7-RqBc5ZE5OA2Nz5V_7-PhBV2KQIVwACpREAAlNJqVU8pPE0pVx6YjsE"
    ],

    "sad": [
        "CAACAgIAAxkBAAED7-JqBc2jeoS0-fiTIQABD6tfTRqTvt0AAuZqAAKLAdFKErLbHiQR86s7BA"
    ],

    "angry": [
        "CAACAgUAAxkBAAED79pqBcu-ItRqPWX7fmhydTdutAdxEAACEBIAAm09aVdzd6Agos8ZbTsE"
    ],

    "love": [
        "CAACAgEAAxkBAAED7-BqBc1Nt7Pzr2rAMmAfYSyVIluHSgACJwYAAlGxkEfjp2zKLaDR5TsE"
    ]
}


def detect_emotion(text):

    text = text.lower()

    if any(
        x in text
        for x in [
            "love",
            "pyar",
            "baby",
            "miss",
            "cute"
        ]
    ):
        return "love"

    if any(
        x in text
        for x in [
            "sad",
            "cry",
            "dukhi",
            "hurt",
            "alone",
            "rona"
        ]
    ):
        return "sad"

    if any(
        x in text
        for x in [
            "angry",
            "mad",
            "gussa",
            "abuse"
        ]
    ):
        return "angry"

    return "happy"


async def send_emotion_sticker(message, text):

    try:

        if random.randint(1, 4) != 1:
            return

        emotion = detect_emotion(text)

        if emotion in EMOTION_STICKERS:

            await message.reply_sticker(
                random.choice(
                    EMOTION_STICKERS[emotion]
                )
            )

    except Exception as e:

        print(f"Sticker Error: {e}")


# ================= VOICE REPLY =================

@app.on_message(filters.voice & ~filters.bot)
async def voice_ai_reply(_, message: Message):

    if not message.from_user:
        return

    if not await is_chatbot_on(message.chat.id):
        return

    try:

        await app.send_chat_action(
            message.chat.id,
            ChatAction.TYPING
        )

        # download
        voice_path = await message.download()

        wav_path = f"{voice_path}.wav"

        # convert
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i",
                voice_path,
                "-ar",
                "16000",
                "-ac",
                "1",
                "-c:a",
                "pcm_s16le",
                wav_path
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        # whisper
        model = whisper.load_model("tiny")

        result = model.transcribe(
            wav_path,
            language="hi",
            fp16=False
        )

        user_text = result["text"]

        # ai reply
        ai_reply = await ask_ai(
            f"Reply only in Hindi naturally: {user_text}"
        )

        # temp file
        with tempfile.NamedTemporaryFile(
            suffix=".mp3",
            delete=False
        ) as tmp:

            tts_file = tmp.name

        # tts
        communicate = edge_tts.Communicate(
            text=ai_reply,
            voice="hi-IN-SwaraNeural",
            rate="-10%",
            pitch="-2Hz"
        )

        await communicate.save(tts_file)

        # send voice
        await message.reply_voice(
            tts_file,
            caption="🎙 AI Voice Reply"
        )

        await send_emotion_sticker(
            message,
            ai_reply
        )

    except Exception as e:

        await message.reply_text(
            f"❌ Voice Error: {e}"
        )