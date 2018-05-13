# TygerCaddy
[![Docker Pulls](https://img.shields.io/docker/pulls/portainer/portainer.svg)](https://hub.docker.com/r/morph1904/tygercaddy/)
[![Microbadger](https://images.microbadger.com/badges/image/morph1904/tygercaddy.svg)](http://microbadger.com/images/morph1904/tygercaddy "Image size")

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
sudo . tyger-install-ubuntu.sh
```

When the script has installed the perquisites it will prompt you for a username, password and email address. Enter these in and then reboot your machine.

```
sudo reboot -now
```
Once the server has rebooted, enter the server ip address in your browser and login with the supplied username and password.

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
sudo . tyger-update-ubuntu.sh
```

Once complete, enter the server ip address in your browser and log on as normal.

## Built With

* [Django 2](https://docs.djangoproject.com/en/2.0/) - Django 2 Python Web Framework
* [CaddyServer](https://caddyserver.com/) - HTTP Reverse Proxy Server

## Authors

* **Morph1904** - *Initial work* - [Morph1904](https://github.com/morph1904)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
