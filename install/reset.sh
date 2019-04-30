/usr/local/bin/k3s-uninstall.sh
docker kill $(docker ps -q)
docker rm $(docker ps -a -q)
docker rmi $(docker images -q)
rm -rf /srv/p2/
rm -rf /var/lib/docker
apt remove --purge docker* -y && apt autoremove --purge -y
