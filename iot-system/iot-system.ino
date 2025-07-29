// Library imports
#include <OneWire.h>
#include <DallasTemperature.h>
#include "DFRobot_PH.h"
#include <EEPROM.h>

// Pins and functionality initialization
#define ONE_WIRE_BUS 13
#define PH_PIN A1
#define TURBIDITY_PIN A2
#define TDS_PIN A4

#define TURBIDITY_PIN2 A5

OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);
DFRobot_PH ph;

float tempValue, phValue, turbidityValue, tdsValue, phVoltage, turbidityVoltage, tdsVoltage;

// Program initialization
void setup() {
  Serial.begin(9600);
  sensors.begin();
  ph.begin();
  // ph.calibration(2.6,25); // for calibration only
}

// Main program loop
void loop() {
  // Temp sensor reading
  sensors.requestTemperatures();
  tempValue = sensors.getTempCByIndex(0);

  // pH sensor reading
  static unsigned long timepoint = millis();
  if(millis()-timepoint>1000U){
      timepoint = millis();
      phVoltage = analogRead(PH_PIN) / 1024.0 * 5000;
      phValue = ph.readPH(phVoltage, tempValue) + 3;
  }
  ph.calibration(phVoltage,tempValue);
    
  // TDS sensor reading
  int tdsRaw = analogRead(TDS_PIN);
  tdsVoltage = tdsRaw * (5.0 / 1024.0); // in volts
  tdsValue = (133.42 * tdsVoltage * tdsVoltage * tdsVoltage
              - 255.86 * tdsVoltage * tdsVoltage
              + 857.39 * tdsVoltage) * 0.5;

  // Turbidity Sensor reading
  int turbidityRaw = analogRead(TURBIDITY_PIN);
  turbidityVoltage = turbidityRaw * (5.0 / 1024.0);
  turbidityValue = -10.83 * turbidityVoltage + 41.65;
  if (turbidityValue < 0) turbidityValue = 0;

  // Print stringified JSON results fot python program access
  Serial.print("temp:");
  Serial.print(tempValue);
  Serial.print(",ph:");
  Serial.print(phValue, 2);
  Serial.print(",turbidity:");
  Serial.print(turbidityValue, 2);
  Serial.print(",tds:");
  Serial.println(tdsValue, 2);

  // Program loop delay
  delay(1000);
}