from flask import Flask, request, jsonify
import torch
from torchvision import transforms, models
from PIL import Image
import cv2
import os
import uuid
import time
from video_utils import extract_faces_from_video


app = Flask(__name__)

# Modeli yükle
MODEL_PATH = "model/deepfake_model.pth"
model = models.resnet50()
model.fc = torch.nn.Linear(model.fc.in_features, 2)
model.load_state_dict(torch.load(MODEL_PATH, map_location=torch.device('cpu')))
model.eval()

# Görsel dönüşüm
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

@app.route('/analyze', methods=['POST'])
def analyze():
    print("✅ Flask API'ye istek geldi.")
    print("🔍 Gelen dosyalar:", request.files)

    if 'video' not in request.files:
        print("❌ 'video' alanı bulunamadı.")
        return jsonify({'error': 'Video dosyası gönderilmedi'}), 400

    video = request.files['video']
    video_filename = f"temp_{uuid.uuid4().hex}.mp4"
    video.save(video_filename)

    try:
        faces = extract_faces_from_video(video_filename)
        if not faces:
            return jsonify({'error': 'Yüz tespit edilemedi'}), 400

        predictions = []
        for face in faces:
            image = Image.fromarray(face)
            input_tensor = transform(image).unsqueeze(0)
            with torch.no_grad():
                output = model(input_tensor)
                prob = torch.softmax(output, dim=1)[0][1].item()
                predictions.append(prob)

        average_confidence = sum(predictions) / len(predictions)
        label = "fake" if average_confidence > 0.5 else "real"

        return jsonify({
            'result': label,
            'confidence': round(average_confidence, 2)
        })

    finally:
        try:
            time.sleep(0.5)
            os.remove(video_filename)
        except Exception as e:
            print(f"[Dosya Silme Hatası] {e}")

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5050, debug=True)
