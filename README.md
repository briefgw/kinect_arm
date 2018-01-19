# Camera Arm Components #
### Computers and microcontrollers ###
* Ubuntu 14.04 machine
* Xbox Kinect
* Raspberry Pi
* Arduino Uno

### Motors ###
* Nema 23 stepper
* Servo City Linear Actuators (2x)
* Hitec HS-785HB servo with gearbox

### Drivers ###
* M542T stepper motor Driver
	* Used with Nema 23 stepper motor
	* https://www.omc-stepperonline.com/stepper-motor-driver/nema-23-stepper-motor-drive-24-50vdc-15a-45a-256-microstep-m542t-m542t.html
* Actobotics Dual Motor Controller
	* Used with the two Servo City Linear Actuators
	* https://www.servocity.com/actoboticsr-dual-motor-controller-assembled 
_____
# Important Instructions #
### How to properly turn off the Raspberry Pi ###
1. Unplug Actuator Power supply
2. ssh into RPi
3. Run `sudo shutdown -h now`
4. Wait 30 seconds
5. Unplug RPi
_____
# Wiring Guide #
### Raspberry Pi + Stepper Motor Driver (M542T)
![RPi_M542T](/resources/RPi_M542T.jpg)
### Nema23 Stepper Motor + Stepper Motor Driver (M542T)
![Nema23_M542T](https://bitbucket.org/GwuSimhaLab/cameraarm/resources/Nema23_M542T.jpg)
### Arduino Uno + Dual Motor Controller
![Arduino_DualMotorController.jpg](https://bitbucket.org/GwuSimhaLab/cameraarm/resources/Arduino_DualMotorController.jpg.jpg)