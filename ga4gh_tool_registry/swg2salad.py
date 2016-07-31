import sys
import json
import ruamel.yaml as yaml
import copy

def convert_p(p, rec, prop, overrides):
    r = {}
    if "$ref" in prop:
        tp = prop["$ref"][14:]
    else:
        tp = prop["type"]

    if tp == "array":
        tp = {"type": "array", "items": convert_p(None, prop, prop["items"], overrides)["type"]}

    if tp == "integer":
        tp = "int"

    if p is not None and p not in rec.get("required", []):
        tp = ["null", tp]

    r["type"] = tp
    r["doc"] = prop.get("description", "")

    if p in overrides:
        r["jsonldPredicate"] = copy.deepcopy(overrides[p])

    return r

def convert_swg(k, v, overrides):
    r = {}
    r["name"] = k
    r["type"] = "record"
    r["doc"] = v.get("description", "")
    r["fields"] = {p: convert_p(p, v, prop, overrides) for p,prop in v["properties"].iteritems()}
    if k in overrides["_documentRoot"]:
        r["documentRoot"] = True
    return r

def swg2salad(swg, overrides):
    return {"$namespaces": overrides.get("$namespaces", {}),
            "$graph": [convert_swg(k, v, overrides) for k,v in swg['definitions'].iteritems()]}

if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        with open(sys.argv[2]) as f2:
            overrides = yaml.load(f2)
        print yaml.dump(swg2salad(yaml.load(f), overrides), indent=4)
