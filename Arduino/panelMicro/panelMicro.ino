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

// Function prototypes
void gpsdump(TinyGPS &gps);
void printFloat(double f, int digits = 2);
void(* resetFunc) (void) = 0; //declare reset function @ address 0
void getIMU();
void getTemp();
void printError();



// Arduino setup function
void setup()
{
  // Start the serial connection between the micro and the Raspberry Pi
  Serial.begin(115200);

  // Start the serial communication to the GPS module
  Uart.begin(9600);

  // Setup the I2C connection the IMU
  imu.settings.device.commInterface = IMU_MODE_I2C;
  imu.settings.device.mAddress = LSM9DS1_M;
  imu.settings.device.agAddress = LSM9DS1_AG;

  // If the IMU is unable to start, print an error and call a SW reset
  if (!imu.begin())
  {
    printError();
    resetFunc();  //call reset
  }
}

// Arduino loop code
void loop()
{
  // Variable to hold whether or not there is new data from the GPS
  bool newdata = false;

  // Track the start of the wait cycle
  unsigned long start = millis();

  // Every 5 seconds we print an update
  while (millis() - start < 5000) {
    // If there is serial data available, read it and send it to the gps library
    if (Uart.available()) {
      char c = Uart.read();
      // If the encode process returned that there is new data, let the rest of
      // the function know
      if (gps.encode(c)) {
        newdata = true;
      }
    }
  }

  // If there is new data from the library, print it out
  if (newdata) {
    // Dump the GPS data
    gpsdump(gps);

    // Dump the IMU data
    getIMU();

    // Dump the temperature sensor
    getTemp();
  }
  else{
    // Dump the IMU data
    getIMU();

    // Dump the temperature data
    getTemp();
  }
}

// Print an error if there is something wrong with initialization
void printError()
{
  Serial.println("{\"error: 1}");
}


// Get the data from the IMU
void getIMU()
{
  // Read the Gyrometer
  imu.readGyro();

  // Read the Accelerometer
  imu.readAccel();

  // Read the Magnetometer
  imu.readMag();

  // Compute the roll and pitch from the imu data
  float roll = atan2(imu.ay, imu.az);
  float pitch = atan2(-imu.ax, sqrt(imu.ay * imu.ay + imu.az * imu.az));

  // Apply Magnetometer offset
  imu.mx-=955;
  imu.my-=1392;
  imu.mz+=594;

  // Compute the heading from IMU data
  float heading;
  if (imu.my == 0)
    heading = (imu.mx < 0) ? 180.0 : 0;
  else
    heading = atan2(imu.mx, imu.my);

  // Offset heading by the declination
  heading -= DECLINATION * PI / 180;

  // Format the heading based on a 0-360 degree representation of the compass
  if (heading > PI) heading -= (2 * PI);
  else if (heading < -PI) heading += (2 * PI);
  else if (heading < 0) heading += 2 * PI;

  // Convert everything from radians to degrees:
  heading *= 180.0 / PI;
  pitch *= 180.0 / PI;
  roll  *= 180.0 / PI;

  // Print out the IMU data to
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

// Process the temperature sensor data
void getTemp()
{
  byte i;
  byte present = 0;
  byte type_s;
  byte data[12];
  byte addr[8];
  float celsius, fahrenheit;
  static int retries = 0;

  // If a Temp sensor can't be found, call this function recursively.
  // A counter variable makes sure that the function doesn't get stuck in a loop
  if ( !ds.search(addr)) {
    // Restart the search for a DS temp sensor
    ds.reset_search();
    delay(250);
    retries++;
    if(retries > 5)
    {
      // If the retries are exhausted, return from the function
      return;
    }
    else
    {
      // If there are more tries left, run the function recursively
      return getTemp();
    }
  }
  // Reset the amount of retries available once a device is found
  retries = 0;

  // Verify that the address CRC matches the computed CRC
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

  // Reset the onewire library
  ds.reset();

  // Instruct the library to select the found device
  ds.select(addr);
  ds.write(0x44, 1);        // start conversion, with parasite power on at the end

  // wait for the conversion to finish
  delay(1000);

  // Reset the library
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
  // Handle different types of sensors
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
  // Convert raw count to C and F
  celsius = (float)raw / 16.0;
  fahrenheit = celsius * 1.8 + 32.0;

  // Report the results
  Serial.print("{\"temp\":");
  Serial.print(fahrenheit, 2);
  Serial.print("}\n");
}

// Handle the GPS data
void gpsdump(TinyGPS &gps)
{
  long lat, lon;
  float flat, flon;
  unsigned long age, date, time, chars;
  int year;
  byte month, day, hour, minute, second, hundredths;
  unsigned short sentences, failed;

  // Get the position from the library
  gps.get_position(&lat, &lon, &age);

  // Get the date and time from the library
  gps.get_datetime(&date, &time, &age);

  // Print the results of the GPS acquisition
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
