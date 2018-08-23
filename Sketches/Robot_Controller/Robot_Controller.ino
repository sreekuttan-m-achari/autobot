#include <Servo.h>
#include <NewPing.h>

String robot_status = "";
String wheels_status = "" ;
String msg = "" ;

#define TRIGGER_PIN 4
#define ECHO_PIN 5
#define MAX_DISTANCE 200

NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE); // NewPing setup of pins and maximum distance.
Servo rangeFinderServo;

const int leftForward = 6;
const int rightBackward = 7;

const int rightForward = 10;
const int leftBackward = 9;

int min_ang = 30;
int max_angle = 150;
int pos = 90 ;
int demo_dly = 5000 ;
int speedLimit = 150 ;

int pivotLimit = 300 ;
int proximityLimit = 30; // stops at <proximityLimit> cms from obstacle in front 

void setup() {

  // initialize digital pin LED_BUILTIN as an output.
  pinMode(LED_BUILTIN, OUTPUT);

  // Attach a servo to pin #3
  rangeFinderServo.attach(3);

  rangeFinderServo.write(pos);              // tell servo to go to position in variable 'pos'
  delay(50);

  pinMode(leftForward , OUTPUT);
  pinMode(leftBackward , OUTPUT);
  pinMode(rightForward , OUTPUT);
  pinMode(rightBackward , OUTPUT);

  stop_wheels() ;

  // start serial port at 9600 bps:
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
    digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
    delay(1000);                       // wait for a second
    digitalWrite(LED_BUILTIN, LOW);    // turn the LED off by making the voltage LOW
    delay(1000);
  }
  establishContact();  // send a byte to establish contact until receiver responds
}

void establishContact() {
  while (Serial.available() <= 0) {
    Serial.println("check");   // check status
    delay(1000);
  }
}


void loop() {
  delay(50);
  proximity_check();

  // if we get a valid byte, read analog ins:
  if (Serial.available() > 0) {
    // get incoming byte:
    robot_status = Serial.readString();

    wheels_status = String(robot_status)  ;

    digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)

    //Serial.println(wheels_status);   // check status


    if (wheels_status == "FORWARD") {
      move_forward() ;
    }
    else if (wheels_status ==  "REVERSE") {
      move_backward();
    }
    else  if (wheels_status ==  "PIVOT_RIGHT") {
      pivot_right();
    }
    else if (wheels_status ==  "PIVOT_LEFT") {
      pivot_left();
    } else if (wheels_status ==  "FIND_WAY") {
      find_way();
    }

    else if (wheels_status ==  "STOP") {
      stop_wheels();
    }

    digitalWrite(LED_BUILTIN, LOW);    // turn the LED off by making the voltage LOW
  }
}


void move_forward() {
  stop_wheels();
  //proximity_check();
  Serial.println("FWD");
  delay(30);
  digitalWrite(leftForward , LOW);
  digitalWrite(leftBackward , HIGH);
  digitalWrite(rightForward , HIGH);
  digitalWrite(rightBackward , LOW);

}

void move_backward() {
  stop_wheels();
  Serial.println("BKW");
  delay(30);
  digitalWrite(leftForward , HIGH);
  digitalWrite(leftBackward , LOW);
  digitalWrite(rightForward , LOW);
  digitalWrite(rightBackward , HIGH);
}


void pivot_right() {
  stop_wheels();
  Serial.println("PVTR");
  delay(30);
  digitalWrite(leftForward , HIGH);
  digitalWrite(leftBackward , LOW);
  digitalWrite(rightForward , HIGH);
  digitalWrite(rightBackward , LOW);
  delay(pivotLimit);
  stop_wheels();

}

void pivot_left() {
  stop_wheels();
  Serial.println("PVTL");
  delay(30);
  digitalWrite(leftForward , LOW);
  digitalWrite(leftBackward , HIGH);
  digitalWrite(rightForward , LOW);
  digitalWrite(rightBackward , HIGH);
  delay(pivotLimit);
  stop_wheels();

}


void stop_wheels() {
  Serial.println("STPWHLS");
  delay(30);
  digitalWrite(leftForward , LOW);
  digitalWrite(leftBackward , LOW);
  digitalWrite(rightForward , LOW);
  digitalWrite(rightBackward , LOW);
}

void find_way() {

  int i;

  for ( i = 0; i < 180; i++) {
    rangeFinderServo.write(i);
    delay(3);
  }

  for (i = 180; i != 0; i--) {
    rangeFinderServo.write(i - 180);
    delay(3);
  }

  rangeFinderServo.write(pos);
}

void proximity_check() {

  unsigned int uS = sonar.ping_cm();
  delay(50);
  Serial.print(uS); 
  delay(50);
  if (uS < proximityLimit && wheels_status == "FORWARD" ) {
    stop_wheels();
    Serial.println("Obstacle:STOP!");
    delay(30);
    //find_way();
  } 
}
