
//pins
const int partBinsA = 13;
const int partBinsB = 12;
const int belt1 = 11;
const int twelveVolt = 10;


//other consts
const int bins = 12;
int startPos = 0;
const int timeTo360 = 10 * 1000;
const int correctionFactorCW = 270;
const int correctionFactorCC = 240;
bool mode = 0;

/**

Wood skrews
m2
m3
m4
m5
m6
m8
resort
DNE
DNE

**/

void setup() {
  // put your setup code here, to run once:
  pinMode(partBinsA, OUTPUT);
  startPos = 0;
  Serial.begin(9600);
  Serial.println("Run Machine (Y/N)");
  setMotion(0);
}

void loop() {

  if (Serial.available() > 0) {

    int targetPos = Serial.parseInt();  // Read an integer from Serial input

    if(mode == 0){
      if(Serial.read() == "y"){
        setMotion(1);
        Serial.println("Say x to stop");
      }
      if(Serial.read() == "x"){
        setMotion(0);
        Serial.println("Stopped belts!");
        Serial.println("Enter a new bin address (0-11):");
        mode = 1;
      }
    }
    else{
      if (targetPos >= 0 && targetPos < bins + 1) {
        Serial.print("Moving to bin: ");
        Serial.println(targetPos);
        turnToPos(targetPos);  // Move to the specified bin
        Serial.println("Run Machine (Y/N)");
      } else {
        Serial.println("Invalid bin address. Please enter a number between 0 and 11.");
      }
      mode = 0;
    }
  }

}
void turnToPos(int index) {
  index = (index + bins) % bins;  // Wrap index within 0-11

  if (index == startPos) {
    return;
  }

  // Calculate clockwise and counterclockwise distances
  int clockwiseDist = (index - startPos + bins) % bins;
  int counterDist = (startPos - index + bins) % bins;

  // Take the shortest path
  if (clockwiseDist <= counterDist) {
    // Clockwise rotation
    Serial.print("Clockwise Distance: ");
    Serial.println(clockwiseDist);

    digitalWrite(partBinsA, HIGH);
    digitalWrite(partBinsB, LOW);

    int delayTime = timeTo360 * (float(clockwiseDist) / bins);
    delay(delayTime - correctionFactorCW);

    digitalWrite(partBinsA, LOW);
    digitalWrite(partBinsB, LOW);
  } else {
    // Counterclockwise rotation
    Serial.print("Counterclockwise Distance: ");
    Serial.println(counterDist);

    digitalWrite(partBinsB, HIGH);
    digitalWrite(partBinsA, LOW);

    int delayTime = timeTo360 * (float(counterDist) / bins);
    delay(delayTime - correctionFactorCC);

    digitalWrite(partBinsB, LOW);
    digitalWrite(partBinsA, LOW);
  }

  // Update startPos to the new position
  startPos = index;
}
void setMotion(bool state) {
  digitalWrite(belt1, state);
  digitalWrite(twelveVolt, state);
}