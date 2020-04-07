from flask import Flask

import pytest


@pytest.fixture(scope="function")
def flask_app():
    app = Flask(__name__)
    with app.app_context():
        yield app
