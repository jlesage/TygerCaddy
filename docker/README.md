TygerCaddy Docker Container
===========================

This container aims to be easy to understand, easy to backup/restore, and easy to operate.

Any suggestions on improving this containers ease of use are welcome.

Building TygerCaddy as a developer
----------------------------------

First we need to clean any existing images:

    docker image rm $(docker images -aq)

Then build and tag the containers:

    docker build --build-arg BUILD_DATE=`date -u +"%Y-%m-%dT%H:%M:%SZ"` \
                 --build-arg VCS_REF=`git rev-parse --short HEAD` \
                 --build-arg VERSION=`cat VERSION.txt` \
                 -t morph1904/tygercaddy:latest \
                 -f docker/Dockerfile .

Push the containers:

    docker push morph1904/tygercaddy:latest

Poll the stats counter to update:

    curl -X POST https://hooks.microbadger.com/images/morph1904/tygercaddy/H1IJ26NFLGCXubTEOCkGpWDam9Q\=
