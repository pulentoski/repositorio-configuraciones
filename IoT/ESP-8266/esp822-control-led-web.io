#if defined(ESP32)
  #include <WiFi.h>
  #include <WebServer.h>
  #include <PubSubClient.h>
#elif defined(ESP8266)
  #include <ESP8266WiFi.h>
  #include <ESP8266WebServer.h>
  #include <PubSubClient.h>
#endif

#include <ArduinoJson.h>

// ------------------ CONFIGURACIÓN ------------------

const char* ssid = "VTR-4264454";
const char* password = "mdfm4rnFnjv4";

const char* mqtt_server = "192.168.0.16";  // IP del servidor ThingsBoard
const int mqtt_port = 1883;
const char* access_token = "6NNhaFPFqaW4HG5VbXWU";

const int ledPin = 2;  // Cambia si usas otro pin
bool ledState = false;

WiFiClient espClient;
PubSubClient client(espClient);

#if defined(ESP32)
  WebServer server(80);
#elif defined(ESP8266)
  ESP8266WebServer server(80);
#endif

// ------------------ FUNCIONES ------------------

String extractRequestId(const char* topic) {
  String t = topic;
  int lastSlash = t.lastIndexOf('/');
  return t.substring(lastSlash + 1);
}

void sendTelemetry() {
  String payload = "{\"led\":";
  payload += (ledState ? "true" : "false");
  payload += "}";
  client.publish("v1/devices/me/telemetry", payload.c_str());
  Serial.println("Telemetría enviada: " + payload);
}

void setLed(bool state) {
  ledState = state;
  digitalWrite(ledPin, ledState ? LOW : HIGH);  // LED activo en bajo
  sendTelemetry();
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("RPC recibido en: ");
  Serial.println(topic);

  StaticJsonDocument<200> doc;
  DeserializationError error = deserializeJson(doc, payload, length);
  if (error) {
    Serial.print("Error al parsear JSON: ");
    Serial.println(error.c_str());
    return;
  }

  const char* method = doc["method"];
  if (method && strcmp(method, "setLED") == 0) {
    bool param = doc["params"];
    setLed(param);

    String requestId = extractRequestId(topic);
    String responseTopic = "v1/devices/me/rpc/response/" + requestId;
    client.publish(responseTopic.c_str(), param ? "true" : "false");
    Serial.println("Respuesta RPC enviada.");
  }
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Conectando a MQTT... ");
    if (client.connect("ESPClient", access_token, NULL)) {
      Serial.println("Conectado.");
      client.subscribe("v1/devices/me/rpc/request/+");
      sendTelemetry();
    } else {
      Serial.print("Fallo. Código: ");
      Serial.print(client.state());
      Serial.println(". Reintentando en 5s...");
      delay(5000);
    }
  }
}

void handleRoot() {
  server.send(200, "text/html", getHTML());
}

void handleOn() {
  setLed(true);
  server.sendHeader("Location", "/");
  server.send(303);
}

void handleOff() {
  setLed(false);
  server.sendHeader("Location", "/");
  server.send(303);
}

String getHTML() {
  String stateText = ledState ? "ENCENDIDO" : "APAGADO";
  String stateColor = ledState ? "#4CAF50" : "#f44336";
  String html = R"====(
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Control de LED</title>
  <style>
    body {
      background: linear-gradient(to right, #1f4037, #99f2c8);
      font-family: 'Segoe UI', sans-serif;
      color: #fff;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      margin: 0;
    }
    .card {
      background-color: rgba(0,0,0,0.4);
      padding: 30px;
      border-radius: 20px;
      box-shadow: 0 10px 25px rgba(0,0,0,0.3);
      text-align: center;
      max-width: 320px;
    }
    h1 {
      margin-bottom: 10px;
      font-size: 24px;
    }
    .status {
      margin: 20px 0;
      padding: 10px;
      font-size: 18px;
      font-weight: bold;
      background-color: )====" + stateColor + R"====(;
      border-radius: 10px;
    }
    .btn {
      display: inline-block;
      padding: 14px 28px;
      font-size: 16px;
      margin: 10px 5px;
      border: none;
      border-radius: 10px;
      cursor: pointer;
      transition: transform 0.2s;
    }
    .btn:hover {
      transform: scale(1.05);
    }
    .on {
      background-color: #4CAF50;
      color: white;
    }
    .off {
      background-color: #f44336;
      color: white;
    }
  </style>
</head>
<body>
  <div class="card">
    <h1>Control de LED</h1>
    <div class="status">Estado: )====" + stateText + R"====(</div>
    <form action="/on" method="POST">
      <button class="btn on">ENCENDER</button>
    </form>
    <form action="/off" method="POST">
      <button class="btn off">APAGAR</button>
    </form>
  </div>
</body>
</html>
)====";
  return html;
}

// ------------------ SETUP Y LOOP ------------------

void setup() {
  Serial.begin(115200);
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, HIGH);  // Inicialmente apagado

  WiFi.begin(ssid, password);
  Serial.print("Conectando a WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi conectado. IP: " + WiFi.localIP().toString());

  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback);

  server.on("/", HTTP_GET, handleRoot);
  server.on("/on", HTTP_POST, handleOn);
  server.on("/off", HTTP_POST, handleOff);
  server.begin();
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
  server.handleClient();
}
