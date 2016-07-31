# Run apt-get to get the dependencies required by the project
apt-get update
apt-get install -y python3-rpi.gpio python3-smbus i2c-tools libi2c-dev build-essential python-dev git scons swig nodejs npm apache2 mysql-server php5 php5-mysql libapache2-mod-php5
npm install -g npm
npm install -g pm2
npm install -g n
n stable

