#include "FastLED.h"

// How many leds in your strip?
#define NUM_LEDS 84

#define DATA_PIN 13


// Define the array of leds
CRGB leds[NUM_LEDS];

uint8_t box1[] = {0,1,2,3,4,5,6,7,8};
uint8_t box2[] = {9,10,11,12,13,14,15,16,17};
uint8_t box3[] = {18,19,20,21,22,23,24,25,26};
uint8_t box4[] = {27,28,29,30,31,32,33,34,35};
uint8_t box5[] = {36,37,38,39,40,41,42,43,44};

//-------------     1      2       3       4       5
uint8_t level1[] = {4,     13,     22,     31,     40};
uint8_t level2[] = {3,5,   12,14,   21,23,  30,32,  39,41};
uint8_t level3[] = {2,6,   11,15,   20,24,  29,33,  38,42};
uint8_t level4[] = {1,7,   10,16,   19,25,  28,34,  37,43};
uint8_t level5[] = {0,8,   9,17,    18,26,  27,35,  36,44};
uint8_t numLevels = 5;
CRGB level1Color = CRGB::Red;
CRGB level2Color = CRGB::Orange;
CRGB level3Color = CRGB::Yellow;
CRGB level4Color = CRGB::Green;
CRGB level5Color = CRGB::Green;

void setup() { 
      
  	  FastLED.addLeds<NEOPIXEL, DATA_PIN>(leds, NUM_LEDS);
      
      randomSeed(analogRead(0));

      Serial.begin(115200);
}
void showLevel(int level, char levelBrightness, char brightness)
{
  uint8_t i;
  // Reverse the meaning of brightness to become a reduction
  brightness = 255-brightness;
  levelBrightness = 255-levelBrightness;
  if (level > numLevels)
  {
    level = numLevels;
  }

  // Reset all LEDS to black
  for(i=0;i<NUM_LEDS;i++)
  {
    leds[i] = CRGB::Black;
  }
  
  if(level >= 1)
  {
    for(i=0;i<sizeof(level1);i++)
    {
      
      leds[level1[i]] = level1Color;
      if(level == 1)
      {
        leds[level1[i]].fadeLightBy( brightness );
      }
      else
      {
        leds[level1[i]].fadeLightBy( levelBrightness );
      }
    }
  }
  if(level >= 2)
  {
    for(i=0;i<sizeof(level2);i++)
    {
      
      leds[level2[i]] = level3Color;
      if(level == 2)
      {
        leds[level2[i]].fadeLightBy( brightness );
      }
      else
      {
        leds[level2[i]].fadeLightBy( levelBrightness );
      }
    }
  }
  if(level >= 3)
  {
    for(i=0;i<sizeof(level3);i++)
    {
      
      leds[level3[i]] = level3Color;
      if(level == 3)
      {
        leds[level3[i]].fadeLightBy( brightness );
      }
      else
      {
        leds[level3[i]].fadeLightBy( levelBrightness );
      }
    }
  }
  if(level >= 4)
  {
    for(i=0;i<sizeof(level4);i++)
    {
      
      leds[level4[i]] = level4Color;
      if(level == 4)
      {
        leds[level4[i]].fadeLightBy( brightness );
      }
      else
      {
        leds[level4[i]].fadeLightBy( levelBrightness );
      }
    }
  }
  if(level >= 5)
  {
    for(i=0;i<sizeof(level5);i++)
    {
      
      leds[level5[i]] = level5Color;
      if(level == 5)
      {
        leds[level5[i]].fadeLightBy( brightness );
      }
      else
      {
        leds[level5[i]].fadeLightBy( levelBrightness );
      }
    }
  }
  FastLED.show();
  
}

void showBox(int box, CRGB color)
{
  uint8_t i;
  switch(box)
  {
    case 1:
      for(i=0;i<sizeof(box1);i++)
      {
        leds[box1[i]] = color;
      }
      break;
    case 2:
      for(i=0;i<sizeof(box2);i++)
      {
        leds[box2[i]] = color;
      }
      break;
    case 3:
      for(i=0;i<sizeof(box3);i++)
      {
        leds[box3[i]] = color;
      }
      break;
    case 4:
      for(i=0;i<sizeof(box4);i++)
      {
        leds[box4[i]] = color;
      }
      break;
    case 5:
      for(i=0;i<sizeof(box5);i++)
      {
        leds[box5[i]] = color;
      }
      break;

  }
  FastLED.show();
}
void blackAll(void)
{
  int i;
  for(i=0;i<NUM_LEDS;i++)
  {
    leds[i] = CRGB::Black;
  }
  FastLED.show();
}
void runBox(int brightness)
{
  int i;
  blackAll();
  brightness *= 25;
  for(i=1;i<6;i++)
  {
    CRGB color;
    color[0] = random(brightness);
    color[1] = random(brightness);
    color[2] = random(brightness);
    showBox(i,color);
    delay(1000);
  }
       
}
void runRed()
{
  int i,j;
  for(i=1;i<255;i++)
  {
    for(j=0;j<NUM_LEDS;j++)
    {
      leds[j] = CRGB(i,0,0);
    }
    delay(5); 
    FastLED.show(); 
    
  }
  for(i=255;i>0;i--)
  {
    for(j=0;j<NUM_LEDS;j++)
    {
      leds[j] = CRGB(i,0,0);
    }
    delay(5);
    FastLED.show();
  }
}
void runLevel(int level, int brightness)
{
  brightness *= 25;
  int i,j;
  for(i=1;i<level;i++)
  {
    for(j=1;j<brightness;j+=1)
    {
      showLevel(i,brightness,j);
      delay(2);
    }
  }
  for(i=1;i<4;i++)
  {
    for(j=1;j<255;j+=3)
    {
      showLevel(level,brightness,j);
      delay(10);
    }
    for(j=255;j>0;j-=3)
    {
      showLevel(level,brightness,j);
      delay(10);
    }
  }

  
}
  static char mode = 'r';
  static int param1 = 255;
  static int param2 = 255;
void loop() { 
  // Turn the LED on, then pause
  String str;

  
  str = Serial.readString();
  // Wait for a valid string
  if(str[0])
  {
    switch(str[0])
    {
      case 'b':
        mode = 'b';
        param1 = str[1] - '0';
        break;
      case 'l':
        mode = 'l';
        param1 = str[1]-'0';
        param2 = str[2] - '0';
        break; 
      case 'r':
        mode = 'r';
        break;    
    }  
  }
  // Play the sequence
  Serial.print(mode);
  switch(mode)
  {
    case 'b':
      runBox(param1);
      break;
      
    case 'l':
      runLevel(param1, param2);
      break;
    case 'r':
      runRed();
      
  }
 
}
