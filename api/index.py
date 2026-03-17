import os
import re
from flask import Flask, render_template, request, jsonify
import instaloader

# Vercel sathi Path Logic
# 'api' folder chya ek level baher root madhe index.html aahe
app = Flask(__name__, template_folder='..')

def _extract_shortcode(post_url):
    if not post_url: return None
    match = re.search(r"/(?:p|reel|tv)/([A-Za-z0-9_\-]+)/?", post_url)
    if match: return match.group(1)
    return post_url.strip('/').split('/')[-1].split('?')[0]

@app.route('/')
def home():
    try:
        # He root madhli index.html load karel
        return render_template('index.html')
    except Exception as e:
        return f"Error: index.html sapdali nahi. Error: {str(e)}"

@app.route('/api/get_images', methods=['POST'])
def get_images():
    try:
        data = request.get_json(silent=True) or {}
        post_url = data.get('url', '').strip()
        if not post_url:
            return jsonify({'success': False, 'error': 'Link taka!'})

        shortcode = _extract_shortcode(post_url)
        loader = instaloader.Instaloader()
        post = instaloader.Post.from_shortcode(loader.context, shortcode)

        images = []
        if getattr(post, 'typename', '') == 'GraphSidecar':
            for node in post.get_sidecar_nodes():
                images.append(node.display_url)
        else:
            images.append(post.display_url)

        return jsonify({'success': True, 'images': images})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# Vercel sathi alias
handler = app