from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hi I am a Derpy Search Engine"
