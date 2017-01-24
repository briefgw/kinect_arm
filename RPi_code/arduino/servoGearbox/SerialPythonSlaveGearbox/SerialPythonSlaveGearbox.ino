#include <Servo.h>

// Karl Preisner
// This program is a slave to the Raspberry Pi.
// It accepts commands to move the Servo Gearbox, middle/bottom Linear actuators.

// Note: Use serial.print(), not serial.println().

Servo servoGearbox;
// servoGearbox range = [37,154]
//int rightPosition = 37;
//int leftPosition = 154;


//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//~~~~~~~~~~~~~~~~~~~~~~~~~~~Setup~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
void setup() {
  // Attach Servo Gearbox
  servoGearbox.attach(12);  // attaches the servo on pin 12 to the servo object
  
  // Open Serial communication with Pi
  Serial.begin(115200);
  Serial.setTimeout(100); // default is 1000ms, set to 100ms

//  delay(5*1000); // wait 5 seconds for servoGearbox to go to default position

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
    
    // Tokenize masterCommand:
    char *i, *motor, *val;
    char *c = cmd;
    // Get motor
    motor = strtok_r(c,":",&i);
    // Get value, turn into an int
    val = strtok_r(NULL,"",&i);
    int value = String(val).toInt();
    
//    Serial.print(motor);
//    delay(0.5*1000);
//    Serial.print(value);

    // Move Servo Gearbox to 'value'
    if(motor = "Servo Gearbox"){
      Serial.print("Begin moving motor. -Arduino");
      servoGearbox.write(value);
      delay(5*1000); //wait 5 seconds (10s to get from side to side
      Serial.print("Finished moving motor. -Arduino");
    }
    // Move Lineaer Actuator - Middle to 'value'
    else if(motor = "Linear Actuator - Middle"){
      Serial.print("Begin moving motor. -Arduino");
      servoGearbox.write(value);
      delay(5*1000); //wait 5 seconds (22s to get from side to side
      Serial.print("Finished moving motor. -Arduino");
    }
    // Move Lineaer Actuator - Bottom to 'value'
    else if(motor = "Linear Actuator - Bottom"){
      Serial.print("Begin moving motor. -Arduino");
      servoGearbox.write(value);
      delay(5*1000); //wait 5 seconds (22s to get from side to side
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

