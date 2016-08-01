import argparse
import sys
import os
import urlparse
import subprocess
import tempfile

from . import swg2salad
import ruamel.yaml as yaml
import requests
from schema_salad.schema import load_schema, validate_doc
from schema_salad import jsonld_context
from schema_salad.main import printrdf
from schema_salad.ref_resolver import Loader

from cwltool.load_tool import validate_document

from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import Namespace

def dockstore_fixup(r):
    if isinstance(r, list):
        for d in r:
            dockstore_fixup(d)
    elif isinstance(r, dict):
        if 'id' in r and r['id'] is None:
            r['id'] = ''

        if 'author' in r and r['author'] is None:
            r['author'] = ''

        if 'descriptor' in r and r['descriptor'] is None:
            if 'dockerfile' in r:
                r['descriptor'] = {"descriptor": "", "type": ""}
            else:
                r['descriptor'] = ''

        if 'tooltype' in r:
            r["toolclass"] = r['tooltype']
            del r['tooltype']

        for d in r.values():
            dockstore_fixup(d)

def expand_cwl(cwl, uri, g):
    try:
        document_loader = Loader({"cwl": "https://w3id.org/cwl/cwl#", "id": "@id"})
        cwl = yaml.load(cwl)
        document_loader, avsc_names, processobj, metadata, uri = validate_document(
            document_loader, cwl, uri, strict=False)
        jsonld_context.makerdf(uri, processobj, document_loader.ctx, graph=g)
        sys.stderr.write("\n%s: imported ok\n" % (uri))
    except Exception as e:
        sys.stderr.write("\n%s: %s\n" % (uri, e))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("swagger")
    parser.add_argument("annotations")
    parser.add_argument("url")

    parser.add_argument("--dockstore-fixup", action="store_true", default=False)
    parser.add_argument("--print-rdf", action="store_true", default=False)
    parser.add_argument("--serve", action="store_true", default=False)
    parser.add_argument("--fuseki-path", type=str, default=".")

    args = parser.parse_args()

    with open(args.annotations) as f2:
        annotations = yaml.load(f2)

    with open(args.swagger) as f:
        sld = swg2salad.swg2salad(yaml.load(f), annotations)

    sld["$base"] = "http://ga4gh.org/schemas/tool-registry-schemas"
    sld["name"] = "file://" + os.path.realpath(args.swagger)

    document_loader, avsc_names, schema_metadata, metaschema_loader = load_schema(sld)

    txt = document_loader.fetch_text(urlparse.urljoin("file://" + os.getcwd()+"/", args.url))
    r = yaml.load(txt)

    if args.dockstore_fixup:
        dockstore_fixup(r)

    validate_doc(avsc_names, r, document_loader, True)

    sys.stderr.write("API returned valid response\n")

    toolreg = Namespace("http://ga4gh.org/schemas/tool-registry-schemas#")
    td =      Namespace("http://ga4gh.org/schemas/tool-registry-schemas#ToolDescriptor/")

    if args.print_rdf or args.serve:
        g = jsonld_context.makerdf(args.url, r, document_loader.ctx)
        for s, _, o in g.triples((None, td["type"], Literal("CWL"))):
            for _, _, d in g.triples((s, toolreg["descriptor"], None)):
                expand_cwl(d, unicode(s), g)

    if args.print_rdf:
        print(g.serialize(format="turtle"))

    if args.serve:
        t = tempfile.NamedTemporaryFile(suffix=".ttl")
        g.serialize(t, format="turtle")
        t.flush()
        subprocess.check_call(["./fuseki-server", "--file="+t.name, "/tools"], cwd=args.fuseki_path)
