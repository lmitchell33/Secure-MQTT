#include <WiFi.h>
#include <PubSubClient.h>
#include <WiFiClientSecure.h>

// Certificate contents
const char *CA_CERT = R"(
-----BEGIN CERTIFICATE-----
// Your CA certificate here
-----END CERTIFICATE-----
)";

const char *CLIENT_CERT = R"(
-----BEGIN CERTIFICATE-----
// Your client certificate here
-----END CERTIFICATE-----
)";

const char *CLIENT_KEY = R"(
-----BEGIN PRIVATE KEY-----
// Your client private key here
-----END PRIVATE KEY-----
)";

const char *WIFI_SSID "Gluten Free";
const char *WIFI_PASSWORD "Miller1821";

const char *MQTT_BROKER "your_broker_address";
const int MQTT_PORT 8883;
const char *MQTT_USERNAME = "testuser1";
const char *MQTT_PASSWORD = "Soccer0104*23";

WiFiClient pubClient;
PubSubClient mqttClient(pubClient);

void setupWifi()
{
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    while (WiFi.status() != WL_CONNECTED)
    {
        delay(500);
        Serial.print(".");
    }
    Serial.println("Connected")
}

void setupMQTT()
{
    wifiClient.setCACert(CA_CERT);

    wifiClient.setCertificate(CLIENT_CERT);

    wifiClient.setPrivateKey(CLIENT_KEY);

    mqttClient.setServer(MQTT_BROKER, MQTT_PORT);

    mqttClient.setCallback(mqttCallback);
}

void reconnectMQTT()
{
    while (!mqttClient.connected())
    {
        String clientId = "ArduinoClient-" + String(random(0xffff), HEX);

        if (mqttClient.connect(
                clientId.c_str(),
                MQTT_USERNAME,
                MQTT_PASSWORD))
        {
            Serial.println("MQTT connected");
            mqttClient.subscribe("your/topic");
        }
        else
        {
            Serial.print("Failed, rc=");
            Serial.print(mqttClient.state());
            delay(5000);
        }
    }
}

void mqttCallback(char *topic, byte *payload, unsigned int length)
{
    Serial.print("Message arrived [");
    Serial.print(topic);
    Serial.print("] ");
    for (int i = 0; i < length; i++)
    {
        Serial.print((char)payload[i]);
    }
    Serial.println();
}

void setup()
{
    Serial.begin(115200);

    setupWifi();
    setupMQTT();
}

void loop()
{
    if (!mqttClient.connected())
    {
        reconnectMQTT();
    }

    mqttClient.publish("test/sensor", "Hello");

    mqttClient.loop();
    delay(1000);
}