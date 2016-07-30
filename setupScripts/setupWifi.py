import argparse

parser = argparse.ArgumentParser(description='Setup wifi by providing username and password')
parser.add_argument('username', help='Username for wifi')
parser.add_argument('password', help='Password for wifi')
args = parser.parse_args()

# Create WPA Supplicant
longString = '''ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=GB

network={
       ssid="GV-Student"
       key_mgmt=WPA-EAP
       eap=PEAP
       identity="'''+args.username+'''"
       password="'''+args.password+'''"
       phase2="auth=MSCHAPV2"
}
'''
with open('/etc/wpa_supplicant/wpa_supplicant.conf','w') as afile:
       afile.write(longString)
