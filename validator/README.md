### Running the Validator

To run the validator on a server, you only need 2 files
1.  build.sh script
2.  The Dockerfile in this repository

Then run the build.sh script.  This will do several things:
1. Build a new Docker container that currently uses this repository (currently feature/flask, need to change later)
2. Run the newly built Docker container