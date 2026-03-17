import os
import re
from flask import Flask, render_template, request, jsonify
import instaloader

# Vercel sathi template folder shodhne
current_dir = os.path.dirname(os.path.abspath(__file__))
template_path = os.path.join(current_dir, '..', 'templates')

app = Flask(__name__, template_folder=template_path)

def _extract_shortcode(post_url):
    if not post_url or not isinstance(post_url, str):
        return None
    post_url = post_url.strip()
    match = re.search(r"/(?:p|reel|tv)/([A-Za-z0-9_\-]+)/?", post_url)
    if match:
        return match.group(1)
    if post_url.endswith('/'):
        post_url = post_url[:-1]
    parts = post_url.split('/')
    if parts:
        candidate = parts[-1].split('?')[0]
        if candidate:
            return candidate
    return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/get_images', methods=['POST'])
def get_images():
    try:
        data = request.get_json(silent=True) or {}
        post_url = (data.get('url') or '').strip()
        if not post_url:
            return jsonify({'success': False, 'error': 'Link taka!'}), 400

        shortcode = _extract_shortcode(post_url)
        if not shortcode:
            return jsonify({'success': False, 'error': 'Shortcode milala nahi.'}), 400

        loader = instaloader.Instaloader(download_pictures=False, save_metadata=False, compress_json=False)
        post = instaloader.Post.from_shortcode(loader.context, shortcode)

        images = []
        if getattr(post, 'typename', '') == 'GraphSidecar':
            for node in post.get_sidecar_nodes():
                images.append(node.display_url)
        else:
            images.append(post.display_url)

        return jsonify({'success': True, 'images': images})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Vercel Python expects a WSGI app object, and this alias is safe.
handler = app

if __name__ == '__main__':
    app.run(debug=True, port=5000)
