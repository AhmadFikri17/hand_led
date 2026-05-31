int ledPins[5] = {2, 3, 4, 5, 6};

String data = "";

int jumlahJari = 0;

// ======================
// BLINK
// ======================
bool blinkMode = false;
bool ledState = false;

unsigned long lastBlink = 0;
unsigned long holdStart = 0;

int blinkDelay = 500;

void setup() {

  Serial.begin(115200);

  for (int i = 0; i < 5; i++) {
    pinMode(ledPins[i], OUTPUT);
    digitalWrite(ledPins[i], LOW);
  }
}

void loop() {

  // ======================
  // TERIMA DATA SERIAL
  // ======================
  while (Serial.available()) {

    char c = Serial.read();

    if (c == '\n') {

      jumlahJari = data.toInt();

      Serial.print("Terima: ");
      Serial.println(jumlahJari);

      data = "";

      // reset mode blink kalau bukan 5
      if (jumlahJari != 5) {

        blinkMode = false;
        blinkDelay = 500;

        for (int i = 0; i < 5; i++) {

          if (i < jumlahJari)
            digitalWrite(ledPins[i], HIGH);
          else
            digitalWrite(ledPins[i], LOW);
        }
      }

      // jika pertama kali 5
      else {

        if (!blinkMode) {

          blinkMode = true;

          holdStart = millis();

          blinkDelay = 500;

          ledState = true;

          // awal semua nyala dulu
          for (int i = 0; i < 5; i++) {
            digitalWrite(ledPins[i], HIGH);
          }
        }
      }
    }

    else {
      data += c;
    }
  }

  // ======================
  // MODE 5 JARI
  // ======================
  if (blinkMode) {

    unsigned long holdTime = millis() - holdStart;

    // ======================
    // 5 DETIK PERTAMA
    // semua nyala stabil
    // ======================
    if (holdTime < 5000) {

      for (int i = 0; i < 5; i++) {
        digitalWrite(ledPins[i], HIGH);
      }
    }

    // ======================
    // SETELAH 5 DETIK
    // mulai berkedip
    // ======================
    else {

      // semakin lama semakin cepat
      if (holdTime < 10000)
        blinkDelay = 400;

      else if (holdTime < 15000)
        blinkDelay = 250;

      else if (holdTime < 20000)
        blinkDelay = 120;

      else
        blinkDelay = 50;

      // blink
      if (millis() - lastBlink > blinkDelay) {

        lastBlink = millis();

        ledState = !ledState;

        for (int i = 0; i < 5; i++) {
          digitalWrite(ledPins[i], ledState);
        }
      }
    }
  }
}