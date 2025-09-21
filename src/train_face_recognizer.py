"""
train_face_recognizer.py
Treina um LBPHFaceRecognizer a partir de data/collected_faces/<label>/
Salva modelo em models/face_recognizer.yml e um map labels.json
"""
import os
import json
import cv2
import joblib
from utils import read_images_labels, ensure_dir
import numpy as np

# Caminhos absolutos baseados na raiz do projeto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data", "collected_faces")
MODEL_DIR = os.path.join(BASE_DIR, "models")
MODEL_FILE = os.path.join(MODEL_DIR, "face_recognizer.yml")
LABELS_FILE = os.path.join(MODEL_DIR, "labels.json")

def train():
    ensure_dir(MODEL_DIR)
    faces, labels, label_to_id = read_images_labels(DATA_DIR)
    if len(faces) == 0:
        print("Nenhuma imagem encontrada em", DATA_DIR)
        return
    # LBPH requer imagens do mesmo tamanho (sugerimos 200x200)
    faces_resized = [cv2.resize(f, (200,200)) for f in faces]
    faces_np = np.array(faces_resized)
    labels_np = np.array(labels)

    # Criar recognizer LBPH (requer opencv-contrib)
    try:
        recognizer = cv2.face.LBPHFaceRecognizer_create()
    except Exception as e:
        print("Erro ao criar LBPH recognizer. Verifique se 'opencv-contrib-python' está instalado.")
        raise e

    recognizer.train(faces_resized, labels_np)
    recognizer.write(MODEL_FILE)
    # invert mapping para id->label
    id_to_label = {v:k for k,v in label_to_id.items()}
    with open(LABELS_FILE, "w") as f:
        json.dump(id_to_label, f, ensure_ascii=False, indent=2)
    print("Treinamento concluído. Modelo salvo em", MODEL_FILE)
    print("Labels salvos em", LABELS_FILE)

if __name__ == "__main__":
    train()

