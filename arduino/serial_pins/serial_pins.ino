// This is a workaround for a build error
extern "C"{
  int _getpid(){ return -1;}
  int _kill(int pid, int sig){ return -1; }
  int _write(){return -1;}
}

void setup() { // code run once
  Serial.begin(9600);
  Serial.println("<Arduino is ready>");
}

int outputVoltageOn = 255; // 3.3V
int outputVoltageOff = 0;
const byte stringLength = 32;
char stringBuffer[stringLength];
boolean newData = false;

void loop() {
  recieveBuffer();
  respond();
  newData = false;
}

void recieveBuffer() {
  static byte index = 0;
  char endMarker = '\n';
  char currentCharacter;

  while (Serial.available() > 0 && newData == false) {
    currentCharacter = Serial.read();
  
    if (currentCharacter != endMarker) {
      stringBuffer[index] = currentCharacter;
      ++index;

      // truncates strings > stringLength
      if (index >= stringLength) index = stringLength - 1;
    } else {
      stringBuffer[index] = '\0';
      index = 0;
      newData = true;
    }
  }
}

void read(int pinNum) {
  Serial.println(analogRead(pinNum));
}

void write(int pinNum, int status) {
  if (status) {
    analogWrite(pinNum, outputVoltageOn);
    read(pinNum);
  } else {
    analogWrite(pinNum, outputVoltageOff);
    read(pinNum);
  }
}

void respond() {
  if (newData == true) {
    char command = stringBuffer[0];

    char pinStr[3] = {stringBuffer[1], stringBuffer[2], '\0'};
    int pin = atoi(pinStr);

    if (pin > 26) {
      Serial.println("ERROR: Pin number out of range");
      return;
    }

    int status = stringBuffer[3];

    switch (command) {
      case 'r': // read
        read(pin);
        break;
      case 'w': // write
        write(pin, status);
        break;
      default:
        Serial.println("ERROR: Invalid input");
        break;
    }
  }
}

void printBuffer() {
  if (newData == true) {
    Serial.println(stringBuffer);
  }
}

void echo() {
  Serial.println(Serial.read());
}