from flask import Flask, render_template, request, jsonify
import instaloader
import os

app = Flask(__name__)

L = instaloader.Instaloader()

USERNAME = None

# 🔹 Home page
@app.route("/")
def home():
    return render_template("index.html")


# 🔹 LOGIN API
@app.route("/login", methods=["POST"])
def login():
    global USERNAME
    data = request.json

    username = data.get("username")
    password = data.get("password")

    try:
        L.login(username, password)
        L.save_session_to_file("session")

        USERNAME = username

        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


# 🔹 LOAD SESSION (auto login like friendly app)
@app.route("/load-session")
def load_session():
    global USERNAME
    try:
        if USERNAME:
            L.load_session_from_file(USERNAME, "session")
            return {"status": "loaded"}
    except:
        pass

    return {"status": "no session"}


# 🔹 DOWNLOAD POST
@app.route("/download", methods=["POST"])
def download():
    data = request.json
    url = data.get("url")

    try:
        shortcode = url.split("/")[-2]
        post = instaloader.Post.from_shortcode(L.context, shortcode)

        L.download_post(post, target="downloads")

        return {"status": "downloaded"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


# 🔹 PORT FIX (Render deploy)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))