from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hi I am a Derpy Search Engine"


# For local testing only.
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
