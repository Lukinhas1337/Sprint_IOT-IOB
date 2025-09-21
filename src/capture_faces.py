"""
capture_faces.py
Uso:
    python capture_faces.py --id NOME --num 50
Salva imagens em data/collected_faces/<id>/
"""
import argparse
import cv2
import os
from utils import ensure_dir

CASCADE_PATH = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"

def main(person_id, num_images, output_dir):
    ensure_dir(output_dir)
    person_dir = os.path.join(output_dir, str(person_id))
    ensure_dir(person_dir)

    cap = cv2.VideoCapture(0)
    detector = cv2.CascadeClassifier(CASCADE_PATH)
    count = 0

    print("Pressione 'q' para sair. Capturando faces...")
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(60,60))
        for (x,y,w,h) in faces:
            cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
        cv2.putText(frame, f"Coletadas: {count}/{num_images}", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0),2)
        cv2.imshow("Capture Faces - Pressione espaço para salvar", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        if key == ord(' '):  # espaço para salvar a face detectada
            if len(faces) == 0:
                print("Nenhuma face detectada — posicione melhor e tente novamente.")
                continue
            # pega a maior face
            faces_sorted = sorted(faces, key=lambda r: r[2]*r[3], reverse=True)
            x,y,w,h = faces_sorted[0]
            face_img = gray[y:y+h, x:x+w]
            face_resized = cv2.resize(face_img, (200,200))
            fname = os.path.join(person_dir, f"{count:03d}.png")
            cv2.imwrite(fname, face_resized)
            count += 1
            print(f"Salvou {fname}")
            if count >= num_images:
                print("Número requerido de imagens coletadas.")
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", required=True, help="ID/nome da pessoa")
    parser.add_argument("--num", type=int, default=50, help="Número de fotos a coletar")
    parser.add_argument("--out", default="data/collected_faces", help="Pasta para salvar imagens")
    args = parser.parse_args()
    main(args.id, args.num, args.out)

