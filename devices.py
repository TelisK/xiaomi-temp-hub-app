# Use every device's mac address which you can find with two ways.
# 1st way
# Through the app Xiaomi home, you have to connect to the device, scroll down to find traditional style. 
# When you are connected to traditional style, you press on 3 dots (top right) and About. In there you can find the mac address of every device

# 2nd way
# You have to run on Linux the following commands:
# sudo systemctl enable bluetooth
# sudo systemctl start bluetooth
# bluetoothctl
# scan on

# This will scan all the bluetooth devices nearby, and the results you need are at the form: 'AA:BB:CC:DD:EE:FF LYWSD03MMC'
# On these results you can find your device's mac address.

kids_bedroom = 'XX:XX:XX:XX:XX:XX'
parents_bedroom = 'XX:XX:XX:XX:XX:XX'
living_room = 'XX:XX:XX:XX:XX:XX'
airbnb = 'XX:XX:XX:XX:XX:XX'