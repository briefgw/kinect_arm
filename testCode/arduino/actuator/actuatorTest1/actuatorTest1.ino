// Karl Preisner
// NOTE: All arduino programs need setup() and loop() methods.
// Linear Actuator control
// Actuator calibration: range = [0,180]
// Gearbox calibration: range = [37,154] *Do not go past these as the gearbox will be damaged.*


// Methods from Servo library:
// 1. servo.attach(digital pin, PWM min, PWM max) where PWM min and max are in microseconds.
// 2. servo.write(degree) where degree is from 0 to 180
// 3. servo.writeMicroseconds(microseconds) where, 
//        Range is the PWM microsecond range of 1000-2000. 
//        Setting to 1500 = degree of 90.
// 4. servo.read()
//        This reads the last position given from the servo.write() method.
//        This does NOT read the actual potentiometer value at the time of the method call.


// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// setup():

# include <Servo.h>

// Create servo objects. 12 can be created on most boards.
Servo servo1; //linear actuator 1
Servo servo2; //linear actuator 2

Servo gearbox; // range from 
const int gearboxpin = 12;

const int servo1pin = 9;
const int servo2pin = 10;
const int microsecLOW = 1000;
const int microsecHIGH = 2000;

void setup() { // put your setup code here, to run once:
  
  // Begin Serial monitor.
  Serial.begin(9600);
  Serial.println("Begin setup().");

  // Set initial positions of each actuator. This is after they get set to default position.
//  servo1.write(180);
//  servo2.write(30);

  // Attach the servos to pins 9 and 10. 
  // Set PWM range to 1000-2000 microseconds when attaching.
  servo1.attach(servo1pin, microsecLOW, microsecHIGH);
  servo2.attach(servo2pin, microsecLOW, microsecHIGH);

  gearbox.attach(gearboxpin);

  Serial.print("--Servo1 attached with initial position = ");
  Serial.println(servo1.read());
  Serial.print("--Servo2 attached with initial position = ");
  Serial.println(servo2.read());

  Serial.print("--Gearbox attached with initial position = ");
  Serial.println(gearbox.read());

  Serial.println("--Wait 20 seconds for motors to get their default positions (90 degrees).");
  printDelay(20);
//  delay(20*1000); //wait 20 seconds
  
  Serial.println("----setup() completed.\n");
} // end void setup()





// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// loop():

boolean runFlag = true;
void loop() { // put your main code here, to run repeatedly:
  if(runFlag == true){

    testGearboxRange(); 
    testServo1();

//    testMicrosecMove();
//    testServo2();

    
  } // end runFlag
  runFlag = false;
} // end void loop()











// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// Control Methods:

// moveServoDeg()
void moveServoDeg(Servo servo, int goalDeg){
  Serial.println("Begin moveServoDeg().");

  int initialPos = servo.read();
  Serial.print("--Initial position (deg) = ");
  Serial.println(initialPos);
  Serial.print("--Goal position = ");
  Serial.println(goalDeg);

  servo.write(goalDeg);
//  delay(25*1000); //wait 10 seconds
  waitTravel(initialPos, goalDeg);

  Serial.print("--Movement completed. Current position (deg) = ");
  Serial.println(servo.read());
  Serial.println("----moveServoDeg() completed.\n");
}


// moveServoMicrosec()
void moveServoMicrosec(Servo servo, int microsec){
  Serial.println("Begin moveServoDeg().");
  Serial.print("--Initial position (deg) = ");
  Serial.println(servo.read());
  Serial.print("--Goal position (microseconds) = ");
  Serial.println(microsec);

  servo.writeMicroseconds(microsec);
  delay(10*1000); //wait 10 seconds

  Serial.print("--Movement completed. Current position (deg) = ");
  Serial.println(servo.read());
  Serial.println("----moveServoDeg() completed.\n");
}



// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// Utility methods:


