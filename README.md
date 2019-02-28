# GA4GH Tool Registry API schema validator

## Installation:

```
$ python setup.py install
```

## Validate tool registry response:

```
$ ga4gh-tool-registry-validate ../tool-registry-schemas/src/main/resources/swagger/ga4gh-tool-discovery.yaml annotations.yml https://www.dockstore.org:8443/api/ga4gh/v1/tools
```

## Convert a tool registry response to RDF:

```
$ ga4gh-tool-registry-validate --print-rdf ../tool-registry-schemas/src/main/resources/swagger/ga4gh-tool-discovery.yaml annotations.yml https://www.dockstore.org:8443/api/ga4gh/v1/tools > tools.ttl
```

## Index a tool registry for SPARQL query

Requires Apache Fuseki: https://jena.apache.org/documentation/fuseki2/#download-fuseki

```
$ ga4gh-tool-registry-validate --serve --fuseki-path=../apache-jena-fuseki-2.3.0 ../tool-registry-schemas/src/main/resources/swagger/ga4gh-tool-discovery.yaml annotations.yml https://www.dockstore.org:8443/api/ga4gh/v1/tools
```

## Running the Validator

To see the validator results for the currently known TRSs, go to https://ga4gh.github.io/tool-registry-service-schemas/Validator/
The badge for each TRS  will be unknown unless it's been manually ran in the past day.  Click on the TRS badge to manually trigger validator for that TRS (it will take a minute).

It's recommended to use the validator that's currently set up.  To test your own TRS, just replace the url query parameter at this endpoint: http://142.1.177.188:8080/trs/validator/debug?url=https://staging.dockstore.org:8443

To run the validator on your own server, you only need 2 files
1.  [build.sh](../build.sh) script
2.  The [Dockerfile](../Dockerfile) in this repository

Then run the build.sh script.  This will do several things:
1. Build a new Docker image that currently uses this repository's develop branch (need to change if testing other branches on this repo)
2. Run the newly built Docker container

~                                                                                                   
