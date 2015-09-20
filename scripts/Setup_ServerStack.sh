#!/bin/bash
#
# Setup Script to install necessary utils for running IWBT
# ------------------------------------------------------------------
#
# After running this script, you should be able to use the IWBT
# stack with no real issues. This includes interacting with back-end
# stuff and serving the website / phone apps.


# -------------------------------------------------------------------
# Settings
# -------------------------------------------------------------------
# These are user editable variables that change the way the installer
# operates


# USER SETTING: Install Type
# 1. Set this value to 'local' if installing on an already existing
#    Machine. This should be standard if you are installing on a
#    desktop.
# 2. Set this value to 'full' if installing on a virtual box or 
#    a raspberry pi
install_type='local'

# SSH SETTINGS: SSH Setup
# If you are doing a full install, you'll need to configure SSH on
# the remote machine. If you're doing a local install, set SSH_CONF
# to 0
SSH_CONF=1
SSH_RSA=1

# Variables
# -------------------------------------------------------------------
app_name="iwbt_install"
app_repo="https://github.com/exleym/IWBT.git"
virtual_env="/opt/venv1"

# Define user variables
# -------------------------------------------------------------------
HOSTNAME="iwbt"
SSHPORT="22"
USER="exley"
PUSER="app_admin"
PPWD="app_admin"

apt-get update

# Create Python Virtualenv
# ---------------------------------------------------------------
apt-get install -y --force-yes python-virtualenv
virtualenv $virtual_env

# Install some python packages
# -------------------------------------------------------------------
apt-get install -y --force-yes libpq-dev python-dev
source "$virtual_env"/bin/activate
pip install MySQL-python
pip install django
pip install gunicorn
pip install psycopg2
pip install jsonfield

# Clone Git
cd "$virtual_env"
git clone $app_repo
deactivate


# Optional Section to Configure a Machine via Full Install
# SHOULD ONLY BE PERFORMED ON A VIRTUAL MACHINE OR RASPBERRY PI
if [ "$install_type" == "full" ]
then
    # Setup User and Host
    # ---------------------------------------------------------------
    echo "$HOSTNAME" > /etc/hostname
    useradd "$USER"
    passwd "$USER"

    # Install some packages
    # ---------------------------------------------------------------
    apt-get install -y --force-yes curl git
    apt-get install -y --force-yes postgresql postgresql-contrib
    apt-get install -y --force-yes nginx
    apt-get install -y --force-yes python-dev libmysqlclient-dev

    # Configure SSH Server
    # ---------------------------------------------------------------
    # Only do this if SSH_CONF is True
    if [ "$SSH_CONF" == '1' ]
    then
        mkdir -p ~/.ssh
        cp /etc/ssh/sshd_config /etc/ssh/ssh_config.bak
        cat $app_repo/IWBT/data/id_rsa.sharkbox.pub >> ~/.ssh/authorized_keys
        if [ "$SSH_RSA" == '1' ]
        then
            sed -i -e s/"#PasswordAuthentication.*"/'PaswordAuthentication no'/g /etc/ssh/sshd_config
	fi
    fi
fi

# Configure Postgresql Server
# -------------------------------------------------------------------
# switch user to "postgres" to allow superuser access while configuring
# postgres; create a superuser; create a database;
su - postgres
createdb "$DBNAME"
createuser -U "$PGUSER"
su -c "psql -d $DBNAME -c \"GRANT ALL PRIVILEGES ON DATABASE $DBNAME TO $PGUSER\""
echo "*:*:*:$PGUSER:$PGPASS" > ~/.pgpass
/etc/init.d/postgresql restart
