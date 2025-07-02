from flask import Flask, request, redirect
import subprocess

app = Flask(__name__)

# ✅ Simple in-memory cache
cache = {}

@app.route('/')
def home():
    return "✅ Use /watch?id=YOUTUBE_ID to stream ad-free"

@app.route('/watch')
def watch():
    vid = request.args.get("id")
    if not vid:
        return "Missing video ID", 400

    # ✅ Check cache first
    if vid in cache:
        print(f"🔁 Using cached stream for {vid}")
        return redirect(cache[vid])

    try:
        yt_url = f"https://www.youtube.com/watch?v={vid}"
        print(f"🎯 Fetching stream for: {yt_url}")

        # ✅ yt-dlp command: Get best 720p or lower with audio (progressive)
        result = subprocess.run(
            ["yt-dlp", "-f", "best[height<=720][ext=mp4]/best[ext=mp4]", "-g", yt_url],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=15
        )

        urls = result.stdout.decode().strip().split("\n")
        if not urls or not urls[0].startswith("http"):
            return "❌ Failed to get stream URL", 500

        stream_url = urls[0]

        # ✅ Save to cache
        cache[vid] = stream_url
        print(f"✅ Cached stream: {stream_url}")

        return redirect(stream_url)

    except Exception as e:
        return f"❌ Error: {str(e)}", 500

# ✅ Needed to run locally or on Render
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
