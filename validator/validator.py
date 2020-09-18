from io import BytesIO
from subprocess import Popen, PIPE
import tempfile

import re
from healthcheck import HealthCheck, EnvironmentDump
import os
import requests
from flask import Flask, send_file, request, Response
from flask_caching import Cache
# import ga4gh_tool_registry.validate as validate
import urllib
import createProcessedYAML
from badge import passing_badge, failing_badge, warning_badge, error_badge, unknown_badge
from constants import SWAGGER, EXPECTED_PASSING_TESTS, GITHUB_BASEURL, GITHUB_BRANCH, GITHUB_FILE_PATH
import uwsgi
app = Flask(__name__)

health = HealthCheck(app, "/health_check")
envdump = EnvironmentDump(app, "/environment")
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

BADGE_CACHE_TIMEOUT = 24*60*60
LOG_CACHE_TIMEOUT = 24*60*60


def _compute_badge(url):
    # (out, err) = validate(url)
    # if "Failed to establish a new connection" in err:
    #     return error_badge()
    # if err != 'API returned valid response\n':
    #     return failing_badge()
    # else:
    """

    :param url: The url the validator is testing
    :return: A badge determined by the test status
    """
    file_url = re.sub(r'[^\w]', '', url.encode('utf8'))
    log = cache.get(file_url)
    if log is None:
        badge = cache.get('unknown')
        if badge is None:
            badge = requests.get(unknown_badge())
            if badge.status_code == 200:
                cache.set('unknown', badge, timeout=BADGE_CACHE_TIMEOUT)
        return badge
    else:
        return _badge_from_output(log)


def _get_dredd_log(url):
    """
    This gets the Dredd validation output.
    This can be either a new Dredd validation run or an old one.
    :param url: The url to test
    :return: The Dredd validation output
    """
    file_url = re.sub(r'[^\w]', '', url.encode('utf8'))
    uwsgi.lock()
    log = run_dredd(SWAGGER, url)
    uwsgi.unlock()
    cache.set(file_url, log, timeout=LOG_CACHE_TIMEOUT)
    return log


def _badge_from_output(output):
    """
    Determines which badge should be returned based on validation output
    :param output: Output from validation
    :return: Badge based on validation output
    """
    if '0 errors' not in output:
        badge = cache.get('error')
        if badge is None:
            badge = requests.get(error_badge())
            if badge.status_code == 200:
                cache.set('error', badge, timeout=BADGE_CACHE_TIMEOUT)
        return badge
    if '0 failing' not in output:
        badge = cache.get('failing')
        if badge is None:
            badge = requests.get(failing_badge())
            if badge.status_code == 200:
                cache.set('failing', badge, timeout=BADGE_CACHE_TIMEOUT)
        return badge
    if str(EXPECTED_PASSING_TESTS) + ' passing' not in output:
        badge = cache.get('warning')
        if badge is None:
            badge = requests.get(warning_badge())
            if badge.status_code == 200:
                cache.set('warning', badge, timeout=BADGE_CACHE_TIMEOUT)
        return badge
    if '0 failing' in output and '0 errors' in output:
        badge = cache.get('passing')
        if badge is None:
            badge = requests.get(passing_badge())
            if badge.status_code == 200:
                cache.set('passing', badge, timeout=BADGE_CACHE_TIMEOUT)
        return badge


@app.route('/trs/validator', methods=['GET'])
def status_badge():
    """
    Endpoint that returns status badge
    :return: Status badge
    """
    url = request.args.get('url', '')
    badge_response = _compute_badge(url)
    return send_file(BytesIO(badge_response.content), mimetype=badge_response.headers['Content-Type'])


@app.route('/trs/validator/debug', methods=['GET'])
def debug():
    """
    Endpoint that returns the log file from validation
    :return:
    """
    url = request.args.get('url', '')
    r = _get_dredd_log(url)
    response = Response(r, mimetype="text/html")
    return response


def validate(url):
    # validate.validate('ga4gh-tool-discovery.yaml', 'annotations.yml', url, False, False, False)
    """
    Validates against the original validation code.  Currently not in use.
    :param url: The url to test validation against
    :return: The output
    """
    file_directory = os.path.dirname(__file__)
    swagger_file_path = os.path.join(file_directory, SWAGGER)
    command_args = [
        'ga4gh-tool-registry-validate',
        swagger_file_path,
        'annotations.yml',
        url + '/tools']
    process = Popen(command_args, stdout=PIPE, stderr=PIPE)
    return process.communicate()


def run_dredd(swagger_filename, url):
    """
    This runs Dredd against the url and given swagger yaml file
    :param swagger_filename: The swagger yaml to test against
    :param url: The url of the webservice to test
    :return: Output generated by Dredd
    """
    file_directory = os.path.dirname(__file__)
    swagger_file_path = os.path.join(file_directory, swagger_filename)
    hooks_file_path = os.path.join(file_directory, 'hooks.py')
    outfile = tempfile.NamedTemporaryFile('w')
    command_args = [
        'dredd',
        swagger_file_path,
        url,
        '-l',
        'error',
        '-a',
        'python',
        '-r',
        'html',
        '-o',
        outfile.name,
        '-f',
        hooks_file_path]
    process = Popen(command_args)
    process.wait()
    return _filename_to_string(outfile.name)


@app.after_request
def add_header(response):
    response.cache_control.max_age = 300
    return response


def _filename_to_string(filename):
    """
    The output was written to a temporary file because the output is too large for the buffer.
    This converts the file contents back to a string
    :param filename: The name of the file containing the Dredd output
    :return: String containing the file contents
    """
    with open(filename) as f:
        return f.read()


def _download_swagger_yaml():
    """
    Downloads the swagger yaml from ga4gh tool-registry-schemas
    TODO: Change the GitHub path once the TRSV changes are merged
    """
    file_directory = os.path.dirname(__file__)
    swagger_file_path = os.path.join(
        file_directory, "ga4gh-tool-discovery.yaml")
    urllib.urlretrieve(
        GITHUB_BASEURL + "/" + GITHUB_BRANCH + "/" + GITHUB_FILE_PATH,
        swagger_file_path)


_download_swagger_yaml()
createProcessedYAML.main()
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
