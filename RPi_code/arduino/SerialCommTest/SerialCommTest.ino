


void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);

}

void loop() {
  // put your main code here, to run repeatedly:
  String s = "1";
  
  if (Serial.available())  {
    s = Serial.readString();
  }
  delay(500);

  if(s == "Hello from Python!"){
    Serial.print("Hi from Arduino!");
  }
  s = "1";
}
