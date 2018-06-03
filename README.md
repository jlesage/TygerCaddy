# TygerCaddy
[![Docker Pulls](https://img.shields.io/docker/pulls/morph1904/tygercaddy.svg)](https://hub.docker.com/r/morph1904/tygercaddy/)
[![](https://images.microbadger.com/badges/image/morph1904/tygercaddy.svg)](https://microbadger.com/images/morph1904/tygercaddy)
[![](https://images.microbadger.com/badges/version/morph1904/tygercaddy.svg)](https://microbadger.com/images/morph1904/tygercaddy)
[![](https://images.microbadger.com/badges/commit/morph1904/tygercaddy.svg)](https://microbadger.com/images/morph1904/tygercaddy)

Caddy based reverse proxy app with web GUI
![alt text](https://github.com/morph1904/TygerCaddy/raw/master/TygerCaddy/assets/img/screenshot.png)

This project is still under heavy development. It should be suitable for every day use but expect bugs and sweeping changes.

__*Although this app uses Caddy, we are not affiliated with or endorsed by the Caddy team.*__

## Docker

### Running TygerCaddy
```
docker run -d -p 80:80 -p 443:443 -p 9090:9090 --name tygercaddy \
  -v $PWD/data/config:/apps/TygerCaddy/TygerCaddy/data \
  -v $PWD/data/certs:/root/.caddy \
  morph1904/tygercaddy
```
Then point your browser to http://127.0.0.1/ and login with the provided credentials

### Building TygerCaddy
```
cd /tmp
git clone https://github.com/morph1904/TygerCaddy.git
cd TygerCaddy
docker build -t morph1904/tygercaddy docker/.
```
## Ubuntu install

### Install Instructions (Ubuntu 16.04 +)
```
cd /tmp
wget https://raw.githubusercontent.com/morph1904/TygerCaddy/master/tyger-install-ubuntu.sh
chmod +x tyger-install-ubuntu.sh
./tyger-install-ubuntu.sh
```
Once the script completes, enter the server IP address in your browser. You will be prompted to setup your server.

### Update Instructions (Ubuntu 16.04 +)
```
cd /tmp
wget https://raw.githubusercontent.com/morph1904/TygerCaddy/master/tyger-update-ubuntu.sh
chmod +x tyger-update-ubuntu.sh
./tyger-update-ubuntu.sh
```
Once complete, enter the server IP address in your browser and log in as normal.

### Uninstall Instructions (Ubuntu 16.04 +)
```
cd /tmp
wget https://raw.githubusercontent.com/morph1904/TygerCaddy/master/tyger-uninstall-ubuntu.sh
chmod +x tyger-uninstall-ubuntu.sh
./tyger-uninstall-ubuntu.sh
```

## Built With
* [Django 2](https://docs.djangoproject.com/en/2.0/) - Django 2 Python Web Framework
* [CaddyServer](https://caddyserver.com/) - HTTP Reverse Proxy Server

## Authors
* **Morph1904** - *Project Lead/Creator* - [Morph1904](https://github.com/morph1904)
* **sparky8251** - *Docker Builds/Testing* - [sparky8251](https://github.com/sparky8251)
* **arevindh** - *UI Improvements/Testing* - [arevindh](https://github.com/arevindh)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
