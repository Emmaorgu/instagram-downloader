from flask import Flask, render_template, request, send_file
import os
import instaloader

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        try:
            L = instaloader.Instaloader()
            shortcode = url.split("/")[-2]  # Extract shortcode from URL
            L.download_post(instaloader.Post.from_shortcode(L.context, shortcode), target="downloads")

            # Find the downloaded video file
            for file in os.listdir("downloads"):
                if file.endswith(".mp4"):
                    video_path = os.path.join("downloads", file)
                    return send_file(video_path, as_attachment=True)
        except Exception as e:
            return f"Error: {e}"
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
