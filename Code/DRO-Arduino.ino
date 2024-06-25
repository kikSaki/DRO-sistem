//length: 50 mm = 50000 um
//resolution: 5 um
//steps: 50000 um / 5 um = 10000
//REMEMBER! You have to calibrate your scale to get precise values in physical units
//You only get increments here and you have to calibrate the increments
 
#define encoder0PinA  2 //Pin 2 is one of the pins which works with attachInterrupt() on Arduino UNO
#define encoder0PinB  4
 
volatile int encoder0Pos = 0; //Position of the encoder
boolean newdata = false; //Flag to see if there's new data (the encoder was moved)

String input;


void setup() {

  Serial.begin (115200);
  pinMode(encoder0PinA, INPUT); //Pin 2 = Input
  digitalWrite(encoder0PinA, HIGH);       // turn on pull-up resistor
  pinMode(encoder0PinB, INPUT); //Pin 4 = Input
  digitalWrite(encoder0PinB, HIGH);       // turn on pull-up resistor
 
  attachInterrupt(digitalPinToInterrupt(encoder0PinA), doEncoder, CHANGE);  // encoder pin on interrupt 0 - pin 2
  attachInterrupt(digitalPinToInterrupt(encoder0PinB), doEncoder, CHANGE);
  




  
}

void printej(int encoder0Pos){

     //char buf[16];
     //sprintf(buf, "%05d", encoder0Pos);
     //Serial.println(buf);


     Serial.println(encoder0Pos);
}
 
void loop()
{
  if(newdata == true) //if the encoder was moved
  {
    printej(encoder0Pos);
  }

  
  if(Serial.available()){
      input = Serial.readStringUntil('\n');
      encoder0Pos = input.toInt();
      printej(encoder0Pos);
      //Serial.print("You typed: " );
      //Serial.println(input);
    }
  
 
  newdata = false; //we switch the flag to 'false' so the Arduino will not do anything until a new data comes in
}
 
void doEncoder() //if the attachInterrupt() is triggered, this function runs
{
   if (digitalRead(encoder0PinA) == digitalRead(encoder0PinB)) //if the Arduino saw the square waves' rising edge
  {
    encoder0Pos++; // increase the position
  } else {
    encoder0Pos--; //otherwise decrease the position
  }
  newdata = true; //we change this flag, so the if statement in the loop() will run and the data will be printed 
}
