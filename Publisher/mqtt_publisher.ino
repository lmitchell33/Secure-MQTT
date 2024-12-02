#include <WiFi.h>
#include <PubSubClient.h>
#include <WiFiClientSecure.h>

// Certificate contents
const char *CA_CERT = R"(
-----BEGIN CERTIFICATE-----
MIIDazCCAlOgAwIBAgIUEuQPTCFTlxLdr3tFELSiV9gcfBswDQYJKoZIhvcNAQEL
BQAwRTELMAkGA1UEBhMCVVMxCzAJBgNVBAgMAlBBMRMwEQYDVQQHDApQaXR0c2J1
cmdoMRQwEgYDVQQDDAtMTUF1aHRvcml0eTAeFw0yNDEyMDIwNDEzMDNaFw0yNTEy
MDIwNDEzMDNaMEUxCzAJBgNVBAYTAlVTMQswCQYDVQQIDAJQQTETMBEGA1UEBwwK
UGl0dHNidXJnaDEUMBIGA1UEAwwLTE1BdWh0b3JpdHkwggEiMA0GCSqGSIb3DQEB
AQUAA4IBDwAwggEKAoIBAQClOXnj4ueasHAtbrrk1jN9GtGpjuwZoZF+vfb1cy0c
TWzXoi6CFJYBjnh3fzETPN2B2GrGb6rxx71Hw0Vl23VI4/Z8QVGQJmv7dIJz7sQC
HzaLDHVv64S4QOowfSXDw3g7draZlQC2+EjBD4w85e+cv3l2rY2nlJJw7+cT/2iE
lG5A92H8wBrHTX90s4z7mUm8wX4kH6SgkKb++a6Zc0xJEvWQaT5WMkGItPvGUs+8
3aLEnDAiP5JhNhPEpnY4FAfOL6PMjN+2BuYV0DNu11lsIsy4/noC9Xwkgeq+A2hR
nH/NAU/IFn1a6yMyxZ4Wd0jYFAFrtFfhhLsTj717xVMXAgMBAAGjUzBRMB0GA1Ud
DgQWBBSCJEhomcmCO3kFSDi8SOQ/gV6QZzAfBgNVHSMEGDAWgBSCJEhomcmCO3kF
SDi8SOQ/gV6QZzAPBgNVHRMBAf8EBTADAQH/MA0GCSqGSIb3DQEBCwUAA4IBAQCS
+FgLveCSrTyjrPdX8cQT8n5tSsz1YIpZoEL20dzLHZ6rZw1+H/VgUeU4Vql9+I4M
Rf0q7SRrO2fjfIRyjZiDBrUkmNj1nGUzazJZGCwdyz54xU0+m9+VDTvSkhWb4JsR
DIRNk33NIFfw2zngqf4QODTWyKfnrM+y4sZcy8x5zR7cX1+84vVIUaNYwUJP05Rw
hzLpTxkpn0H2fAirJOBcnxu4QPmGNsQN88If4JPZAx9Q9bNJp14FjZEzSKWxWnyu
fOUI5F2t4b6UyeIaKb+VIslVF3tHVHoPHMlW6dyTslMeJWFgvu3kELzyp8xL26Sp
UEGyemML8Bn8l8ngm9LO
-----END CERTIFICATE-----
)";

const char *CLIENT_CERT = R"(
-----BEGIN CERTIFICATE-----
MIIDDzCCAfcCFA9omEYaPYDIcykI4mbJCTyiDb6/MA0GCSqGSIb3DQEBCwUAMEUx
CzAJBgNVBAYTAlVTMQswCQYDVQQIDAJQQTETMBEGA1UEBwwKUGl0dHNidXJnaDEU
MBIGA1UEAwwLTE1BdWh0b3JpdHkwHhcNMjQxMjAyMDQxMzAzWhcNMjUxMjAyMDQx
MzAzWjBDMQswCQYDVQQGEwJVUzELMAkGA1UECAwCUEExEzARBgNVBAcMClBpdHRz
YnVyZ2gxEjAQBgNVBAMMCVB1Ymxpc2hlcjCCASIwDQYJKoZIhvcNAQEBBQADggEP
ADCCAQoCggEBAO1LzRinetKrow3gzFxtlJitDNymGmBPbZDciLfig6kveNH3bijc
CI1lN31yeRto6Q9GsVuVDC6sI+NNsx2WqIredIespRjVz5NLlIb90L65IBLzmsew
o7Au7xORK1kMvVmWtSQoH898/ihGQbi5OvH0e8ZMXwNXFw3yBl77SQ8EWQnU0evp
+KXXAwTXNCDTlbmuGNaPhNWWTkva641Q/J1RspOHRaWvhkzBOhsjuA6GL67Qi6TU
LtaPhtQ9H0y2Og8zby7GejkVa12q3Auop6lpXG3UuL8KBA0iZalQA0hHHG64V3Gf
xElhEO6jwMoDTFwlNbNVOIkvjI8MUjfnbSsCAwEAATANBgkqhkiG9w0BAQsFAAOC
AQEAIzt5liEtI0wnXLttZKiqr1mJkzQ7v70VjbQ+4jrAoVSUHNbKBaSHOb1df5pE
GjEzLzVpD9asNCmhuzkkxKk3z7BJMpS02MYWQdedHQe/yUrWIk3vwFEiUl/MyGW+
8UEhiTHuBblF/lRhJS02GfX/sT9ezPXJVGosGXXX0i7XJ/i+eAPLBZOMJbtgsCf7
ZRnfCVypUSWFplFerhynXYLMi44WNN+jL3Fh2T8v5xYekiM3wJQJFaEEkWmqeodQ
UwFqwRxf6m0ANVzfQa0lKseMn93h/fu4DgKoIUo8Bemsz3S5iOYcEdeBK9buixwD
0P4WBBPP3xpGdfAdeoz2e2eqtg==
-----END CERTIFICATE-----
)";

