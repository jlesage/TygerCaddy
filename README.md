# TygerCaddy
[![Docker Pulls](https://img.shields.io/docker/pulls/morph1904/tygercaddy.svg)](https://hub.docker.com/r/morph1904/tygercaddy/)
[![](https://images.microbadger.com/badges/image/morph1904/tygercaddy.svg)](https://microbadger.com/images/morph1904/tygercaddy)
[![](https://images.microbadger.com/badges/version/morph1904/tygercaddy.svg)](https://microbadger.com/images/morph1904/tygercaddy)
[![](https://images.microbadger.com/badges/commit/morph1904/tygercaddy.svg)](https://microbadger.com/images/morph1904/tygercaddy)

Caddy based reverse proxy app with web GUI
![alt text](https://github.com/morph1904/TygerCaddy/raw/master/TygerCaddy/assets/img/screenshot.png)

# INFO!
Please be aware this is still in BETA and not suitable for a production environment.
Although this app uses Caddy, we are not affiliated with or endorsed by the Caddy team.

## Install Instructions (Ubuntu 16.04 +)
Currently only ubuntu is supported by the install script

SSH on to your server.

```
cd /tmp
```
Get the Ubuntu Installer

```
wget https://raw.githubusercontent.com/morph1904/TygerCaddy/master/tyger-install-ubuntu.sh
```
Now run it with sudo privileges

```
chmod +x tyger-install-ubuntu.sh
./tyger-install-ubuntu.sh
```
Once the script completes, enter the server IP address in your browser. You will be prompted to setup your server

## Update

SSH on to your server.

```
cd /tmp
```
Get the Ubuntu Updater

```
wget https://raw.githubusercontent.com/morph1904/TygerCaddy/master/tyger-update-ubuntu.sh
```
Now run it with sudo privileges

```
chmod +x tyger-update-ubuntu.sh
./tyger-update-ubuntu.sh
```
Once complete, enter the server IP address in your browser and log in as normal.

## Install Instructions (Docker)
[View Docker README](docker/README.md)

## Built With
* [Django 2](https://docs.djangoproject.com/en/2.0/) - Django 2 Python Web Framework
* [CaddyServer](https://caddyserver.com/) - HTTP Reverse Proxy Server

## Authors
* **Morph1904** - *Project Lead/Creator* - [Morph1904](https://github.com/morph1904)
* **sparky8251** - *Docker Builds/Testing* - [sparky8251](https://github.com/sparky8251)
* **arevindh** - *UI Improvements/Testing* - [arevindh](https://github.com/arevindh)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
