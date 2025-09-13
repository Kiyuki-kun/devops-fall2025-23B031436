#!/usr/bin/env bash
set -e
apt-get update
DEBIAN_FRONTEND=noninteractive apt-get install -y python3 python3-venv python3-pip postgresql postgresql-contrib libpq-dev
# create postgres user db for demo
sudo -u postgres psql -c "CREATE USER vagrant WITH PASSWORD 'password';" || true
sudo -u postgres psql -c "CREATE DATABASE simpleauth OWNER vagrant;" || true
# run init SQL
psql -U vagrant -d simpleauth -f /vagrant/migrations/init.sql || true

# create virtualenv and install requirements
python3 -m venv /home/vagrant/simpleauth-venv
source /home/vagrant/simpleauth-venv/bin/activate
pip install --upgrade pip
pip install -r /vagrant/requirements.txt

# create systemd service file (the repo includes a unit file; copy it into place)
cp /vagrant/systemd/simpleauth.service /etc/systemd/system/simpleauth.service
systemctl daemon-reload
systemctl enable --now simpleauth.service || true