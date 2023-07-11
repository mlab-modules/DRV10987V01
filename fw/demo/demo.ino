

// KV = 0.00358

#include <Wire.h>

int led = 13;         // the PWM pin the LED is attached to
int brightness = 0;  // how bright the LED is
int fadeAmount = 5;  // how many points to fade the LED by

#define ADDR_DRV 0b1010010
#define ADDR_DRV_W 0b1010011



#define Fault_Reg 0x00 //
#define MotorSpeed_Reg 0x01 //
#define DeviceIDRevisionID_Reg 0x08
#define EEPROM_Access_Code_Reg 0x31
#define EEPROM_EeReady_Reg 0x32
#define EEPROM_Iindividual_Access_Adr_Reg 0x33
#define EEPROM_Individual_Access_Write_Data_Reg 0x34
#define EEPROM_Access_Reg 0x35
#define EECTRL_Reg 0x60


// Funkce pro zápis dvou bytů do registru I2C zařízení
void writeTwoBytes(uint8_t reg, uint8_t data1, uint8_t data2) {
  Wire.beginTransmission(ADDR_DRV);
  Wire.write(reg);     // Adresa registru
  Wire.write(data1);   // První byte dat
  Wire.write(data2);   // Druhý byte dat
  Wire.endTransmission();
}

// Funkce pro čtení dvou bytů z registru I2C zařízení
void readTwoBytes(uint8_t reg, uint8_t& data1, uint8_t& data2) {
  Wire.beginTransmission(ADDR_DRV);
  Wire.write(reg);     // Adresa registru
  Wire.endTransmission();

  Wire.requestFrom(ADDR_DRV, 2);  // Požadavek na čtení dvou bytů

  if (Wire.available() >= 2) {
    data1 = Wire.read();   // První byte dat
    data2 = Wire.read();   // Druhý byte dat
  }
}


uint16_t read_twoByte(int address, unsigned char r){
  Wire.beginTransmission(address);
  Wire.write(r);
  Wire.endTransmission(false);
  Wire.requestFrom(address, 2);
  unsigned int lsb, msb;
  if (Wire.available() >= 2){
    msb = Wire.read();
    lsb = Wire.read();
  }
  //Wire.endTransmission(false);
  return ((msb << 8) | lsb);
}

void write_twoByte(int address, unsigned char r, uint16_t data){
  uint16_t begin = 0;
  begin = read_twoByte(address, r);
  delay(1);

  Wire.beginTransmission(address);
  Wire.write(r);
  Wire.write((data >> 8) & 0xFF); // LSB
  Wire.write(data & 0xFF);
  Wire.endTransmission(true);
  
  delay(1);
  uint16_t end = 0;
  end = read_twoByte(address, r);
  Serial.printf("reg 0x%04X: 0x%04X -> 0x%04X -> 0x%04X \r\n", r, begin, data, end);
}

  uint16_t i = 0;


