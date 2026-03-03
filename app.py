from flask import Flask, request, jsonify, render_template
import yt_dlp

# Template folder '.' dewar karon hocche jeno index.html same folder e rakha jay
app = Flask(__name__, template_folder='.')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/get-url', methods=['POST'])
def get_url():
    data = request.json
    video_url = data.get('url')
    res = data.get('resolution')

    if not video_url:
        return jsonify({'success': False, 'error': 'Link dewa hoyni'})

    # Free server e ffmpeg chara video+audio ekshathe pawar jonno nicher format use kora holo
    if res == 'best':
        format_str = 'best'
    else:
        format_str = f'best[height<={res}]'

    ydl_opts = {
        'format': format_str,
        'noplaylist': True,
        'quiet': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            download_url = info.get('url')
            return jsonify({'success': True, 'download_url': download_url})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
  
