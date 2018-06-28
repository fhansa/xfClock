# xfClock - DRAFT ONGOING WORK

Small lightweight MagicMirror-type clone to be used as a bedroom clock (or similar).    
Concept is similar to MagicMirror but implemented using PyGame with a goal to run on a PiZero.

*Insert picture*


## Getting Started
To install xfClock you will need a Raspberry Pi with some kind of screen.  

### Prerequisites

A Raspberry PI with screen.   
I will not go throught installation of PI and/or Screen. It is up to you to fix.   
Below is how I did it using PiZero and a Adafruit PiTFT.

* Python3
* Pygame - SDL
*

### Installing

Clone xfClock to your RaspberryPi
```
git clone xxxxx
```
Setup configuration by creating config.py (e.g. by copying sample_config.py)  
Default configuration will show an ananlogue clock with a two-liner calendar. 

```
cd xfClock
cp sample_config.py config.py
```

Start xfClock for testing 
```
python3 main.py
```

## Configuration

## Modules

Built-in modules

Clock - a simple analogue clock. 
Options:
	* Face

Calendar - Show calendar items on Screen
Options:
	* ICS-url
	* max number of items
	*

Screen - MQTT recipient to turn screen on and off:
Options:
	* mqttTopic
	* payload_on
	* payload_off

Gesture Recognizer - APDS9960 gesture sensor conencted to xfClock
Is used to control stuff using MQTT
	* mqtt command topic
	* gesture map
		up 
		down
		left	
		right

Schematic overview of xfClock - default configuration

Setup in MQTT Broker (and using NodeRed) is
 	Gesture Up 	-> Screen On
	Gesture Down 	-> Screen Off
	Gesture Left	-> Bedroom light on
	Gesture Right	-> Bedrum light off or Set House in night mode

### Develop your own module

## xfClock using piZero and PiTFT
this is how I did it

* Rasbian [LINK]
* PiTFT [LINK]
* FAMEBUFFER
* 

## Built With

* PyGame
* Adafruit PiTFT

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.


## Authors

* **Fredrik Hansson** - *Initial work* 

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Mitch MagicMirror...
