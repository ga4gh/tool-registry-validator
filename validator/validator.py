from io import BytesIO

import os

import requests
from flask import Flask, send_file, request

from badge import passing_badge, failing_badge, warning_badge, error_badge

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


def _compute_badge(url):
    os.system('ga4gh-tool-registry-validate ga4gh-tool-discovery.yaml annotations.yml ' + url)
    if url == 'dockstore':
        return passing_badge()
    if url == 'warning':
        return warning_badge()
    if url == 'error':
        return error_badge()
    else:
        return failing_badge()


@app.route('/trs/validator', methods=['GET'])
def status_badge():
    url = request.args.get('url', '')
    r = requests.get(_compute_badge(url))
    return send_file(BytesIO(r.content), mimetype=r.headers['Content-Type'])

if __name__== '__main__':
    app.run(debug=True,host='0.0.0.0')