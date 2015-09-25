# Greenhouse Demo Scenario

>This document is in DRAFT version, something can be missing or wrong. If you intend to re-create this scenario, you are smart enough to go through without a real step-by-step guide. Anyway, if you find errors, missing steps or typos  as well as if you need some help to implement the scenario, feel free to contact me. I really appreciate your help and your feedbacks.

>This scenario doesn't want to represent the best way to do things using SAP HCP, but it's a first attempt to make things work. Code can be improved in readability, efficiency and design.

This is the repository for a real and complete end-to-end scenario (**Greenhouse**) built using the SAP Hana Cloud Platform IoT Services ([SAP HCP IoT](http://hcp.sap.com/)) and a [RaspberryPi](https://www.raspberrypi.org/) as a gateway.

The document and the code snippets  will provide information on how to quick re-use it, replicate what I built, improve it and extend it.

![Greenhouse](/images/greenhouse.png)

The entire _Greenhouse_ scenario is based on two separate applications:

- **greenshouse**: Sensor data readings, data transmission via RaspberryPi to SAP HCP and an HTML5 UI/Dashboard developed with [SAPUI5](https://sapui5.netweaver.ondemand.com/) on SAP HCP.

![GreenhouseTiles](/images/greenhouse_tiles.png)
![GreenhouseUI1](/images/greenhouse_ui_1.png)
![GreenhouseUI2](/images/greenhouse_ui_2.png)

- **remotecontroller**: Receiving the messages sent to the device. It acts as a controller to switch on/off a lamp, open/close the roof consuming messages sent to the devices.

![RemoteController](/images/remote_controller.png)

## Shopping list
Here a list of components used to build the scenario:

- 1 Raspberry Pi B+ or Raspberry Pi 2
- 1 AM2302 sensor
- 1 Breadboard   
- 3 leds (Red, Green and Yellow)
- 3 resistors 330Ω
- 1 T-Cobbler cable
- 1 DC 5V Relay module
- 1 Lamp
- 1 [Continuous Rotation Servo](http://www.adafruit.com/products/154)
- 1 Additional 5V (2000mA) power supply
- Some jumpers
- Plexiglass box (W: 50cm H: 25cm)

## Prerequisites
In this section you can find a quick list of prerequisites, software and hardware.

Discussing how to connect leds, lamp, servo motor and so on to the RaspberryPi as well as the SAP HCP IoT architecture, features etc. are outside the scope of this document; There are lots of resources available on line.

### RaspberryPi
The RaspberryPi acts as a gateway. All the code is written in Python 3  (v. 3.2) and uses some python libs. Take a look to the following links to install all the requirements:

- [RPi.GPIO](https://learn.adafruit.com/playing-sounds-and-using-buttons-with-raspberry-pi/install-python-module-rpi-dot-gpio)
- [Requests](http://docs.python-requests.org/en/latest/)

#### Getting started with SAP HCP IoT
Use the following documentations as step-by-step guide to get start with all you need on SAP HCP IoT:

1. [Get HANA Cloud Platform Developer Account](https://github.com/SAP/iot-starterkit/blob/master/src/prerequisites/account)
2. [Enable Internet of Things Services](https://github.com/SAP/iot-starterkit/blob/master/src/prerequisites/service)
3. [Create Device Information in Internet of Things Services Cockpit](https://github.com/SAP/iot-starterkit/blob/master/src/prerequisites/cockpit) and take note of device id, OAuth Token etc.
4. [Deploy the Message Management Service (MMS)](Deploy the Message Management Service (MMS))
5. [Consume the messages with HANA XS using XSJS and OData](https://github.com/SAP/iot-starterkit/tree/master/src/apps/xs/consumption)

## How to use it.
In this section you can find steps to replicate the entire scenario. Make sure all the above prerequisites are in place.

### 1. RaspberryPi
To handle the AM2302 sensor protocol (as well as for of DHT11 and DHT22) will use an utility developed by [Adafruit](http://adafruit.com) that, among other things, develops and sells many interesting accessories for RaspberryPi.

The sources of Adafruit also contains a library to allow Python code to access the sensor data. Unfortunately, at the moment, the library has not been updated to support Python 3. We will use a class in Python 3, [DHTUtils](apps/greenhouse/raspberrypi/utils/dhtutils.py), as a wrapper that implements methods to make the call to the library Adafruit.

First of all, we clone the [Adafruit_Python_DHT](https://github.com/adafruit/Adafruit_Python_DHT) Github repository and save the code in a `Adafruit ` folder within the `home` directory of `pi` user:

```shell
cd ~/
mkdir Adafruit && cd $_
git clone https://github.com/adafruit/Adafruit_Python_DHT.git
```

The, we clone this repository:

```shell
cd ~/
git clone https://github.com/indaco/saphcpiot-greenhouse.git
```

Create a folder to save the code inside it:

```shell
cd ~/
mkdir code
```

Move code for the _greenhouse_ app to the right folder:

```shell
cd ~/
mv ~/saphcpiot-greenhouse/apps/greenhouse/raspberrypi ~/code/greenhouse
```

and adapt the [configs.py](apps/greenhouse/raspberrypi/configs.py) with your information

Copy and paste code for the _remotecontroller_ app to the right folder
```shell
cd ~/
mv ~/saphcpiot-greenhouse/apps/remotecontroller/raspberrypi ~/code/remotecontroller
```
and adapt the [configs.py](apps/remotecontroller/raspberrypi/configs.py) with your information

### 2. SAP HCP

#### Greenhouse App
1. Create a [new XS App](https://github.com/SAP/iot-starterkit/tree/master/src/apps/xs/consumption#hana-xs-development) for the _Greenhouse_
2. Copy all the code in `~/saphcpiot-greenhouse/apps/greenhouse/hcp/xs/iotmmsxs` to the HANA XS app previously created
3. Adapt the following files to reflect information from your account and your HANA Schema:
   - [.xsaccess](apps/greenhouse/hcp/xs/iotmmsxs/.xsaccess)
   - [.xsprivileges](apps/greenhouse/hcp/xs/iotmmsxs/.xsprivileges)
   - [roles/user.hdbrole](apps/greenhouse/hcp/xs/iotmmsxs/roles/user.hdbrole)
   - [services/iotservices.xsodata](apps/greenhouse/hcp/xs/iotmmsxs/services/iotservices.xsodata)
   - [services/lastValues.xsjs](apps/greenhouse/hcp/xs/iotmmsxs/services/lastValues.xsjs)
   - [services/measurements.xsjs](apps/greenhouse/hcp/xs/iotmmsxs/services/measurements.xsjs)
4. Execute the following SQL Script to grant accesses (refer to  [Grant Access](https://github.com/SAP/iot-starterkit/tree/master/src/apps/xs/consumption#grant-roles)) documentation
```SQL
call "HCP"."HCP_GRANT_ROLE_TO_USER"('<user_id>trial.iotmmsxs::iotaccess', '<user_id>');
```

#### Remote Controller App

1. Open the Java project `~/saphcpiot-greenhouse/apps/remotecontroller/hcp/java/it.sapiotlab.greenhouse.remotecontroller` with Eclipse
2. Adapt the [index.html](apps/remotecontroller/hcp/java/it.sapiotlab.greenhouse.remotecontroller/src/main/webapp/index.html) file at the bottom of the page to reflect information from your SAP HCP IoT Cookpit
3. [Compile with Maven and Deploy](https://github.com/SAP/iot-starterkit/tree/master/src/apps/java/consumption#compilation-and-deployment)

## Start & Stop
Two different files are provided to start and stop the applications.

START:
- [start_greenhouse.sh](apps/greenhouse/raspberrypi/start_greenhouse.sh)
- [start_remotecontroller.sh](apps/remotecontroller/raspberrypi/start_remotecontroller.sh)

STOP:
- [stop_greenhouse.sh](apps/greenhouse/raspberrypi/stop_greenhouse.sh)
- [stop_remotecontroller.sh](apps/remotecontroller/raspberrypi/stop_remotecontroller.sh)

Execute them as `sudo`, e.g.:

```shell
cd /home/pi/code/greenhouse/
sudo ./start_greenhouse.sh
```

## Auto-Start&Stop
Crontab tasks are used to automatically start and stop the scenario.

| Application      | Wake-Up | Sleep   | Days            |
| ---------------- | --------| ------- | --------------- |
| Greenhouse       | 8:00 AM | 8:00 PM | Monday - Friday |
| RemoteController | 8:05 AM | 7:55 PM | Monday - Friday |

Run `crontab -e` and paste the following entries:

```shell
# Greenhouse
0 8 * * 1-5 /home/pi/code/greenhouse/start_greenhouse.sh > /tmp/start_greenhouse.log
0 22 * * 1-5 /home/pi/code/greenhouse/stop_greenhouse.sh > /tmp/stop_greenhouse.log
# Remote Controller
5  8  * * 1-5 /home/pi/code/remotecontroller/start_remotecontroller.sh > /tmp/start_remotecontroller.log
55 19 * * 1-5  /home/pi/code/remotecontroller/stop_remotecontroller.sh > /tmp/stop_remotecontroller.log
```

You can find the `cron-file.txt` for both the applications.

## Miscellaneous
To access the RaspberryPi via SSH or other network protocols without a monitor and moving from network to network, we need to know the IP address. The [startup_mailer.py](app/greeanhouse/raspberrypi/scripts/startup_mailer.py) utility do exactly this task. It's based on [RPi Email IP On Boot Debian](http://elinux.org/RPi_Email_IP_On_Boot_Debian) documentation by Cody Giles.

## Further Resources

- [SAP Hana Cloud Platform](http://hcp.sap.com/)
- [SAP HANA Cloud Platform Developer Center](http://scn.sap.com/community/developer-center/cloud-platform)
- [SAP HANA Cloud Platform Internet of Things (IoT) Services](https://help.hana.ondemand.com/iot/frameset.htm)
- [SAP HANA Cloud Platform IoT Starter Kit](https://github.com/SAP/iot-starterkit)
- [Turning on an led with your RaspberryPi's GPIO pins](http://thepihut.com/blogs/raspberry-pi-tutorials/27968772-turning-on-an-led-with-your-raspberry-pis-gpio-pins)
- [Controlling Relay Boards using RaspberryPi](https://elementztechblog.wordpress.com/2014/09/09/controlling-relay-boards-using-raspberrypi/)
- [Controlling Servo Motors](http://razzpisampler.oreilly.com/ch05.html)

## License
All the code is released under [Creative Commons CC0 1.0 Universal (CC0 1.0)](https://creativecommons.org/publicdomain/zero/1.0/) license
