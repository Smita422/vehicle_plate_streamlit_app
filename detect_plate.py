import cv2
import easyocr

reader = easyocr.Reader(['en'])

def detect_plate_from_frame(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 100, 200)

    contours, _ = cv2.findContours(edges.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    plate_candidates = []

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        ratio = w / float(h)
        if 2 < ratio < 6 and 100 < w < 500 and 30 < h < 150:
            plate_candidates.append((x, y, w, h))

    for (x, y, w, h) in plate_candidates:
        plate_img = gray[y:y+h, x:x+w]
        result = reader.readtext(plate_img)
        if result:
            text = result[0][1]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, text, (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    return frame
