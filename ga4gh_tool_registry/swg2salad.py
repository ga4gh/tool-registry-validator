import sys
import json
import ruamel.yaml as yaml
import copy

def convert_p(p, rec, prop, annotations):
    r = {}
    if "$ref" in prop:
        tp = prop["$ref"][14:]
    else:
        tp = prop["type"]

    if tp == "array":
        tp = {"type": "array", "items": convert_p(None, prop, prop["items"], annotations)["type"]}

    if tp == "integer":
        tp = "int"

    if p is not None and p not in rec.get("required", []):
        tp = ["null", tp]

    r["type"] = tp
    r["doc"] = prop.get("description", "")

    if p in annotations:
        r["jsonldPredicate"] = copy.deepcopy(annotations[p])

    return r

def convert_swg(k, v, annotations):
    r = {}
    r["name"] = k
    r["type"] = "record"
    r["doc"] = v.get("description", "")
    r["fields"] = {p: convert_p(p, v, prop, annotations) for p,prop in v["properties"].iteritems()}
    if k in annotations["_documentRoot"]:
        r["documentRoot"] = True
    return r

def swg2salad(swg, annotations):
    return {"$namespaces": annotations.get("$namespaces", {}),
            "$graph": [convert_swg(k, v, annotations) for k,v in swg['definitions'].iteritems()]}

if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        with open(sys.argv[2]) as f2:
            annotations = yaml.load(f2)
        print yaml.dump(swg2salad(yaml.load(f), annotations), indent=4)
