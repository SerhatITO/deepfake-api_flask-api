import cv2
import gc

def extract_faces_from_video(video_path, max_frames=10):
    faces = []
    face_cascade =cv2.CascadeClassifier("utils/haarcascade_frontalface_default.xml")

    video = cv2.VideoCapture(video_path)
    frame_count = 0

    while frame_count < max_frames:
        ret, frame = video.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        detected = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        for (x, y, w, h) in detected:
            face = frame[y:y+h, x:x+w]
            face_rgb = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
            faces.append(face_rgb)
            break  # sadece ilk yüz

        frame_count += 1

    video.release()
    del video
    gc.collect()  # bellek temizliği

    return faces
