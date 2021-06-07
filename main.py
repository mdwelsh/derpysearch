from flask import Flask, render_template

import gentext

app = Flask(__name__)


@app.route("/")
def home():
    result = gentext.randomtext()
    return render_template('home.html', result=result)


# For local testing only.
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
