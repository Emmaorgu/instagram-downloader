import os
import instaloader
from flask import Flask, render_template, request, send_file
import re

app = Flask(__name__)

# Ensure the "downloads" folder exists
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)


def download_instagram_video(url):
    """Downloads Instagram video using Instaloader."""
    L = instaloader.Instaloader()

    # Extract shortcode from URL
    match = re.search(r"https://www.instagram.com/reel/([A-Za-z0-9_-]+)", url)
    if not match:
        return None, "Invalid Instagram URL. Please provide a valid reel link."

    shortcode = match.group(1)

    try:
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        video_url = post.video_url

        if not video_url:
            return None, "This Instagram post does not contain a video."

        file_path = os.path.join(DOWNLOAD_FOLDER, f"{shortcode}.mp4")

        # Download video
        os.system(f"wget -O {file_path} {video_url}")

        return file_path, None

    except Exception as e:
        return None, f"Error: {str(e)}"


@app.route("/", methods=["GET", "POST"])
def index():
    """Home page for the Instagram video downloader."""
    if request.method == "POST":
        url = request.form.get("url")
        if not url:
            return render_template("index.html", error="Please enter a URL.")

        file_path, error = download_instagram_video(url)
        if error:
            return render_template("index.html", error=error)

        return send_file(file_path, as_attachment=True)

    return render_template("index.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Ensure correct port
    app.run(host="0.0.0.0", port=port)  # Bind to all network interfaces