// wait for motor to travel specified.
void waitTravel(int initialDeg, int goalDeg){
  int distDeg = goalDeg - initialDeg;
  if(distDeg < 0){
    distDeg = distDeg * (-1);
  }

  if(distDeg > 0 && distDeg < 30){
    Serial.print("--Degrees traveled = ");
    Serial.print(distDeg);
    Serial.println(". So, wait 16 seconds.");
//    delay(16*1000); // wait 16 sec
    printDelay(16);
  }
  else if(distDeg >= 30 && distDeg < 90){
    Serial.print("--Degrees traveled = ");
    Serial.print(distDeg);
    Serial.println(". So, wait 19 seconds.");
//    delay(19*1000); // wait 19 sec
    printDelay(19);
  }
  else if(distDeg >= 90 && distDeg < 135){
    Serial.print("--Degrees traveled = ");
    Serial.print(distDeg);
    Serial.println(". So, wait 22 seconds.");
//    delay(22*1000); // wait 22 sec
    printDelay(22);
  }
  else if(distDeg >= 135 && distDeg <= 180){
    Serial.print("--Degrees traveled = ");
    Serial.print(distDeg);
    Serial.println(". So, wait 25 seconds.");
//    delay(25*1000); // wait 25 sec
    printDelay(25);
  }
}

void printDelay(int seconds){
  Serial.print("--Counting down: ");
  for(int i = seconds; i > 0; i--){
    Serial.print(i);
    Serial.print(" ");
    delay(1000);
  }
  Serial.println();
}


// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// test methods:

void testGearboxRange(){
  Serial.println("\nTest: move gearbox to 37");
  gearbox.write(37);
  printDelay(10);
  Serial.println("\nTest: move gearbox to 154");
  gearbox.write(154);
  printDelay(10);
}


void testMicrosecMove(){
  Serial.println("\nTest: moveServoMicrosec(servo1, 1000)");
  moveServoMicrosec(servo1, 1000);

  Serial.println("\nTest: moveServoMicrosec(servo1, 1750)");
  moveServoMicrosec(servo1, 1750);
}


void testServo1(){
  
  Serial.println("\nTest: moveServoDeg(servo1, 180)");
  moveServoDeg(servo1, 180);

  Serial.println("\nTest: moveServoDeg(servo1, 90)");
  moveServoDeg(servo1, 90);
  
  Serial.println("\nTest: moveServoDeg(servo1, 0)");
  moveServoDeg(servo1, 0);

  Serial.println("\nTest: moveServoDeg(servo1, 90)");
  moveServoDeg(servo1, 90);
}

void testServo2(){ //servo2
  Serial.println("\nTest: moveServoDeg(servo2, 180)");
  moveServoDeg(servo2, 180);

  Serial.println("\nTest: moveServoDeg(servo2, 90)");
  moveServoDeg(servo2, 90);
  
  Serial.println("\nTest: moveServoDeg(servo2, 0)");
  moveServoDeg(servo2, 0);

  Serial.println("\nTest: moveServoDeg(servo2, 90)");
  moveServoDeg(servo2, 90);
}






//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// Increment movement

// scrapping the idea of moveServoIncrement
void testIncrement(){
  Serial.println("Test: moveServoIncrement(servo1, 0)");
  moveServoIncrement(servo1, 0);

  Serial.println("Test: moveServoIncrement(servo1, 90)");
  moveServoIncrement(servo1, 90);
}



// This method does not work well with this library and motors. 
void moveServoIncrement(Servo servo, int deg){
  int x = servo.read(); // current position of the motor
  
  int i = 1; // i is the increment, positive or negative
  if(x > deg){
    i = -1;
  }
  
  while(x != deg){
    x = x + i;
    servo.write(x);
    delay(150);
    Serial.print("--x = ");
    Serial.println(servo.read());
  }

  // THIS IS NOT THE CORRECT WAIT TIME. MUST BE FIXED IF YOU WANT TO USE THIS METHOD.
  Serial.println("--Wait 5 seconds");
  delay(5*1000); //wait 5 seconds
  Serial.println("----moveServoIncrement() completed.\n");
}



