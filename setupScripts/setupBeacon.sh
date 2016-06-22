# From http://yencarnacion.github.io/eddystone-url-calculator/
# Encodes the web address of the project as an eddystone beacon
sudo hciconfig hci0 up
sudo hciconfig hci0 leadv 3
sudo hcitool -i hci0 cmd 0x08 0x0008 1c 02 01 06 03 03 aa fe 14 16 aa fe 10 00 02 65 67 72 2e 67 76 73 75 02 7e 65 73 6d 2f 00 00 00
