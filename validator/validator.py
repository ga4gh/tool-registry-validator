from io import BytesIO
from subprocess import Popen, PIPE
import tempfile

import os
import requests
from flask import Flask, send_file, request, Response
# import ga4gh_tool_registry.validate as validate

from badge import passing_badge, failing_badge, warning_badge, error_badge
from constants import RELAXED_SWAGGER, SWAGGER

app = Flask(__name__)


def _compute_badge(url):
    # (out, err) = validate(url)
    # if "Failed to establish a new connection" in err:
    #     return error_badge()
    # if err != 'API returned valid response\n':
    #     return failing_badge()
    # else:
    out2 = run_dredd(SWAGGER, url)
    if ' 0 failing, 0 errors' in out2:
        return passing_badge()
    else:
        if ' 0 errors' not in out2:
            return error_badge()
        out3 = run_dredd(RELAXED_SWAGGER, url)
        if ' 0 failing, 0 errors' in out3:
            return warning_badge()
        else:
            return failing_badge()


@app.route('/trs/validator', methods=['GET'])
def status_badge():
    url = request.args.get('url', '')
    r = requests.get(_compute_badge(url))
    return send_file(BytesIO(r.content), mimetype=r.headers['Content-Type'])


@app.route('/trs/validator/debug', methods=['GET'])
def debug():
    url = request.args.get('url', '')
    r = run_dredd(SWAGGER, url)
    response = Response(r, mimetype="text/plain")
    return response


@app.route('/trs/validator/debug2', methods=['GET'])
def debug2():
    url = request.args.get('url', '')
    r = run_dredd(RELAXED_SWAGGER, url)
    response = Response(r, mimetype="text/plain")
    return response


def validate(url):
    # validate.validate('ga4gh-tool-discovery.yaml', 'annotations.yml', url, False, False, False)
    file_directory = os.path.dirname(__file__)
    swagger_file_path = os.path.join(file_directory, RELAXED_SWAGGER)
    command_args = ['ga4gh-tool-registry-validate', swagger_file_path, 'annotations.yml', url + '/tools']
    process = Popen(command_args, stdout=PIPE, stderr=PIPE)
    return process.communicate()


def run_dredd(swagger_filename, url):
    file_directory = os.path.dirname(__file__)
    swagger_file_path = os.path.join(file_directory, swagger_filename)
    hooks_file_path = os.path.join(file_directory, 'hooks.py')
    command_args = ['dredd', swagger_file_path, url, '-l', 'fail', '-c', 'false', '-a', 'python', '-f', hooks_file_path]
    outfile = tempfile.NamedTemporaryFile('w')
    process = Popen(command_args, stdout=outfile, stderr=PIPE)
    process.wait()
    return _temp_file_to_string(outfile)


def _temp_file_to_string(file):
    with open(file.name) as f:
        return f.read()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
