import typing as tp
import logging

from flask import Flask, jsonify, Response

import settings

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY=settings.SECRET_KEY
)


@app.route('/')
def index() -> tp.Tuple[Response, int]:
    return jsonify({'ok': 'Main page'}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
