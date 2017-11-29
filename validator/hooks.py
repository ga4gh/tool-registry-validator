from dredd_hooks import before_each, before_each_validation, after, before
from flask import json
import ast
import urllib
response_stash = {}
id = "registry.hub.docker.com%2Fsequenza%2Fsequenza"
api_uri = "XXX"
DEFAULT_TYPE = 'type_placeholder'
DEFAULT_RELATIVE_PATH = 'relative_path_placeholder'
DEFAULT_VERSION_ID = 'version_id_placeholder'
DEFAULT_ID = 'id_placeholder'

NEW_TYPE = None
NEW_RELATIVE_PATH = None
NEW_VERSION_ID = None
NEW_ID = None


@before_each
def add_path_parameter_values(transaction):
    """
    Dredd needs sample path parameter to test against, this injects it before testing
    :param transaction: Dredd transaction object
    """
    global NEW_ID
    global NEW_VERSION_ID
    global NEW_TYPE
    global NEW_RELATIVE_PATH
    if _defined_parameters():
        transaction['fullPath'] = transaction['fullPath'].replace(DEFAULT_VERSION_ID, NEW_VERSION_ID)
        transaction['fullPath'] = transaction['fullPath'].replace(DEFAULT_TYPE, NEW_TYPE)
        transaction['fullPath'] = transaction['fullPath'].replace(DEFAULT_RELATIVE_PATH, '%2Fsequenza.cwl')
        transaction['fullPath'] = transaction['fullPath'].replace(DEFAULT_ID, NEW_ID)


@before_each_validation
def relax_headers(transaction):
    """
    Dredd only compares headers that are identical to what's expected.
    It will fail if it's slightly different.
    This takes over validation
    :param transaction:
    :return:
    """
    try:
        real_content_type = transaction['real']['headers']['content-type']
        expected_content_type = transaction['expected']['headers']['Content-Type']
        if expected_content_type in real_content_type:
            transaction['expected']['headers']['Content-Type'] = real_content_type
    except KeyError:
        return


@before('GA4GH > /api/ga4gh/v1/tools/{id}/versions/{version_id}/descriptor/{relative_path} > Get additional tool '
        'descriptor files (CWL/WDL) relative to the main file > 200 > application/json')
def ignore_relative_path(transaction):
    """
    Skipping this endpoint because it's really difficult to get an example relative_path to test against
    :param transaction: Dredd transaction object
    """
    transaction['skip'] = True


@after('GA4GH > /api/ga4gh/v1/tools > List all tools > 200 > application/json')
def add_value(transaction):
    """
    This determines what sample path parameters Dredd should test against for all other endpoints
    :param transaction: The Dredd transaction object
    :return:
    """
    try:
        string = (json.dumps(transaction['real']['body']))
        d = ast.literal_eval(string)
        jdata = json.loads(d)
        for tool in jdata:
            if _defined_parameters():
                break
            tool_id = tool['id']
            if tool_id is not None:
                _check_version(tool['versions'], tool_id)
    except KeyError:
        return


def _defined_parameters():
    """
    Checks whether or not there are sample path parameters to test against
    :return:
    """
    global NEW_ID
    global NEW_VERSION_ID
    global NEW_TYPE
    if NEW_ID is not None and NEW_VERSION_ID is not None and NEW_TYPE is not None:
        return True
    else:
        return False


def _check_version(versions, tool_id):
    """
    Parses the sample version(s) to retrieve sample path parameters to test against
    :param versions:
    :param tool_id:
    """
    for version in versions:
        if version['descriptor_type'] is not None and version['name'] is not None:
            global NEW_ID
            global NEW_VERSION_ID
            global NEW_TYPE
            global NEW_RELATIVE_PATH
            print tool_id
            NEW_ID = urllib.quote_plus(tool_id)
            NEW_VERSION_ID = urllib.quote_plus(version['name'])
            NEW_TYPE = urllib.quote_plus(version['descriptor_type'][0])
            if _defined_parameters():
                break

