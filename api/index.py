from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>WORKING PERFECT</h1>"

@app.route("/test")
def test():
    return "OK"