const char *CLIENT_KEY = R"(
-----BEGIN PRIVATE KEY-----
MIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDtS80Yp3rSq6MN
4MxcbZSYrQzcphpgT22Q3Ii34oOpL3jR924o3AiNZTd9cnkbaOkPRrFblQwurCPj
TbMdlqiK3nSHrKUY1c+TS5SG/dC+uSAS85rHsKOwLu8TkStZDL1ZlrUkKB/PfP4o
RkG4uTrx9HvGTF8DVxcN8gZe+0kPBFkJ1NHr6fil1wME1zQg05W5rhjWj4TVlk5L
2uuNUPydUbKTh0Wlr4ZMwTobI7gOhi+u0Iuk1C7Wj4bUPR9MtjoPM28uxno5FWtd
qtwLqKepaVxt1Li/CgQNImWpUANIRxxuuFdxn8RJYRDuo8DKA0xcJTWzVTiJL4yP
DFI3520rAgMBAAECggEAXJMfavhfvtOOE6p5H6/yclPEukok7SDflk2rGs4IXlcy
U/urIs6gmYT8znh7zdkyXy7Nn3R44bZvc8yKzcbKbw7VOF7+s78qMYUhZz6bEuUH
Ic2euzvqyB+vTptqZV3Gey6D8ZyjuF9DijPKjQXafK1MInMF+DggOuUKXkC7Ylso
A70HoyvuBEndeZMkyRtcbeGejF9zNzx0R3TSag8OBVeluXjChUFotk6ByNyPzn0G
9TYtsSN10i9u4X11+7+YOfu7kcCHtMD5/YGP79v4N/vzXMi56u884hT7W7nsC4KK
Xs0zFGwAccjdz1hJ8FwRuCHjZnqLk/qipOmDPYrYPQKBgQDxEeOZ8Vax26CjHwNv
RZ6Wu2w3uhOLHTzawBqbQU32OZLl3oNlVUZRVgkVrzZRT8qj07hyz55gokumINk7
7rtNqkEVry9crgVAgfWYNdqPNj+UDdV8QT/JcrUAyLTgC7gsoTPFdJp/nyIFgCfl
s7SBajc+4BCqxweggiyylCfPVwKBgQD7/hRhKgE9Pt8mtzykvO1W+PM67izt4hsR
JuHVHypJ/ImgX+b5gDzFUyobJWjL26A9/+ZFC7pVih3ZSsdqLmEDZdK9K4rnwxjz
fPUOeSSzHd5EtJqBozX+F9zn/eKn3ZjQwo2gwYJbvdAgvdQcKcwlZyHcFnBIoBsH
i3KZQYhwTQKBgCrohTt0Ynr73abLMWBP4v9vUr7Ehw/+30MMaG/z+r111/jEV1zl
BcQabTmH20Iz0pzAZZdB7y3CFXb3Z9MsFfin8je629JCQzsNJrq18zYEcOKYZ8Rb
FNB1c1Q1ZURvsZN4Ce/+ZjWLDJIwEmnnR5y1XCn71duf23KtWOlcR423AoGAdCih
OFDmlVbgArbAq6ezOD410Nptt5Jcq8FipJ1jHwvcXSMYE7b7THKTnEPYVPB+o1XM
zdMkJ74tGDcSSW3rpmdPh4gE1eTnIYZeaDeLpU2FYeJmvo9/mgth90bfLkZF5SVp
p8rLzoJm6FDY78qMokkyIIPvamrzSr0LLH466JkCgYBbEecG6PFuzt3c2u9bEpG3
lPGNUh4uqVb2MX3dn/WpEiwW+C/BAH5jAE8Juytco/UQxj1QUUNNfDpZ4Ti12uiA
o/7MtNtIGB2NgUnHil2OHCxLy7jAxm5n10HIjUQMy7VOTEciW38JfoZsr7nHrCPi
jdTX+KRp3e3uGf1vF1sk9g==
-----END PRIVATE KEY-----
)";

const char *WIFI_SSID "Gluten Free";
const char *WIFI_PASSWORD "Miller1821";

const char *MQTT_BROKER "192.168.68.69";
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