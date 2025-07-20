#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <PubSubClient.h>
#include <Adafruit_Sensor.h>
#include <DHT.h>

// === CONFIGURACIÓN ===
#define DHTPIN D4
#define DHTTYPE DHT22

const char* ssid = "VTR-4264454";
const char* password = "mdfm4rnFnjv4";

const char* mqttServer = "192.168.0.16";
const int mqttPort = 1883;
const char* token = "LvK6kHo67utqlwhTqMOX";

DHT dht(DHTPIN, DHTTYPE);
WiFiClient espClient;
PubSubClient mqttClient(espClient);
ESP8266WebServer webServer(80);

float currentTemp = 0.0;
float currentHum = 0.0;
unsigned long lastSend = 0;
String mqttStatus = "Desconectado";

// === HTML PROFESIONAL ===
String buildHTML(float t, float h) {
  String html = R"====(
  <!DOCTYPE html>
  <html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Panel AM2302</title>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
    <style>
      * {
        box-sizing: border-box;
        font-family: 'Roboto', sans-serif;
        margin: 0;
        padding: 0;
      }
      body {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        color: #fff;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        padding: 20px;
      }
      .container {
        background: rgba(255, 255, 255, 0.1);
        padding: 30px 40px;
        border-radius: 16px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.18);
        text-align: center;
        width: 100%;
        max-width: 420px;
      }
      h1 {
        margin-bottom: 20px;
        font-size: 1.8em;
        color: #00d4ff;
      }
      .metric {
        margin: 15px 0;
        font-size: 2.4em;
        font-weight: bold;
        display: flex;
        justify-content: center;
        align-items: baseline;
      }
      .metric span.unit {
        font-size: 0.5em;
        margin-left: 10px;
        opacity: 0.7;
      }
      .info {
        margin-top: 20px;
        font-size: 0.9em;
        color: #cccccc;
        line-height: 1.6em;
      }
      .status {
        margin-top: 10px;
        font-size: 0.95em;
        color: #aaffaa;
      }
    </style>
  </head>
  <body>
    <div class="container">
      <h1>🌐 Panel Sensor AM2302</h1>
      <div class="metric">🌡️ )====" + String(t, 1) + R"====( <span class="unit">°C</span></div>
      <div class="metric">💧 )====" + String(h, 1) + R"====( <span class="unit">%</span></div>
      <div class="info">
        IP Local: )====" + WiFi.localIP().toString() + R"====(<br>
        Estado WiFi: Conectado a )====" + String(ssid) + R"====(<br>
        Estado MQTT: )====" + mqttStatus + R"====(
      </div>
      <div class="status">Actualiza cada 5 segundos</div>
    </div>
    <script>
      setTimeout(() => location.reload(), 5000);
    </script>
  </body>
  </html>
  )====";
  return html;
}

void handleRoot() {
  webServer.send(200, "text/html", buildHTML(currentTemp, currentHum));
}

void reconnectMQTT() {
  while (!mqttClient.connected()) {
    Serial.print("Conectando a ThingsBoard MQTT...");
    if (mqttClient.connect("esp8266-client", token, NULL)) {
      mqttStatus = "Conectado";
      Serial.println("¡Conectado!");
    } else {
      mqttStatus = "Fallo MQTT (rc=" + String(mqttClient.state()) + ")";
      Serial.println("Fallo, rc=" + String(mqttClient.state()) + " intentando en 5s");
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  dht.begin();

  // WiFi
  WiFi.begin(ssid, password);
  Serial.print("Conectando a WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi conectado. IP: " + WiFi.localIP().toString());

  // MQTT
  mqttClient.setServer(mqttServer, mqttPort);
  reconnectMQTT();

  // Web
  webServer.on("/", handleRoot);
  webServer.begin();
  Serial.println("Servidor web iniciado.");
}

void loop() {
  if (!mqttClient.connected()) reconnectMQTT();
  mqttClient.loop();
  webServer.handleClient();

  unsigned long now = millis();
  if (now - lastSend > 5000) {
    lastSend = now;

    float temp = dht.readTemperature();
    float hum = dht.readHumidity();

    if (!isnan(temp) && !isnan(hum)) {
      currentTemp = temp;
      currentHum = hum;

      // Enviar a ThingsBoard
      String payload = "{\"temperature\":" + String(temp, 1) + ",\"humidity\":" + String(hum, 1) + "}";
      Serial.println("Enviando MQTT: " + payload);
      mqttClient.publish("v1/devices/me/telemetry", payload.c_str());
    } else {
      Serial.println("Error leyendo el sensor.");
    }
  }
}
