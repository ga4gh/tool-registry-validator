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

To run the validator on a server, you only need 2 files
1.  [build.sh](../build.sh) script
2.  The [Dockerfile](../Dockerfile) in this repository

Then run the build.sh script.  This will do several things:
1. Build a new Docker container that currently uses this repository (currently feature/flask, need to change later)
2. Run the newly built Docker container

Currently, the validator is running at this temporary location: https://garyluu.github.io/TRSV/
~                                                                                                   
