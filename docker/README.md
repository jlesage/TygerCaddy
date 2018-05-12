TygerCaddy Docker Container
=========================

_*This container is in development and not recommended for normal use!*_

This container aims to be easy to understand, easy to backup/restore, and easy to operate.

Any suggestions on improving this containers ease of use are welcome.

Running TygerCaddy
-----------------

    docker run -d -p 80:80 -p 443:443 --name tygercaddy \
        -e username=admin \
        -e password=secret \
        -e email=admin@example.com \
        tygercaddy/tygercaddy:testing

Then point your browser to http://127.0.0.1/ and login with the provided credentials

Building TygerCaddy
-----------------

First clone the repo and cd to it

    docker build -t tygercaddy/tygercaddy:testing docker/.
