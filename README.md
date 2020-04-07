<h1 align='center'>
    Flask-Once
</h1>

<h4 align='center'>
    Idempotent decorator for flask routes.
</h4>

Inspired by [stripe's idempotent](https://stripe.com/docs/api/idempotent_requests)
endpoints.

## Install

```bash
pip install flask-once
```

## Usage

```python
import uuid

from flask import Flask
from flask import jsonify

import flask_once
from flask_once import idempotent


class Cache(dict):
    pass


app = Flask(__name__)
app.cache = Cache()

flask_once.attach(app, app.cache)

@app.route("/endpoint", methods=["POST"])
@idempotent()
def create_transaction():
    uuid = str(uuid.uuid4())
    return jsonify(transaction=uuid)
```

## Test

```bash
pip install requirements-dev.txt
make test
```

## Run example

Start app

```bash
python example.py
```

Curl endpoints

```bash
curl localhost:5000/endpoint \
    -H 'Idempotent-Key: x'
```

## Upload

```bash
make tag
```

## TODO:

- Only cache routes with decorator.
- Add tests endpoints not wrapped in idempotency
