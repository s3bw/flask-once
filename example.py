from flask import Flask
from flask import jsonify
from flask import current_app

import flask_once
from flask_once import idempotent


app = Flask(__name__)

app.score = 0
app.cache = dict()

flask_once.attach(app, app.cache)


@app.route("/endpoint", methods=["POST"])
@idempotent()
def create_transaction():
    current_app.score += 1
    return jsonify(transaction=current_app.score)


@app.route("/duplicate", methods=["POST"])
def create_duplicate():
    current_app.score += 1
    return jsonify(transaction=current_app.score)


if __name__ == '__main__':
    app.run()
