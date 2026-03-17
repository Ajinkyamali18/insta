import os
from flask import Flask, render_template, request, jsonify
import instaloader

# Vercel sathi path set karnyacha sarvat safe marg
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
template_dir = os.path.join(base_dir, 'templates')

app = Flask(__name__, template_folder=template_dir)

L = instaloader.Instaloader()

@app.route('/')
def home():
    # Jar file sapdali nahi tar error screen var disel (White screen yenyapekshya)
    try:
        return render_template('index.html')
    except Exception as e:
        return f"Templates folder sapdat nahiye. Path: {template_dir}. Error: {str(e)}"

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