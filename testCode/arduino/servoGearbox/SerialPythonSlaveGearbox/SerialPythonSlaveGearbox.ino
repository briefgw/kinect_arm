#include <Servo.h>

// Karl Preisner
// This program is a slave to the Raspberry Pi.
// It accepts commands to move the Servo Gearbox, middle/bottom Linear actuators.

// Note: Use serial.print(), not serial.println().
// servoGearbox range = [37,154]

Servo servoGearbox;
Servo middleActuator;
Servo bottomActuator;

int gearboxWaitSeconds = 10; // wait time for gearbox 
int actuatorWaitSeconds = 24; // wait time for actuators

//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//~~~~~~~~~~~~~~~~~~~~~~~~~~~Setup~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
void setup() {
  // Attach Servo Gearbox, middleActuator, bottomActuator
  servoGearbox.attach(11);  // attaches the gearboxServo on pin 12 to the Servo object
  middleActuator.attach(10);
  bottomActuator.attach(9);


  // Put these above attach??
  // set starting position for Actuators (Change this when we construct the arm.)
  middleActuator.write(90);
  bottomActuator.write(90);
  
  // Open Serial communication with Pi
  Serial.begin(115200);
  Serial.setTimeout(100); // default is 1000ms, set to 100ms

  delay(5*1000); // wait 5 seconds for servoGearbox to go to default position (90 degrees)
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
    // First add '\n' to masterCommand string
    String tempStr = masterCommand + "\n";

    // Convert to char array
    char cmd[tempStr.length()];
    tempStr.toCharArray(cmd, tempStr.length());

    ////////////////////////////////////////////
    Serial.print(cmd);
    delay(0.5*1000);
    ////////////////////////////////////////////
    
    // Tokenize masterCommand:
    char *i, *motor, *val;
    char *c = cmd;
    // Get motor
    motor = strtok_r(c,":",&i);
    // Get value, turn into an int
    val = strtok_r(NULL,"",&i);
    int value = String(val).toInt();

    /////////////////////////////////////////////
    Serial.print(motor);
    delay(0.5*1000);
    Serial.print(val);
    delay(0.5*1000);
    /////////////////////////////////////////////

    // Move Servo Gearbox to 'value'
    if(String(motor).equals("Servo Gearbox")){
      Serial.print("motor == servoGearbox");//////////////////////////
      delay(0.5*1000);
      Serial.print("Begin moving motor. -Arduino");
      servoGearbox.write(value);
      delay(gearboxWaitSeconds*1000); //wait 10 seconds
      Serial.print("Finished moving motor. -Arduino");
    }
    // Move Lineaer Actuator - Middle to 'value'
    else if(String(motor).equals("Linear Actuator - Middle")){
      Serial.print("motor == middleActuator");/////////////////////////
      delay(0.5*1000);
      Serial.print("Begin moving motor. -Arduino");
      middleActuator.write(value);
      delay(actuatorWaitSeconds*1000); //wait 24 seconds
      Serial.print("Finished moving motor. -Arduino");
    }
    // Move Lineaer Actuator - Bottom to 'value'
    else if(String(motor).equals("Linear Actuator - Bottom")){
      Serial.print("motor == bottomActuator");/////////////////////////
      delay(0.5*1000);
      Serial.print("Begin moving motor. -Arduino");
      bottomActuator.write(value);
      delay(actuatorWaitSeconds*1000); //wait 24 seconds
      Serial.print("Finished moving motor. -Arduino");
    }
  }

//  if(masterCommand == "a"){
//    servoGearbox.write(leftPosition);
//    Serial.print("b");
//    delay(0.2*1000); //wait 5 seconds
//    Serial.print("c");
//  }
//
//  if(masterCommand == "move servoGearbox to leftPosition"){
//    servoGearbox.write(leftPosition);
//    Serial.print("moving gearbox to leftPosition now. -Arduino");
//    delay(0.2*1000); //wait 5 seconds
//    Serial.print("gearbox movement completed! -Arduino");
//  }
//
//  if(masterCommand == "move servoGearbox to rightPosition"){
//    servoGearbox.write(rightPosition);
//    Serial.print("moving gearbox to rightPosition now. -Arduino");
//    delay(0.2*1000); //wait 5 seconds
//    Serial.print("gearbox movement completed! -Arduino");
//  }

  masterCommand = "";// reset masterCommand
}

