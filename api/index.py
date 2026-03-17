from flask import Flask, render_template, request, jsonify
import instaloader

app = Flask(__name__)
L = instaloader.Instaloader()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/get_images', methods=['POST'])
def get_images():
    try:
        data = request.json
        post_url = data.get('url')
        if not post_url:
            return jsonify({'success': False, 'error': 'Link takali nahi!'})

        # Link madhun shortcode kadhne
        shortcode = post_url.split("/")[-2] if post_url.endswith("/") else post_url.split("/")[-1]
        
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        
        images = []
        if post.typename == 'GraphSidecar': # Multiple Photos (Carousel)
            for node in post.get_sidecar_nodes():
                images.append(node.display_url)
        else: # Single Photo or Reel
            images.append(post.display_url)
            
        return jsonify({'success': True, 'images': images})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# Vercel sathi handler
def handler(event, context):
    return app(event, context)