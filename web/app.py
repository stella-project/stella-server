from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/")
def home():
    html = "<h1> Hello, world! </h1>"
    # html = '<h1>Bad Request</h1>', 400

    return html


@app.route("/user/<name>")
def user(name):
    return "<h1>Hi, {}!</h1>".format(name)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
