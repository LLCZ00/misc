#include "arduino_secrets.h" 
#include <SPI.h>
#include <WiFiNINA.h>
#include <WiFiUdp.h>
#include <Servo.h>

Servo serX;
Servo serY;

int x;
int y;

int status = WL_IDLE_STATUS;
char ssid[] = SECRET_SSID;        
char pass[] = SECRET_PASS;

unsigned int localPort = 2390;      // local port to listen on

char packetBuffer[255]; //buffer to hold incoming packet

WiFiUDP Udp;

void setup() {
  serX.attach(9);
  serY.attach(11);

  serX.write(85);
  serY.write(85); //set servos to look forward
  
  Serial.begin(9600);
  Serial.setTimeout(10);

  // attempt to connect to Wifi network:
  while (status != WL_CONNECTED) {
    Serial.print("Attempting to connect to SSID: ");
    Serial.println(ssid);
    // Connect to WPA/WPA2 network. Change this line if using open or WEP network:
    status = WiFi.begin(ssid, pass);

    // wait 5 seconds for connection:
    delay(5000);
  }
  Serial.println("Connected to wifi");
  printWifiStatus();

  Serial.println("\nAwaiting Data");
  // if you get a connection, report back via serial:
  Udp.begin(localPort);
}

void loop() {

  // if there's data available, read a packet
  int packetSize = Udp.parsePacket();
  if (packetSize) {
    // read the packet into packetBufffer
    int len = Udp.read(packetBuffer, 255);
    if (len > 0) {
      packetBuffer[len] = 0;
    }
    x = map(parseX(packetBuffer), 0, 640, 139, 85);
    y = map(parseY(packetBuffer), 0, 480, 103, 147); 
    //out values need to be calibrated by moving laser to edge of screen and recording coordinates
    /*
     * only required for calibration
    Serial.print("X: ");
    Serial.println(x);
    Serial.print("Y: ");
    Serial.println(y);
    */
    serX.write(x);
    serY.write(y);
  }
}



int parseX(String data) {
  data.remove(data.indexOf('y'));
  data.remove(data.indexOf('x'), 1);

  return data.toInt();
}


int parseY(String data) {
  data.remove(0, data.indexOf('y') + 1);
  
  return data.toInt();
}


void printWifiStatus() {
  // print your board's IP address:
  IPAddress ip = WiFi.localIP();
  Serial.print("IP Address: ");
  Serial.println(ip);
}
