import cv2
import mediapipe as mp
import serial
import time

# =========================
# SERIAL ESP32
# =========================
try:
    ser = serial.Serial('COM3', 115200, timeout=1)
    time.sleep(2)
    print("ESP32 terhubung")
except:
    ser = None
    print("ESP32 tidak terhubung")

# =========================
# KAMERA
# =========================
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

if not cap.isOpened():
    print("Kamera gagal")
    exit()

print("Kamera aktif")

cv2.namedWindow("Hand Detection")

# =========================
# MEDIAPIPE
# =========================
mp_hands = mp.solutions.hands

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    model_complexity=0,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.5
)

mp_draw = mp.solutions.drawing_utils

tip_ids = [4, 8, 12, 16, 20]

last_value = -1

# =========================
# LOOP
# =========================
while True:

    success, img = cap.read()

    if not success:
        continue

    img = cv2.flip(img, 1)

    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    result = hands.process(rgb)

    total_fingers = 0

    if result.multi_hand_landmarks:

        for hand_landmarks in result.multi_hand_landmarks:

            lm_list = []

            h, w, c = img.shape

            for id, lm in enumerate(hand_landmarks.landmark):

                cx = int(lm.x * w)
                cy = int(lm.y * h)

                lm_list.append((cx, cy))

            fingers = []

            # ibu jari
            if lm_list[4][0] < lm_list[3][0]:
                fingers.append(1)
            else:
                fingers.append(0)

            # jari lain
            for i in range(1, 5):

                if lm_list[tip_ids[i]][1] < lm_list[tip_ids[i] - 2][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            total_fingers = fingers.count(1)

            # gambar tangan
            mp_draw.draw_landmarks(
                img,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

    # =========================
    # KIRIM SERIAL
    # =========================
    if ser and total_fingers != last_value:

        try:

            ser.write(f"{total_fingers}\n".encode())

            print("Kirim:", total_fingers)

            last_value = total_fingers

        except Exception as e:

            print("Serial error:", e)

    # =========================
    # TAMPILKAN
    # =========================
    cv2.putText(
        img,
        f'Jari: {total_fingers}',
        (10, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0,255,0),
        2
    )

    cv2.imshow("Hand Detection", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()

cv2.destroyAllWindows()

if ser:
    ser.close()