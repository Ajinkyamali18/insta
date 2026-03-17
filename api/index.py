from flask import Flask, render_template, request, jsonify
import instaloader
import re

# Ensure flask can find templates from the repo-level templates directory
app = Flask(__name__, template_folder='../templates')

def _extract_shortcode(post_url):
    if not post_url or not isinstance(post_url, str):
        return None
    post_url = post_url.strip()
    # Instagram URL formats: /p/SHORTCODE/, /reel/SHORTCODE/, /tv/SHORTCODE/ or just SHORTCODE
    match = re.search(r"/(?:p|reel|tv)/([A-Za-z0-9_\-]+)/?", post_url)
    if match:
        return match.group(1)
    if post_url.endswith('/'):
        post_url = post_url[:-1]
    parts = post_url.split('/')
    if parts:
        return parts[-1]
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
            return jsonify({'success': False, 'error': 'Link takali nahi!'}), 400

        shortcode = _extract_shortcode(post_url)
        if not shortcode:
            return jsonify({'success': False, 'error': 'Shortcode extract doch yeta nahii'}), 400

        loader = instaloader.Instaloader(dirname_pattern='/tmp/instaloader', download_pictures=False, save_metadata=False, compress_json=False)
        post = instaloader.Post.from_shortcode(loader.context, shortcode)

        images = []
        if getattr(post, 'typename', '') == 'GraphSidecar':  # Multiple Photos (Carousel)
            for node in post.get_sidecar_nodes():
                images.append(node.display_url)
        else:  # Single Photo/Reel
            images.append(post.display_url)

        return jsonify({'success': True, 'images': images})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# For Vercel Python, exporting `app` as WSGI is sufficient. Keep compatibility alias (does not do direct app(event, context)).
handler = app