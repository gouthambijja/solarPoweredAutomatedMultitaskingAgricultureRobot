
#include <ESP8266WiFi.h>
#include <FirebaseArduino.h>
#include "DHT.h"
#define DHTTYPE DHT11

#define DHTPIN D1     
#define FLAMEPIN D2
#define MOTORPUMP D8
// Set these to run example.
#define FIREBASE_HOST "spamar-71800-default-rtdb.firebaseio.com"
#define FIREBASE_AUTH "m18p4HSkzsZ6D3J8YDip5G2EFuryXjGG28Sg7IiN"
#define WIFI_SSID "Goutham"
#define WIFI_PASSWORD "KakaRot@8897139849"

//dht pin
DHT dht(DHTPIN, DHTTYPE);

const int sensor_pin = A0;
int n = 0;

void setup() {
  Serial.begin(9600);
  pinMode(FLAMEPIN,INPUT);
  pinMode(MOTORPUMP,OUTPUT);
  dht.begin();
  // dht.begin();
  // connect to wifi.
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("connecting");
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
  }
  Serial.println();
  Serial.print("connected: ");
  Serial.println(WiFi.localIP());
  
  Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);

  digitalWrite(MOTORPUMP,HIGH);
  //pins
}



void loop() {
  delay(2000);
  float moisture_percentage;
  moisture_percentage = (100.00 - ((analogRead(sensor_pin) / 1023.00) * 100));
  // set value
  if(moisture_percentage <= 25){
    digitalWrite(MOTORPUMP,LOW);
    Serial.println("motor Pump on");
  }
  else{
    digitalWrite(MOTORPUMP,HIGH);
  }
  float humidity_percentage = dht.readHumidity();

  bool flame = !digitalRead(FLAMEPIN);
  Serial.println(flame);
  Firebase.setFloat("kakarotSoilMoisture", moisture_percentage);
  Firebase.setFloat("kakarotHumidity", humidity_percentage);
  Firebase.setBool("kakarotFlame", flame);
  
  // handle error
  if (Firebase.failed()) {
    Serial.print("setting /number failed:");
    Serial.println(Firebase.error());
    return;
  }

  // // update value
  // Firebase.setFloat("number", 43.0);
  // // handle error
  // if (Firebase.failed()) {
  //     Serial.print("setting /number failed:");
  //     Serial.println(Firebase.error());
  //     return;
  // }
  // delay(1000);

  // // get value
  // Serial.print("number: ");
  // Serial.println(Firebase.getFloat("soilmoisture"));
  // delay(1000);

  // // remove value
  // Firebase.remove("number");
  // delay(1000);

  // // set string value
  // Firebase.setString("message", "hello world");
  // // handle error
  // if (Firebase.failed()) {
  //     Serial.print("setting /message failed:");
  //     Serial.println(Firebase.error());
  //     return;
  // }
  // delay(1000);

  // // set bool value
  // Firebase.setBool("truth", false);
  // // handle error
  // if (Firebase.failed()) {
  //     Serial.print("setting /truth failed:");
  //     Serial.println(Firebase.error());
  //     return;
  // }
  // delay(1000);

  // append a new value to /logs
  // String name = Firebase.pushInt("logs", n++);
  // // handle error
  // if (Firebase.failed()) {
  //     Serial.print("pushing /logs failed:");
  //     Serial.println(Firebase.error());
  //     return;
  // }
  // Serial.print("pushed: /logs/");
  // Serial.println(name);
  // delay(1000);
}
