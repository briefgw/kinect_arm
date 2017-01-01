#include <Servo.h>

// use serial.print(), not serial.println()

Servo gearboxServo;
// gearboxServo range = [37,154]

int rightPosition = 37;
int leftPosition = 154;

void setup() {
  gearboxServo.attach(12);  // attaches the servo on pin 9 to the servo object
  Serial.begin(9600);

  delay(5*1000); // wait 5 seconds for gearboxServo to go to default position

}

void loop() {
  String pythonCommand = "";
  if (Serial.available())  {
    pythonCommand = Serial.readString();
  }
  delay(100);

  if(pythonCommand == "move gearboxServo to leftPosition"){
    gearboxServo.write(leftPosition);
    Serial.print("moving gearbox to leftPosition now. -Arduino");
    delay(5*1000); //wait 5 seconds
    Serial.print("gearbox movement completed! -Arduino");
  }

  if(pythonCommand == "move gearboxServo to rightPosition"){
    gearboxServo.write(rightPosition);
    Serial.print("moving gearbox rightPosition now. -Arduino");
    delay(5*1000); //wait 5 seconds
    Serial.print("gearbox movement completed! -Arduino");
  }

  pythonCommand = "";// reset pythonCommand
}

