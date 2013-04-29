# Hardware

The brew setup uses a cooler mashtun, a hotwater tun and a boiler, and it is all electric. From a software point of view the different units are controller by "appliances", this includes a controller, as a switch for a heater element, and a sensor, a thermometer.

All controllers and sensors are USB based, and this is done by design. USB  is well supported, and allows you to use any PC based computer. USB devices enables a modular design, allowing the controller to grow incrementally without having to change hardware. As example, the original design was just a thermostat for the strike water, consisting of a X10 controller and a USB thermometer. 

Many USB devices are well supported with API or source code examples. All the USB devices currently in use have source code support. The script SETUP will pull down the code if it is not included in the repo.


#### Appliances
Appliances includes a controller and a sensor working together. As example the hot water tun water heater consists of an X10 controller water heat element and a GoIO USB thermometer. The appliance is set with a target temperature and will manage the heater element to ensure that hot water tun has reached the right water temperature. Note that the same controller and sensors could be used by multiple appliances. The brewing requires each appliance to meet it's target before the next step can be taken, as example the strike water will not be pumped into the mash tun before the water heater for the hot water tun has reached it's target temperature. Note that there is also a timer "sensor" that can be used to hold an not do anything, as example during the mashing.

* [Water heater](https://github.com/cloudymike/hopitty/wiki/Water-Heater)
* Hot Water Pump
* Wort Pump
* Boiler
* Hop dispenser
* Hot Water Circulation
* Mash Circulation

#### Controllers and Sensors

Controllers
* X10 switch
* Phidget pump controller
* Polulo dispenser controller

Sensors
* GoIO thermometer
* DigiScale USB scale
* Timer (though not strictly a sensor)

