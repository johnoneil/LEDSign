LEDSign
=======

Code to control a Chainzone (Texcellent) Sigma 3000 compatible JetFileII Protocol based LED Sign

![example image display](https://github.com/johnoneil/LEDSign/blob/master/images/TQzHZa6.jpg?raw=true)

Cable Wiring Example
====================
My texcellent sign did not come with the direct ethernet interface board, so I had to control it serially. However, the only available port to do so was an rj11 (5 pin "telephone") style port. It was necessary to do a little digging an poking to find the pin definitions in order to construct a cable to connect this to a db9 PC serial port.
In the end, the pinouts for both sides of the cable (between any PC DB9 and my LED sign rj11) is as follows:

![pinouat diagram](https://github.com/johnoneil/LEDSign/blob/master/images/pinouts.png?raw=true)

