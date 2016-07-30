virtualenv -p python3 --system-site-packages myenv
. myenv/bin/activate
pip install -r requirements.txt
git clone https://github.com/jgarff/rpi_ws281x.git
cd rpi_ws281x
scons
cd python
python setup.py install
cd ../..

pm2 start esm.py --interpreter=myenv/bin/python
