# motion-temperature

A simple Python script which subscribes to two separate MQTT topics and updates Motion video overlay texts when a message is received. This is written for a setup with four cameras, three of which are pointing outside of the house and one is in garage. If you have different amount of temperature data sources, you can easily either add more mqtt client instances or comment out the other one if you only need one.

## Requirements
- Python 3 installed
- python3-urllib3
- python3-paho-mqtt

## How to set up

This is supposed to be set up in your motionEye host. There are few things you should configure before doing rest of the steps.

* The mqtt broker address
* Camera configuration file paths according to your setup
* The mqtt topics where temperature values are posted (my setup posts just the temperature values as floats)
* Change ```on_outdoortemp_message``` and ```on_garagetemp_message``` to update the correct cameras

Then you can install the script.

Create directory 

```shell
sudo mkdir /opt/motion-temperature
```

Copy script

```shell
sudo cp motion-temperature.py /opt/motion-temperature
```

Set permissions

```shell
sudo chmod -R 755 /opt/motion-temperature
```

Copy systemd script

```shell
sudo cp motion-temperature.service /etc/systemd/system/
```

Enable service

```shell
sudo systemctl enable motion-temperature.service
```

Start

```shell
sudo systemctl start motion-temperature
```
