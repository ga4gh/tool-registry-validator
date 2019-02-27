import os
import argparse
import sys
import ruamel.yaml as yaml
import logging
import json

from schema_salad.ref_resolver import Loader
from cwltool.load_tool import validate_document
from flask import Flask, Response, request, redirect

_logger = logging.getLogger("cwltool")

defaultStreamHandler = logging.StreamHandler()
_logger.addHandler(defaultStreamHandler)
_logger.setLevel(logging.DEBUG)

app = Flask(__name__)

tools = {}
tooldirs = {}


@app.route("/api/ga4gh/v1/tools", methods=['GET'])
def gettools():
    return json.dumps(tools.values(), indent=4), 200, ''


@app.route("/api/ga4gh/v1/tools/<toolid>", methods=['GET'])
def gettool_id(toolid):
    return json.dumps(tools[toolid], indent=4), 200, ''


@app.route("/api/ga4gh/v1/tools/<toolid>/versions", methods=['GET'])
def gettool_id_versions(toolid):
    return json.dumps(tools[toolid]["versions"], indent=4), 200, ''


@app.route(
    "/api/ga4gh/v1/tools/<toolid>/versions/<int:version_id>",
    methods=['GET'])
def gettool_id_versionid(toolid, version_id):
    return json.dumps(tools[toolid]["versions"][version_id], indent=4), 200, ''


@app.route(
    "/api/ga4gh/v1/tools/<toolid>/versions/<int:version_id>/<type>/descriptor",
    methods=['GET'])
def gettool_id_version_descriptor(toolid, version_id, type):
    return json.dumps(tools[toolid]["versions"][version_id]
                      ["descriptor"], indent=4), 200, ''


@app.route(
    "/api/ga4gh/v1/tools/<toolid>/versions/<int:version_id>/<type>/<other>",
    methods=['GET'])
def gettool_id_version_descriptor_other(toolid, version_id, type, other):
    dir = tooldirs["/api/ga4gh/v1/tools/%s/versions/%s" % (toolid, version_id)]
    f = open(os.path.join(dir, other))
    return f.read(), 200, ''


@app.route(
    "/api/ga4gh/v1/tools/<toolid>/versions/<int:version_id>/dockerfile",
    methods=['GET'])
def gettool_id_version_dockerfile(toolid, version_id):
    return json.dumps(tools[toolid]["versions"][version_id]
                      ["dockerfile"], indent=4), 200, ''


@app.route("/api/ga4gh/v1/metadata", methods=['GET'])
def get_metadata():
    return json.dumps({}, indent=4), 200, ''


@app.route("/api/ga4gh/v1/tool-classes", methods=['GET'])
def get_classes():
    return json.dumps({}, indent=4), 200, ''


if __name__ == "__main__":
    app.debug = True

    parser = argparse.ArgumentParser()
    parser.add_argument("dir")
    args = parser.parse_args()

    for dirpath, dirnames, filenames in os.walk(args.dir):
        for f in filenames:
            if f.endswith(".cwl"):
                path = os.path.realpath(os.path.join(args.dir, dirpath, f))
                try:
                    with open(path) as f2:
                        content = f2.read()
                        cwl = yaml.load(content)
                    document_loader = Loader(
                        {"cwl": "https://w3id.org/cwl/cwl#", "id": "@id"})
                    document_loader, avsc_names, processobj, metadata, uri = validate_document(
                        document_loader, cwl, "file://" + path, strict=False)

                    tools[f] = {
                        "url": "/api/ga4gh/v1/tools/%s" %
                        f,
                        "id": f,
                        "organization": "",
                        "author": "",
                        "meta-version": "",
                        "toolclass": {
                            "id": cwl["class"],
                        },
                        "versions": [
                            {
                                "url": "/api/ga4gh/v1/tools/%s/versions/0" %
                                f,
                                "descriptor": {
                                    "url": "/api/ga4gh/v1/tools/%s/versions/0/CWL/%s" %
                                    (f,
                                     f),
                                    "type": "CWL",
                                    "descriptor": content},
                                "id": "0",
                                "meta-version": ""}]}
                    tooldirs["/api/ga4gh/v1/tools/%s/versions/0" %
                             f] = os.path.realpath(os.path.join(args.dir, dirpath))
                except Exception as e:
                    sys.stderr.write("\nError reading %s: %s\n" % (path, e))
                except KeyboardInterrupt:
                    sys.stderr.write("\nInterrupted reading %s\n" % (path))
                    raise
                else:
                    sys.stderr.write("\nReading %s ok\n" % (path,))

    app.run()
