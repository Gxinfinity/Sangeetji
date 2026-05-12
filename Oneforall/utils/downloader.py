from os import path
import yt_dlp

ytdl = yt_dlp.YoutubeDL({"extractor_args": {"youtube": {"player_client": ["web_creator"], "player_skip": ["web_embedded_web_player"]}},
    "outtmpl": "downloads/%(id)s.%(ext)s",
    "format": "bestaudio/best",
    "geo_bypass": True,
    "nocheckcertificate": True,
    "cookiefile": "/root/cookies/youtube.txt",
    "js_runtimes": {"bun": "/root/.bun/bin/bun"},
    "remote_components": ["ejs:github"],
})


def download(url: str, my_hook) -> str:
    # 👉 name support
    if not url.startswith("http"):
        url = f"ytsearch1:{url}"

    ydl_optssx = {
        "format": "bestaudio/best",
        "outtmpl": "downloads/%(id)s.%(ext)s",
        "geo_bypass": True,
        "nocheckcertificate": True,
    "cookiefile": "/root/cookies/youtube.txt",
    "js_runtimes": {"bun": "/root/.bun/bin/bun"},
    "remote_components": ["ejs:github"],
        "quiet": True,
        "no_warnings": True,
    }

    try:
        x = yt_dlp.YoutubeDL(ydl_optssx)
        x.add_progress_hook(my_hook)

        # 🔥 extract + download together
        info = x.extract_info(url, download=True)

        # 👉 search case handle
        if "entries" in info:
            info = info["entries"][0]

    except Exception as y_e:
        print(y_e)
        return None

    # ✅ correct file path
    xyz = x.prepare_filename(info)
    return xyz