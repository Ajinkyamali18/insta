import os
import re
from flask import Flask, render_template, request, jsonify
import instaloader

# Vercel sathi simple path logic
# 'api' folder chya baher asleli index.html vaparnyasathi
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
app = Flask(__name__, template_folder=base_dir)

def _extract_shortcode(post_url):
    if not post_url or not isinstance(post_url, str):
        return None
    post_url = post_url.strip()
    # Regex vaprun shortcode kadhne (p/reel/tv)
    match = re.search(r"/(?:p|reel|tv)/([A-Za-z0-9_\-]+)/?", post_url)
    if match:
        return match.group(1)
    
    # Jar regex fail jale tar split logic
    temp_url = post_url.strip('/')
    parts = temp_url.split('/')
    if parts:
        return parts[-1].split('?')[0]
    return None

@app.route('/')
def home():
    try:
        # He ata baherchya folder madhli index.html load karel
        return render_template('index.html')
    except Exception as e:
        return f"Error: index.html sapdali nahi. Path: {base_dir} | {str(e)}"

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

        # Instaloader setup
        loader = instaloader.Instaloader(
            download_pictures=False, 
            save_metadata=False, 
            compress_json=False
        )
        
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

# Vercel expects 'app' or 'handler'
handler = app