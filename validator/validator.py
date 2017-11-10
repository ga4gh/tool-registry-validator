from io import BytesIO
from subprocess import Popen, PIPE
import requests
from flask import Flask, send_file, request
# import ga4gh_tool_registry.validate as validate
from badge import passing_badge, failing_badge, warning_badge, error_badge

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


def _compute_badge(url):
    # validate.validate('ga4gh-tool-discovery.yaml', 'annotations.yml', url, False, False, False)
    commandargs = ['ga4gh-tool-registry-validate', 'ga4gh-tool-discovery.yaml', 'annotations.yml', url]
    process = Popen(commandargs, stdout=PIPE, stderr=PIPE)
    (out, err) = process.communicate()
    if "Failed to establish a new connection" in err:
        return error_badge()
    if err != 'API returned valid response\n':
        return failing_badge()
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


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
