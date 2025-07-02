from flask import Flask, request, redirect
import subprocess

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Server is up. Use /watch?id=YOUTUBE_ID"

@app.route('/watch')
def watch():
    vid = request.args.get("id")
    if not vid:
        return "Missing YouTube video ID", 400

    try:
        yt_url = f"https://www.youtube.com/watch?v={vid}"
        result = subprocess.run(["yt-dlp", "-g", yt_url], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10)
        urls = result.stdout.decode().strip().split("\n")
        return redirect(urls[0])
    except Exception as e:
        return f"❌ Error: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
