#!/bin/bash

echo "[*] Log in here: http://127.0.0.1:8080/?mongo=127.0.0.1&username="
echo "[*] For diagnostic purposes visit: http://127.0.0.1:28017/"
php -S 127.0.0.1:8080 /var/www/adminer/index.php >/dev/null
