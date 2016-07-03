/*
 * Contains the code for interacting with the panel measurement microcontroller
 */


#include <TinyGPS.h>
#include <Wire.h>
#include <SPI.h>
#include <SparkFunLSM9DS1.h>
#include <OneWire.h>

// Create the GPS object
TinyGPS gps;

OneWire  ds(25);  // on pin 10 (a 4.7K resistor is necessary)

// Create the imu object
LSM9DS1 imu;

#define LSM9DS1_M  0x1E // Would be 0x1C if SDO_M is LOW
#define LSM9DS1_AG  0x6B // Would be 0x6A if SDO_AG is LOW

// Earth's magnetic field varies by location. Add or subtract
// a declination to get a more accurate heading. Calculate
// your's here:
// http://www.ngdc.noaa.gov/geomag-web/#declination
#define DECLINATION 5.95 // Declination (degrees) in Grand Rapids,MI


// Teensy has an extra hardware UART, we are using UART2
#define Uart Serial2

void gpsdump(TinyGPS &gps);
void printFloat(double f, int digits = 2);
void(* resetFunc) (void) = 0; //declare reset function @ address 0
void getIMU();
void getTemp();
void printErorr();
void setup()
{
  Serial.begin(115200);
  Uart.begin(9600);
  imu.settings.device.commInterface = IMU_MODE_I2C;
  imu.settings.device.mAddress = LSM9DS1_M;
  imu.settings.device.agAddress = LSM9DS1_AG;

  if (!imu.begin())
  {
    printErorr();
    resetFunc();  //call reset
  }
}

void loop()
{
  bool newdata = false;
  unsigned long start = millis();
  unsigned long fix_age, time, date;

  // Every 5 seconds we print an update
  while (millis() - start < 5000) {
    if (Uart.available()) {
      char c = Uart.read();
      //Serial.print(c);  // uncomment to see raw GPS data
      if (gps.encode(c)) {
        newdata = true;
        // break;  // uncomment to print new data immediately!
      }
    }
  }
  
  if (newdata) {
    gpsdump(gps);
    getIMU();
    getTemp();
  }
  else{
    getIMU();
    getTemp();
  }
}
void printErorr()
{
  Serial.println("{\"error: 1}");
}
void getIMU()
{
  imu.readGyro();
  imu.readAccel();
  imu.readMag();
  
  float roll = atan2(imu.ay, imu.az);
  float pitch = atan2(-imu.ax, sqrt(imu.ay * imu.ay + imu.az * imu.az));
  
  float heading;
  if (imu.my == 0)
    heading = (imu.mx < 0) ? 180.0 : 0;
  else
    heading = atan2(imu.mx, imu.my);
    
  heading -= DECLINATION * PI / 180;
  
  if (heading > PI) heading -= (2 * PI);
  else if (heading < -PI) heading += (2 * PI);
  else if (heading < 0) heading += 2 * PI;
  
  // Convert everything from radians to degrees:
  heading *= 180.0 / PI;
  pitch *= 180.0 / PI;
  roll  *= 180.0 / PI;
  
  Serial.print("{\"pitch\":");
  Serial.print(pitch, 2);
  Serial.print(", ");
  Serial.print("\"roll\":");
  Serial.print(roll, 2);
  Serial.print(", ");
  Serial.print("\"heading\":");
  Serial.print(heading, 2);
  Serial.print("}\n");

}
void getTemp()
{
  byte i;
  byte present = 0;
  byte type_s;
  byte data[12];
  byte addr[8];
  float celsius, fahrenheit;
  static int retries = 0;
  
  if ( !ds.search(addr)) {
    ds.reset_search();
    delay(250);
    retries++;
    if(retries > 5)
    {
      return;
    }
    else
    {
      return getTemp();
    }
  }
  retries = 0;
  
  if (OneWire::crc8(addr, 7) != addr[7]) {
      Serial.println("{\"temp: -1}");
      return;
  }
 
  // the first ROM byte indicates which chip
  switch (addr[0]) {
    case 0x10:
      type_s = 1;
      break;
    case 0x28:
      type_s = 0;
      break;
    case 0x22:
      type_s = 0;
      break;
    default:
      Serial.println("{\"temp: -1}");
      return;
  } 

  ds.reset();
  ds.select(addr);
  ds.write(0x44, 1);        // start conversion, with parasite power on at the end
  
  delay(1000);     // maybe 750ms is enough, maybe not
  // we might do a ds.depower() here, but the reset will take care of it.
  
  present = ds.reset();
  ds.select(addr);    
  ds.write(0xBE);         // Read Scratchpad

  for ( i = 0; i < 9; i++) {           // we need 9 bytes
    data[i] = ds.read();
  }

  // Convert the data to actual temperature
  // because the result is a 16 bit signed integer, it should
  // be stored to an "int16_t" type, which is always 16 bits
  // even when compiled on a 32 bit processor.
  int16_t raw = (data[1] << 8) | data[0];
  if (type_s) {
    raw = raw << 3; // 9 bit resolution default
    if (data[7] == 0x10) {
      // "count remain" gives full 12 bit resolution
      raw = (raw & 0xFFF0) + 12 - data[6];
    }
  } else {
    byte cfg = (data[4] & 0x60);
    // at lower res, the low bits are undefined, so let's zero them
    if (cfg == 0x00) raw = raw & ~7;  // 9 bit resolution, 93.75 ms
    else if (cfg == 0x20) raw = raw & ~3; // 10 bit res, 187.5 ms
    else if (cfg == 0x40) raw = raw & ~1; // 11 bit res, 375 ms
    //// default is 12 bit resolution, 750 ms conversion time
  }
  celsius = (float)raw / 16.0;
  fahrenheit = celsius * 1.8 + 32.0;

  Serial.print("{\"temp\":");
  Serial.print(fahrenheit, 2);
  Serial.print("}\n");
  
}
void gpsdump(TinyGPS &gps)
{
  long lat, lon;
  float flat, flon;
  unsigned long age, date, time, chars;
  int year;
  byte month, day, hour, minute, second, hundredths;
  unsigned short sentences, failed;

  gps.get_position(&lat, &lon, &age);
  gps.get_datetime(&date, &time, &age);
  Serial.print("{\"lat\":");
  Serial.print(lat);
  Serial.print(", ");
  Serial.print("\"long\":");
  Serial.print(lon);
  Serial.print(", ");
  Serial.print("\"date\":");
  Serial.print(date);
  Serial.print(", ");
  Serial.print("\"time\":");
  Serial.print(time);
  Serial.print("}\n");
}

void printFloat(double number, int digits)
{
  // Handle negative numbers
  if (number < 0.0) {
     Serial.print('-');
     number = -number;
  }

  // Round correctly so that print(1.999, 2) prints as "2.00"
  double rounding = 0.5;
  for (uint8_t i=0; i<digits; ++i)
    rounding /= 10.0;
  
  number += rounding;

  // Extract the integer part of the number and print it
  unsigned long int_part = (unsigned long)number;
  double remainder = number - (double)int_part;
  Serial.print(int_part);

  // Print the decimal point, but only if there are digits beyond
  if (digits > 0)
    Serial.print("."); 

  // Extract digits from the remainder one at a time
  while (digits-- > 0) {
    remainder *= 10.0;
    int toPrint = int(remainder);
    Serial.print(toPrint);
    remainder -= toPrint;
  }
}
