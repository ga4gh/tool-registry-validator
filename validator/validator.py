from io import BytesIO
from subprocess import Popen, PIPE

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
        (out2, err2) = run_dredd(SWAGGER, url)
        if ' 0 failing, 0 errors' in out2:
            return passing_badge()
        else:
            if ' 0 errors' not in out2:
                return error_badge()
            (out3, err3) = run_dredd(RELAXED_SWAGGER, url)
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
    r = _compute_debug(url)
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
    command_args = ['dredd', swagger_file_path, url, '-l', 'fail']
    process = Popen(command_args, stdout=PIPE, stderr=PIPE)
    return process.communicate()


def _compute_debug(url):
    (out, err) = run_dredd(SWAGGER, url)
    return out


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
