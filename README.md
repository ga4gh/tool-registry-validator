# GA4GH Tool Registry API schema validator

Installation:

```
$ python setup.py install
```

Running the validator:

```
$ ga4gh-tool-registry-validate ../tool-registry-schemas/src/main/resources/swagger/ga4gh-tool-discovery.yaml annotations.yml https://www.dockstore.org:8443/api/v1/tools
```

Convert the tool registry response to RDF:

```
$ ga4gh-tool-registry-validate --print-rdf ../tool-registry-schemas/src/main/resources/swagger/ga4gh-tool-discovery.yaml annotations.yml https://www.dockstore.org:8443/api/v1/tools > tools.ttl
```
