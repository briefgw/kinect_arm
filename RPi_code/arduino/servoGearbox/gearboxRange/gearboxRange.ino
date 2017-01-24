// Karl Preisner
// Sweep ServoGearbox left and right. 
// 12/16/2016


/* Sweep
 by BARRAGAN <http://barraganstudio.com>
 This example code is in the public domain.

 modified 8 Nov 2013
 by Scott Fitzgerald
 http://www.arduino.cc/en/Tutorial/Sweep
*/

#include <Servo.h>

Servo myservo;  // create servo object to control a servo
// twelve servo objects can be created on most boards

int pos = 0;    // variable to store the servo position

void setup() {
  myservo.attach(9);  // attaches the servo on pin 9 to the servo object
  Serial.begin(9600);  
}


// For the ServoGearbox, the range of positions are calibrated as described below: 
// When looking at the ServoGearbox from the top, with the Hitech label below the gear,
//  left most position = 154.
//  right most position = 37.
// It takes 10 seconds to move from leftPos to rightPos*
// make sure the tape is lined up on the gear and the right-angle connector*


int leftPos = 154; // 154 is set. do not go to 155 or higher.
int rightPos = 37; // 37 is set. do not go to 36 or lower.


// To make the loop method only run a segment of code once, I set a boolean flag.
boolean runFlag = true;
void loop() {

  while(runFlag == true){
    Serial.println("Begin function to move ServoGearbox");
    
    myservo.write(leftPos);
    Serial.println("left pos");
    delay(10*1000); //wait 10 seconds
    
    myservo.write(rightPos);
    Serial.println("right post");
    delay(10*1000);
    
    
    runFlag = false; // set runFlag to false so that the above code does not run again.
    
  } // end while


//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  // This segment of code is an example how you can change the speed of the motor.

//  for (pos = rightPos; pos <= leftPos; pos += 1) { // goes from rightPos to leftPos
//    // in steps of 1 degree
//    myservo.write(pos);              // tell servo to go to position in variable 'pos'
//    delay(50);                       // waits 15ms for the servo to reach the position
//  }
//  Serial.println(pos);
//  for (pos = leftPost; pos >= rightPos; pos -= 1) { // goes from leftPos to rightPos
//    myservo.write(pos);              // tell servo to go to position in variable 'pos'
//    delay(50);                       // waits 15ms for the servo to reach the position
//  }


} // End void loop()

