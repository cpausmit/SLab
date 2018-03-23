//==================================================================================================
// Useful global variables
//==================================================================================================
unsigned long microSecs = 0;

int sensorValue0 = 0;  // variable to store the value coming from sensor 0
int sensorValue1 = 0;  // variable to store the value coming from sensor 1

int voltage0 = 0;      // variable to store voltage value 0
int voltage1 = 0;      // variable to store voltage value 1

//==================================================================================================
// General setup, once executed when you start the program
//==================================================================================================
void setup() {

  // Make sure we have a serial output to print our results  
  Serial.begin(9600);
  Serial.println(" Hello World! Startup of the Measurement Series.");
 
}

//==================================================================================================
// Continuously executed code that runs in the microprocessor
//==================================================================================================
void loop() {

  // read the analog value on pin 0 and 1
  microSecs = micros();
  sensorValue0 = analogRead(A0);
  sensorValue1 = analogRead(A1);
 
  // output one full series of readings
  Serial.print(microSecs);
  Serial.print(",");
  Serial.print(sensorValue0);
  Serial.print(",");
  Serial.print(sensorValue1);
  // end of the line
  Serial.println("");

  delay(1000); // 1000 milli seconds
}
