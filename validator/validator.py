from io import BytesIO
from subprocess import Popen, PIPE

import requests
from flask import Flask, send_file, request

from badge import passing_badge, failing_badge, warning_badge, error_badge

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


def _compute_badge(url):
    process = Popen(['ga4gh-tool-registry-validate ga4gh-tool-discovery.yaml annotations.yml ' + url], stdout=PIPE, stderr=PIPE, shell=True)
    (out, err) = process.communicate()
    if err != 'API returned valid response\n':
        return error_badge()
    else:
        if url == 'failing':
            return failing_badge()
        if url == 'warning':
            return warning_badge()
        else:
            return passing_badge()


@app.route('/trs/validator', methods=['GET'])
def status_badge():
    url = request.args.get('url', '')
    r = requests.get(_compute_badge(url))
    return send_file(BytesIO(r.content), mimetype=r.headers['Content-Type'])

if __name__== '__main__':
    app.run(debug=True,host='0.0.0.0')