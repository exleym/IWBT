#!/bin/bash
#
# Setup Script to install necessary utils for running IWBT
# ------------------------------------------------------------------
#
# After running this script, you should be able to use the IWBT
# stack with no real issues. This includes interacting with back-end
# stuff and serving the website / phone apps.

# Variables
# -------------------------------------------------------------------
app_name="iwbt_install"
app_repo="https://github.com/exleym/IWBT.git"

# Define user variables
# -------------------------------------------------------------------
HOSTNAME="iwbt"
SSHPORT="22"
USER="exley"

# Install some packages
# -------------------------------------------------------------------
apt-get update
apt-get install -y --force-yes curl mysql-server git

# Configure SSH Server
# -------------------------------------------------------------------
sudo cp /etc/ssh/sshd_config /etc/ssh/ssh_config.bak
sed -i -e s/"#PasswordAuthentication.*"/'PaswordAuthentication no'/g /etc/ssh/sshd_config

