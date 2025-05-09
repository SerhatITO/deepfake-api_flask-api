with open("/mnt/data/README_flask_api.md", "w", encoding="utf-8") as f:
    f.write("""# 🧠 Deepfake Detection - Flask API

Bu proje, derin öğrenme tabanlı bir model kullanarak yüklenen videolardaki yüzleri analiz eder ve videonun sahte (deepfake) mi yoksa gerçek mi olduğunu tahmin eder. Python ve Flask kullanılarak geliştirilmiştir.

## 🚀 Özellikler

- Flask tabanlı API
- .mp4 uzantılı video dosyaları üzerinden analiz
- ResNet50 tabanlı eğitimli PyTorch modeli kullanır
- Yüz tespiti için OpenCV `haarcascade` modeli
- Sonuç olarak gerçek/sahte etiketi ve güven skoru döndürür

## 📁 Proje Yapısı

deepfake-api_flask-api/
│
├── app.py # Flask API'nin ana dosyası
├── video_utils.py # Videodan yüz çıkarımı yapan yardımcı modül
├── model/
│ └── deepfake_model.pth # Eğitimli PyTorch modeli
├── utils/
│ └── haarcascade_frontalface_default.xml # Yüz tespiti için haarcascades modeli
├── README.md # Bu belge

## ▶️ Çalıştırmak için

1. Gerekli kütüphaneleri yükleyin:

```bash
pip install flask torch torchvision pillow opencv-python
app.py dosyasını başlatın:

python app.py
API http://127.0.0.1:5050 adresinde çalışacaktır.