// the setup routine runs once when you press reset:
void setup() {

  // declare pin 9 to be an output:
  pinMode(led, OUTPUT);
  Wire.begin();        // join i2c bus (address optional for master)
  Wire.setClock(100000);

  Serial.begin(115200);
  Serial.println("Hello!");


  Serial.println("EEPROM PROG");
  write_twoByte(ADDR_DRV, 0x35, 0b0001000000000000);    // EEPROM SHADOW


  Serial.println(".......");


  uint16_t CFG1 = 0;

  CFG1 |= 0b0111010; // RMShift, RMValue - Motor phase resistance 0.8 Ohm
  CFG1 |= 0b1 << 7; // Half-cycle adjust
  CFG1 |= 7 << 8;  // Pocet polu motoru
  CFG1 |= 0b00 << 12; // FG open-loop select
  CFG1 |= 0b11 << 14; // Spead spctrum modulation control
  
  write_twoByte(ADDR_DRV, 0x90, CFG1);



  uint16_t CFG2 = 0;
  CFG2 |= 0x6c; // 4, comutation advance value
  CFG2 |= 0b0 << 7; // Commutation advance mode
  CFG2 |= 0b0011000 << 8; // Kt value 
  write_twoByte(ADDR_DRV, 0x91, CFG2);


  uint16_t CFG3 = 0;
  CFG3 |= 0b000; // Braking mode
  CFG3 |= 0b000 << 3; // Open-loop rampup
  CFG3 |= 0b10 << 6; // Open-loop current
  CFG3 |= 0b00 << 8;
  CFG3 |= 0b0 << 10;
  CFG3 |= 0b0 << 11;
  CFG3 |= 0b1 << 12; // Hysteresis for BEMF
  write_twoByte(ADDR_DRV, 0x92, CFG3);


  uint16_t CFG4 = 0;
  CFG4 |= 0b111; // algin time
  CFG4 |= 0b11111 << 3; // Open to close loop
  CFG4 |= 0b011 << 8;
  CFG4 |= 0b0 << 11;
  CFG4 |= 1 << 14; //  Accel range selection
  write_twoByte(ADDR_DRV, 0x93, CFG4);


  uint16_t CFG5 = 0;
  CFG5 |= 0b1;
  CFG5 |= 0b000 << 1;  // HW current limit 
  CFG5 |= 0b010 << 4;   // SW current limit
  CFG5 |= 0b000000 << 8; // Lock5 - LOCK0
  CFG5 |= 0b01 << 14; // Limit current when overtemp
  write_twoByte(ADDR_DRV, 0x94, CFG5);


  uint16_t CFG6 = 0;
  CFG6 |= 0b10;
  CFG6 |= 0b11 << 2;
  CFG6 |= 0b100 << 4;
  CFG6 |= 0b1 << 7; // Transfer to Open-loop
  CFG6 |= 0b1 << 8; // Hi-z
  CFG6 |= 0b11 << 12; // KT detect threshold
  write_twoByte(ADDR_DRV, 0x95, CFG6);

  //write_twoByte(ADDR_DRV, 0x92, 0b1010000);
  //write_twoByte(ADDR_DRV, 0x92, 0b0000000100000000);

  //write_twoByte(ADDR_DRV, 0x93, 0b1101110001010);
  //write_twoByte(ADDR_DRV, 0x93, 0b000000100001011);

 // write_twoByte(ADDR_DRV, 0x94, 0b11111110101111);
  //write_twoByte(ADDR_DRV, 0x94, 0b000000000000110);

  //write_twoByte(ADDR_DRV, 0x95, 0b11000101110111);
  //write_twoByte(ADDR_DRV, 0x95, 0b11110101000011);

  write_twoByte(ADDR_DRV, 0x96, 0b101101010);
  //write_twoByte(ADDR_DRV, 0x96, 0b101100010);
  



  Serial.println("......................");

  //Serial.println("CONFIG1");
  //write_twoByte(ADDR_DRV, 0x90, 0x003A);

  Serial.println("IPDPos, VoltageSupply");
  write_twoByte(ADDR_DRV, 0x05, 0x0067);  // 0x0067 - 12V


  Serial.println("Current");
  //write_twoByte(ADDR_DRV, 0x04, 0x015);
  delay(100);



  Serial.println("SPEED");
  write_twoByte(ADDR_DRV, 0x30, 0x8003);
}

// the loop routine runs over and over again forever:
void loop() {
  i += 1;
  //Serial.println(i);
  // set the brightness of pin 9:
  analogWrite(led, brightness);

  // change the brightness for next time through the loop:
  brightness = brightness + fadeAmount;

  // reverse the direction of the fading at the ends of the fade:
  if (brightness <= 0 || brightness >= 255) {
    fadeAmount = -fadeAmount;
  }
  // wait for 30 milliseconds to see the dimming effect
  delay(30);


  uint16_t val = read_twoByte(ADDR_DRV, 0x00);
  Serial.println(val, BIN);
  write_twoByte(ADDR_DRV, 0x00, 0xffff);

  // uint16_t current = read_twoByte(ADDR_DRV, 0x04);
  // if(current >= 1023){
  //   current -= 1023;
  // }
  // current = 3*current/512;
  // Serial.println(current);

  Serial.println(read_twoByte(ADDR_DRV, 0x06), HEX);

    write_twoByte(ADDR_DRV, 0x30, 0x8001);


  //write_twoByte(ADDR_DRV, 0x35, 0b0001000000000000);    // EEPROM SHADOW

  //write_twoByte(ADDR_DRV, 0x30, 0x101);





}
