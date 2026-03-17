import os
from flask import Flask, render_template, request, jsonify
import instaloader

# Path set karne
template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
app = Flask(__name__, template_folder=template_dir)

L = instaloader.Instaloader()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/get_images', methods=['POST'])
def get_images():
    try:
        data = request.json
        post_url = data.get('url', '')
        if not post_url:
            return jsonify({'success': False, 'error': 'Link taka!'})

        temp_url = post_url.strip('/')
        shortcode = temp_url.split('/')[-1]
        
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        
        images = []
        if post.typename == 'GraphSidecar':
            for node in post.get_sidecar_nodes():
                images.append(node.display_url)
        else:
            images.append(post.display_url)
            
        return jsonify({'success': True, 'images': images})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# Vercel sathi he khup mahatvache aahe
# Handler kadhun taka, fakt app export kara