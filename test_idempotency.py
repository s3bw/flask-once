from werkzeug.exceptions import BadRequest

import pytest

import flask_once
from flask_once import idempotent


@pytest.fixture()
def flask_json(flask_app):
    from flask import jsonify

    response = {
        "status_code": 200,
        "content_type": "application/json",
        "response": b'{"message":"CACHED"}\n',
        "request": b'{"x": "z"}',
    }
    flask_app.cache = {"key": response}
    flask_once.attach(flask_app, flask_app.cache)

    @flask_app.route("/endpoint", methods=["POST", "GET", "PUT"])
    @idempotent()
    def json_endpoint():
        return jsonify(message="OK")

    @flask_app.errorhandler(BadRequest)
    def handle_bad_request(e):
        return jsonify(message=e.description), 400

    yield flask_app.test_client()


@pytest.mark.parametrize("key, expected_message", [("a", "OK"), ("key", "CACHED")])
def test_route_method_not_called(flask_json, key, expected_message):
    resp = flask_json.post(
        "/endpoint", json={"x": "z"}, headers={"Idempotent-Key": key}
    )
    assert resp.status_code == 200
    assert resp.json["message"] == expected_message
    assert resp.headers["Idempotent-Key"] == key


def test_data_mismatch(flask_json):
    resp = flask_json.post(
        "/endpoint", json={"x": "z"}, headers={"Idempotent-Key": "a"}
    )
    assert resp.status_code == 200

    resp = flask_json.post(
        "/endpoint", json={"x": "y"}, headers={"Idempotent-Key": "a"}
    )
    assert resp.status_code == 400
    assert "request data does not match" in resp.json["message"]


def test_4xx_avoid_cache(flask_json):
    resp = flask_json.post("/endpoint")
    assert resp.status_code == 400

    resp = flask_json.post("/endpoint", headers={"Idempotent-Key": "a"})
    assert resp.status_code == 200


def test_no_idempotent_header(flask_json):
    resp = flask_json.post("/endpoint")
    assert resp.status_code == 400
    assert "Missing 'Idempotent-Key' field" in resp.json["message"]
