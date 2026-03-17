import re
from flask import Flask, render_template, request, jsonify
import instaloader

# Templates folder path (VERY IMPORTANT)
app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates")
)


# 🔍 Shortcode extract function
def _extract_shortcode(post_url):
    if not post_url:
        return None
    match = re.search(r"/(?:p|reel|tv)/([A-Za-z0-9_\-]+)/?", post_url)
    if match:
        return match.group(1)
    return post_url.strip('/').split('/')[-1].split('?')[0]


# 🏠 Home route
@app.route("/")
def home():
    try:
        return render_template("index.html")
    except Exception as e:
        return f"❌ index.html load jhala nahi: {str(e)}"


# 📸 API route
@app.route("/api/get_images", methods=["POST"])
def get_images():
    try:
        data = request.get_json(silent=True) or {}
        post_url = data.get("url", "").strip()

        if not post_url:
            return jsonify({"success": False, "error": "Link taka!"})

        shortcode = _extract_shortcode(post_url)

        loader = instaloader.Instaloader()
        post = instaloader.Post.from_shortcode(loader.context, shortcode)

        images = []

        # Multiple images (carousel)
        if getattr(post, "typename", "") == "GraphSidecar":
            for node in post.get_sidecar_nodes():
                images.append(node.display_url)
        else:
            images.append(post.display_url)

        return jsonify({"success": True, "images": images})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


# 🧪 Debug route (optional but useful)
@app.route("/test")
def test():
    return "✅ API Working!"


