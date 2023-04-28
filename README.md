# cs370termproject

This project will provide a basic, or “starter,” library that provides a programmer with several options to interact with the sensors (placed on a breadboard) that are connected to the Raspberry Pi. This library can be thought of as an extra layer of abstraction between the sensors/Raspberry Pi and the programmer. These basic interactions include:

+ Detecting whether the light is on or off in the surrounding room
+ If the light has just been switched on, how long has the room been dark for?
+ Detecting when a user hovers their hand, or any other object, over a sensor – which is analogous to a virtual button press. When the user virtually “presses a button,” an LED would blink to indicate that input has been received
+ Turn on or off an LED light fixed onto the breadboard
+ Detecting motion in the surrounding area – and not just user’s hand right in front of a sensor as in the “virtual button” feature above.
+ Additionally, the sensor used as “virtual button” above can also measure distance to an object right in front, if the sensor is oriented towards the object. So for example, if desired, a programmer can also detect whether the user is sitting at a desk or not.

Using this library requires that the programmer can connect DuPont wires correctly between the different pins of the sensors and the appropriate GPIO pins on the Raspberry Pi, and pass in the pin numbers into the library.

In the userAssistantProgram.py, the simple “personal assistant” program will utilize all other modules to detect when the light comes back on after a few hours, indicating that the user either has just woken up, or has just come home. If the current time is early morning, the program will read out summary of weather and news (location or topics are hard-coded settings).

The sensors will detect when the user starts sitting at the desk, and the program will read a reminder of tasks that the user previously typed or recorded. The user has the option to cancel this reminder reading.

Related to this reminder feature, the user can hover one of the sensors to activate the recording feature to record a reminder to be read to themselves later.

This program will have no GUI component. It will be executed from the console. Given the purpose of experimenting with sensors as input, this program will not take inputs from the console.

