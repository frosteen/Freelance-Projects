# Add line on crontab -e
# @reboot sh /home/pi/Raspistill_TCP_Stream.sh &

echo 0 | sudo tee /sys/class/leds/led0/brightness > /dev/null

while true;
do
	echo 1 | sudo tee /sys/class/leds/led0/brightness > /dev/null
	
	raspivid -t 0 -w 1280 -h 720 -vf -hf -fps 30 -l -o tcp://0.0.0.0:5000;
	
	echo 0 | sudo tee /sys/class/leds/led0/brightness > /dev/null
done
