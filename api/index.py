import re
from flask import Flask, render_template, request, jsonify

app = Flask(__name__, template_folder="templates")


@app.route("/")
def home():
    try:
        return render_template("index.html")
    except Exception as e:
        return f"""
        <h1>ERROR</h1>
        <pre>{str(e)}</pre>
        """


@app.route("/test")
def test():
    return "OK"