from flask import Flask, render_template, request, send_file
from pytube import YouTube
import os

app = Flask(__name__)
DOWNLOAD_FOLDER = "downloads"
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        media_type = request.form['type']
        try:
            yt = YouTube(url)
            if media_type == 'audio':
                stream = yt.streams.filter(only_audio=True).first()
                out_file = stream.download(output_path=DOWNLOAD_FOLDER)
                base, ext = os.path.splitext(out_file)
                new_file = base + '.mp3'
                os.rename(out_file, new_file)
                return send_file(new_file, as_attachment=True)
            elif media_type == 'video':
                stream = yt.streams.get_highest_resolution()
                out_file = stream.download(output_path=DOWNLOAD_FOLDER)
                return send_file(out_file, as_attachment=True)
        except Exception as e:
            return f"Error: {str(e)}"
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
