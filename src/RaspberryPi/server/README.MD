## Contents

* The configuration file for an nginx reverse proxy to a nodejs server.
* The nodejs server entry point. Listens to POST and GET requests.
* Node modules directory ()

## Done so far

* Installed nginx, nodejs, npm, pm2(npm), and Express(npm)
* Created configuration for nginx in /etc/nginx/sites-available/typeswipe-server
* Symlinked /etc/nginx/sites-enabled to /etc/nginx/sites-available/typeswipe-server
* Configured pm2 to launch server after bootup
* Wrote simple server using Express to listen to POST and GET

