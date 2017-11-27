### Running the Validator

To run the validator on a server, you need 2 files
1.  build.sh script
2.  The Dockerfile in this repository

Then run the build.sh script.  This will do several things:
1. Download the ga4gh-tool-discovery.yaml if it has changed on GitHub
2. Build a new Docker container with this new ga4gh-tool-discovery
3. Run the newly built Docker container