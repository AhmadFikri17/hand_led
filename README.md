# Hand Gesture LED Control with ESP32

Sistem deteksi jumlah jari menggunakan MediaPipe dan OpenCV yang terhubung dengan ESP32 melalui komunikasi serial.

Jumlah jari yang terdeteksi akan mengontrol 5 LED pada ESP32:

* 0 jari → Semua LED mati
* 1 jari → LED 1 menyala
* 2 jari → LED 1-2 menyala
* 3 jari → LED 1-3 menyala
* 4 jari → LED 1-4 menyala
* 5 jari → Semua LED menyala dan setelah 5 detik akan berkedip semakin cepat

## Hardware

* ESP32 DevKit V1
* 5x LED
* 5x Resistor 220Ω
* Webcam / Laptop Camera
* Kabel USB

## Wiring

| LED   | GPIO ESP32 |
| ----- | ---------- |
| LED 1 | GPIO 2     |
| LED 2 | GPIO 3     |
| LED 3 | GPIO 4     |
| LED 4 | GPIO 5     |
| LED 5 | GPIO 6     |

Semua LED menggunakan resistor 220Ω dan terhubung ke GND.

## Software Requirements

* Python 3.10+
* Arduino IDE

### Python Libraries

Install seluruh library yang diperlukan:

```bash
pip install opencv-python mediapipe pyserial
```

## Struktur Project

```text
project/
│
├── hand_detection.py
├── esp32_c3Supermini_control.ino
└── README.md
```

## Upload Program ESP32

1. Buka Arduino IDE.
2. Pilih board ESP32 Dev Module.
3. Buka file `esp32_hand_control.ino`.
4. Pilih port ESP32.
5. Upload program.

## Menentukan COM Port

Cek COM port ESP32 pada Device Manager.

Contoh:

```text
USB Serial Device (COM3)
```

Jika berbeda, ubah bagian berikut pada `hand_detection.py`:

```python
ser = serial.Serial('COM3', 115200, timeout=1)
```

Sesuaikan dengan COM port yang digunakan.

## Menjalankan Program Python

Masuk ke folder project:

```bash
cd project
```

Jalankan program:

```bash
python hand_detection.py
```

Jika berhasil akan muncul:

```text
ESP32 terhubung
Kamera aktif
```

## Cara Penggunaan

1. Pastikan ESP32 sudah terhubung ke komputer.
2. Jalankan program Python.
3. Hadapkan tangan ke kamera.
4. Sistem akan mendeteksi jumlah jari yang terbuka.
5. Data jumlah jari dikirim ke ESP32 melalui serial.
6. LED akan menyala sesuai jumlah jari yang terdeteksi.

## Mode Khusus 5 Jari

Saat sistem mendeteksi 5 jari:

* Semua LED menyala stabil selama 5 detik.
* Setelah 5 detik LED mulai berkedip.
* Semakin lama 5 jari dipertahankan, semakin cepat kedipan LED.

## Teknologi yang Digunakan

* OpenCV
* MediaPipe Hands
* Python
* ESP32
* Serial Communication

## Demo

Tambahkan foto atau video demo proyek di bagian ini.

## Author

Ahmad Fikri
