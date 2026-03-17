import os
from flask import Flask, render_template, request, jsonify
import instaloader

# Vercel sathi template folder shodhne
current_dir = os.path.dirname(os.path.abspath(__file__))
template_path = os.path.join(current_dir, '..', 'templates')

app = Flask(__name__, template_folder=template_path)
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

        # URL madhun shortcode kadhne
        shortcode = post_url.strip('/').split('/')[-1].split('?')[0]
        
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

# Vercel sathi handler chi garaj naste pan app export karne garjeche aahe