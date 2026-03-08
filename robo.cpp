/*
 * Desk Buddy V1 - Audio Streaming MVP
 * * This code connects an ESP32 to Wi-Fi, listens for a double-tap on a TTP223 touch sensor,
 * and streams 3 seconds of raw I2S audio from an INMP441 microphone to a local Python WebSocket server.
 * * Dependencies:
 * - WebSockets by Markus Sattler (Install via Arduino Library Manager)
 */

#include <WiFi.h>
#include <WebSocketsClient.h>
#include <driver/i2s.h>

// ===================*=======================
// 1. CONFIGURATION (CHANGE THESE)
// ===================*=======================
const char* ssid = "YOUR_WIFI_NAME";
const char* password = "YOUR_WIFI_PASSWORD";

// The local IP address of the computer running the Python server
const char* websocket_server = "192.168.1.3"; 
const int websocket_port = 8000;

// ====================*======================
// 2. PIN DEFINITIONS
// ====================*======================
#define TOUCH_PIN 34 // TTP223 SIG Pin

// INMP441 Microphone Pins
#define I2S_WS 32    // Word Select (L/R Clock)
#define I2S_SCK 25   // Serial Clock
#define I2S_SD 33    // Serial Data

// ===================*=======================
// 3. GLOBAL VARIABLES
// ===================*=======================
WebSocketsClient webSocket;
bool isRecording = false;

// Variables for tap detection
unsigned long lastTapTime = 0;
int tapCount = 0;
const int tapDebounce = 300;     // Minimum ms between taps
const int tapResetTime = 1000;   // Max ms to wait for a second tap before resetting

// ===================*=======================
// 4. I2S MICROPHONE SETUP
// ===================*=======================
void setupI2S() {
  i2s_config_t i2s_config = {
    .mode = (i2s_mode_t)(I2S_MODE_MASTER | I2S_MODE_RX),
    .sample_rate = 16000,                      // 16kHz sample rate for voice
    .bits_per_sample = I2S_BITS_PER_SAMPLE_16BIT,
    .channel_format = I2S_CHANNEL_FMT_ONLY_LEFT, // INMP441 L/R pin tied to GND = Left channel
    .communication_format = I2S_COMM_FORMAT_STAND_I2S,
    .intr_alloc_flags = ESP_INTR_FLAG_LEVEL1,
    .dma_buf_count = 8,
    .dma_buf_len = 64,
    .use_apll = false,
    .tx_desc_auto_clear = false,
    .fixed_mclk = 0
  };
  
  i2s_pin_config_t pin_config = {
    .bck_io_num = I2S_SCK,
    .ws_io_num = I2S_WS,
    .data_out_num = I2S_PIN_NO_CHANGE, // Not transmitting audio out yet
    .data_in_num = I2S_SD
  };
  
  i2s_driver_install(I2S_NUM_0, &i2s_config, 0, NULL);
  i2s_set_pin(I2S_NUM_0, &pin_config);
}

// ==================*========================
// 5. WEBSOCKET EVENT HANDLER
// ===================*=======================
void webSocketEvent(WStype_t type, uint8_t * payload, size_t length) {
  switch(type) {
    case WStype_DISCONNECTED:
      Serial.println("[WS] Disconnected from server!");
      break;
    case WStype_CONNECTED:
      Serial.println("[WS] Connected to Python Server!");
      break;
    case WStype_BIN:
      Serial.println("[WS] Received Audio response from Server! (Playback coming next)");
      break;
  }
}

// =====================*=====================
// 6. MAIN SETUP
// ======================*====================
void setup() {
  Serial.begin(115200);
  pinMode(TOUCH_PIN, INPUT);
  
  // Connect to Wi-Fi
  Serial.print("\nConnecting to WiFi...");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi Connected!");
  Serial.print("ESP32 IP Address: ");
  Serial.println(WiFi.localIP());

  // Initialize Microphone
  setupI2S();

  // Connect to Python WebSocket Server
  webSocket.begin(websocket_server, websocket_port, "/ws");
  webSocket.onEvent(webSocketEvent);
  webSocket.setReconnectInterval(5000); // Try to reconnect every 5s if connection drops
}

// ====================*======================
// 7. MAIN LOOP
// =====================*=====================
void loop() {
  // Keep the WebSocket connection alive
  webSocket.loop();

  // Read the touch sensor
  bool touched = digitalRead(TOUCH_PIN);
  
  // --- Tap Logic ---
  if (touched) {
    // Debounce: ensure enough time has passed since the last tap
    if (millis() - lastTapTime > tapDebounce) { 
      tapCount++;
      lastTapTime = millis();
      Serial.print("Tap detected! Count: "); 
      Serial.println(tapCount);
    }
  }

  // --- Double Tap Detected: Start Recording ---
  if (tapCount >= 2 && !isRecording) {
    Serial.println("Double Tap! Recording 3 seconds of audio...");
    isRecording = true;
    tapCount = 0; // Reset tap counter
    
    size_t bytesRead;
    uint8_t i2sData[1024];
    
    unsigned long recordStartTime = millis();
    
    // Read from mic and send to server for exactly 3 seconds
    while (millis() - recordStartTime < 3000) { 
      // Keep WebSocket alive during the blocking while-loop
      webSocket.loop(); 
      
      // Read raw I2S data from the microphone
      i2s_read(I2S_NUM_0, &i2sData, sizeof(i2sData), &bytesRead, portMAX_DELAY);
      
      // If we got data, send it as binary over the WebSocket
      if (bytesRead > 0) {
        webSocket.sendBIN(i2sData, bytesRead);
      }
    }
    
    Serial.println("Recording finished. Sent to server!");
    isRecording = false;
  }
  
  // --- Reset Tap Counter ---
  // If too much time passes after a single tap, reset the count
  if (millis() - lastTapTime > tapResetTime && tapCount > 0) {
    tapCount = 0;
    Serial.println("Tap timeout. Resetting count.");
  }
}

// Whom to Thanks
//  ---> Yeah its me your BRO[Unless you are a girl] `ARNAB` ;