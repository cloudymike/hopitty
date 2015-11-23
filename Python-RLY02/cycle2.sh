#! /bin/bash
RELAY=1
for i in {1..50}; do
echo -n "cycle $i relay $RELAY on.."
sudo python rly02.py -r $RELAY -a on
sleep 5
echo "off"
sudo python rly02.py -r $RELAY -a off
sleep 5
done
