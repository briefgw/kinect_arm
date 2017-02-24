/*  Karl Preisner
 *  17 Feb 2017
 *  
 *  This program is a slave to the Raspberry Pi running motorServer.py
 *  It accepts commands for the following devices:
 *    - Servo Gearbox (Kinect camera mount joint)
 *    - Middle Linear Actuator
 *    - Bottom Linear Actuator
 *    
 *  A USB Serial communication is used for receiving commands from the Raspberry Pi's
 *  motorServer.py.
 *  Note: Use serial.print(), not serial.println().
 *  
 *  The Servo Gearbox and Linear Actuators use the Servo Library. When the goal 
 *  position for a servo is written to its respective digital pin, the servo 
 *  drives to that position until its built-in potentiometer says the position has 
 *  been acheived. There is no feedback from the motor as to when the position is 
 *  acheived. 
 *  
 *  Motor Ranges:
 *    - Servo Gearbox range = [65,149]
 *    - Middle linear actuator range = [20,140]
 *    - Bottom Linear Actuator range = [20,140]
 */
#include <Servo.h>

Servo servoGearbox;
Servo middleActuator;
Servo bottomActuator;

const int servoGearboxPin = 3;
const int middleActuatorPin = 11;
const int bottomActuatorPin = 10;

const int min_actuator_pulse = 1000;
const int max_actuator_pulse = 2000;

//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//~~~~~~~~~~~~~~~~~~~~~~~~~~~Setup~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
void setup() {
  // Set the starting positions for each motor (Change this when we construct the arm.)
  servoGearbox.write(105);
  middleActuator.write(20);
  bottomActuator.write(20);
  
  // Attach servoGearbox, middleActuator, bottomActuator
  servoGearbox.attach(servoGearboxPin);  // attaches the gearboxServo to a Servo object
  middleActuator.attach(middleActuatorPin, min_actuator_pulse, max_actuator_pulse);
  bottomActuator.attach(bottomActuatorPin, min_actuator_pulse, max_actuator_pulse);

  // Open Serial communication with RPi
  Serial.begin(115200);
  Serial.setTimeout(100); // Set timeout to 100ms (default is 1000ms).

  delay(5*1000); // wait 5 seconds for servoGearbox to go to default position (105 degrees)
}

//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//~~~~~~~~~~~~~~~~~~~~~~~~~~~Loop~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
void loop() {
  String masterCommand = "";
  if (Serial.available()) {
    masterCommand = Serial.readString();
  }
  if(masterCommand == "Are you alive?"){
    Serial.print("I'm alive! -Arduino");
  }
  else if(masterCommand != ""){
    moveMotor(masterCommand);
  }
}


// Move specific motor.
void moveMotor(String masterCommand){
  // First add '\n' to masterCommand string
  String tempStr = masterCommand + "\n";

  // Convert to char array
  char cmd[tempStr.length()];
  tempStr.toCharArray(cmd, tempStr.length());
    
  // Tokenize masterCommand:
  char *i, *motor, *val;
  char *c = cmd;
  // Get motor
  motor = strtok_r(c,":",&i);
  // Get value, turn into an int
  val = strtok_r(NULL,"",&i);
  int value = String(val).toInt();

  // Move Servo Gearbox to 'value'
  if(String(motor).equals("Servo Gearbox")){
    Serial.print("Begin moving motor. -Arduino");
    servoGearbox.write(value);
    delay(0.5*1000);
    Serial.print("Finished moving motor. -Arduino");
  }
  // Move Lineaer Actuator - Middle to 'value'
  else if(String(motor).equals("Linear Actuator - Middle")){
    Serial.print("Begin moving motor. -Arduino");
    middleActuator.write(value);
    delay(0.5*1000);
    Serial.print("Finished moving motor. -Arduino");
  }
  // Move Lineaer Actuator - Bottom to 'value'
  else if(String(motor).equals("Linear Actuator - Bottom")){
    Serial.print("Begin moving motor. -Arduino");
    bottomActuator.write(value);
    delay(0.5*1000);
    Serial.print("Finished moving motor. -Arduino");
  }
 
} // End moveMotor()




