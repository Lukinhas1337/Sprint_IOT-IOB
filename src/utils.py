import os
import cv2
import numpy as np

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

def read_images_labels(base_dir):
    """
    Espera estrutura base_dir/<label>/<img_files>
    Retorna (faces_list, labels_list, label_to_id)
    """
    faces = []
    labels = []
    label_to_id = {}
    current_id = 0
    for label in sorted(os.listdir(base_dir)):
        folder = os.path.join(base_dir, label)
        if not os.path.isdir(folder):
            continue
        if label not in label_to_id:
            label_to_id[label] = current_id
            current_id += 1
        id_ = label_to_id[label]
        for fname in os.listdir(folder):
            path = os.path.join(folder, fname)
            try:
                img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
                if img is None:
                    continue
                faces.append(img)
                labels.append(id_)
            except Exception:
                continue
    return faces, labels, label_to_id

def get_face_count(label):
    """Retorna a quantidade de faces registradas para um label."""
    import os
    base_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "collected_faces")
    folder = os.path.join(base_dir, label)
    if not os.path.isdir(folder):
        return 0
    return len([f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))])

