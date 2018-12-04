*this script use in Server.

How to use.
1. Install library pySerial by open command prompt and input command "python -m pip install pyserial".
2. Install library Adafruit-DHT by open command prompt and input command "$ sudo apt-get update" and "$ git clone https://github.com/adafruit/Adafruit_Python_DHT.git".
3. Create folder client in raspberry pi.
4. Copy each files to /client/... in Raspberry pi.
5. Set auto run script after reboot or start raspberry pi.
   5.1 Open prompt and input command "$ sudo nano /etc/profile"
   5.2 Followed by sudo python3 /home/pi/client/client.py &
		   sudo python3 /home/pi/client/server_config.py &
    		   sudo python3 /home/pi/client/server_config_30003.py &
	in the last line.
   5.3 Reboot raspberry pi by command "$ sudo reboot".
6. Start raspberry pi after Run server. 
