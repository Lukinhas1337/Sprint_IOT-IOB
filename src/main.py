"""
main.py
Demo em tempo real:
- detecta faces (Haar Cascade)
- reconhece (LBPH) se modelo existir
- chama o modelo de risco (sintético) para estimar baixo/médio/alto risco com features simuladas
- permite ajustar scaleFactor e minNeighbors via trackbars para demonstrar impacto
Uso:
    python main.py
"""
import cv2
import joblib
import json
import numpy as np
import os
import tkinter as tk
import subprocess
import time
from tkinter import messagebox
from datetime import datetime
from utils import ensure_dir, get_face_count


CASCADE_PATH = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
MODEL_DIR = "models"
FACE_MODEL_FILE = os.path.join(MODEL_DIR, "face_recognizer.yml")
LABELS_FILE = os.path.join(MODEL_DIR, "labels.json")
RISK_MODEL_FILE = os.path.join(MODEL_DIR, "risk_model.pkl")

def nothing(x):
    pass

def map_scalefactor(val):
    # trackbar gives 105..200 -> maps to 1.05..2.00
    return val / 100.0

def simulate_features_from_frame(face_w, face_h):
    """
    Simula features para o modelo de risco a partir do tamanho da face / tempo.
    Na aplicação real, essas features viriam de histórico de uso/transações.
    """
    # heurística: faces pequenas => usuário mais distante (não relevante), usamos aleatório controlado
    freq = max(0, int(np.clip(face_w/50 + np.random.normal(0,1), 0, 20)))
    avg_deposit = max(1.0, np.abs(np.random.normal(40, 60)))
    session_minutes = max(1.0, np.abs(np.random.normal(45, 30)))
    spikes = int(np.random.rand() < 0.1)
    loss_streak = int(max(0, np.random.poisson(2)))
    return np.array([freq, avg_deposit, session_minutes, spikes, loss_streak]).reshape(1, -1)

def human_label_from_pred(pred):
    return {0: "BAIXO", 1: "MÉDIO", 2: "ALTO"}.get(int(pred), "DESCONHECIDO")

def show_success_window():
    success = tk.Toplevel()  # Cria nova janela
    success.title("Sucesso")
    success.geometry("250x100")
    success.resizable(False, False)

    label = tk.Label(success, text="Login bem-sucedido ✅", font=("Arial", 12))
    label.pack(expand=True)

    ok_button = tk.Button(success, text="OK", width=10, command=success.destroy)
    ok_button.pack(pady=5)

def on_login():
    try:
      if(reconhecimento()):
         show_success_window() 

        

    except subprocess.CalledProcessError:
        messagebox.showerror("Erro", "Erro ao executar o main.py. Verifique o console.")
    except Exception as e:
        messagebox.showerror("Erro inesperado", str(e))

def main():
    root = tk.Tk()
    root.title("Interface de Login")
    root.geometry("400x400")
    root.resizable(False, False)

    frame = tk.Frame(root)
    frame.pack(expand=True)

    login_button = tk.Button(frame, text="Login", width=30, height=4, command=on_login)
    login_button.pack()

    root.mainloop()

def reconhecimento():
    ensure_dir(MODEL_DIR)
    cap = cv2.VideoCapture(0)
    detector = cv2.CascadeClassifier(CASCADE_PATH)

    # carregar recognizer se existir
    recognizer = None
    labels = {}
    if os.path.exists(FACE_MODEL_FILE) and os.path.exists(LABELS_FILE):
        try:
            recognizer = cv2.face.LBPHFaceRecognizer_create()
            recognizer.read(FACE_MODEL_FILE)
            with open(LABELS_FILE, "r", encoding="utf-8") as f:
                labels = {int(k): v for k, v in json.load(f).items()}
            print("Recognizer e labels carregados.")
        except Exception as e:
            print("Falha ao carregar recognizer:", e)

    # carregar risk model se existir
    risk_model = None
    if os.path.exists(RISK_MODEL_FILE):
        risk_model = joblib.load(RISK_MODEL_FILE)
        print("Risk model carregado.")

    # Trackbars window
    win = "Valoriza - Demo"
    cv2.namedWindow(win)
    cv2.createTrackbar("scale(x100)", win, 110, 200, nothing)
    cv2.createTrackbar("minNeighbors", win, 5, 15, nothing)
    cv2.createTrackbar("minSize", win, 60, 300, nothing)

    # Variáveis para login por tempo
    AUTHORIZED_TIME = 5  # segundos necessários de reconhecimento contínuo
    auth_start_time = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        sf_raw = cv2.getTrackbarPos("scale(x100)", win)
        scaleFactor = map_scalefactor(sf_raw)
        minNeighbors = cv2.getTrackbarPos("minNeighbors", win)
        minSizeVal = cv2.getTrackbarPos("minSize", win)
        minSize = (max(20, minSizeVal), max(20, minSizeVal))

        faces = detector.detectMultiScale(gray, scaleFactor=scaleFactor, minNeighbors=max(1, minNeighbors), minSize=minSize)

        info_text = f"scale={scaleFactor:.2f} neighbors={minNeighbors} minSize={minSize[0]}"
        cv2.putText(frame, info_text, (10,20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)

        for (x,y,w,h) in faces:
            cv2.rectangle(frame, (x,y), (x+w,y+h), (0,200,0), 2)
            face_roi = gray[y:y+h, x:x+w]
            try:
                face_resized = cv2.resize(face_roi, (200,200))
            except:
                continue

            label_text = "Desconhecido"
            conf_text = ""
            if recognizer is not None:
                try:
                    label_id, confidence = recognizer.predict(face_resized)
                    if label_id in labels:
                        label_text = labels[label_id]
                    else:
                        label_text = f"id {label_id}"
                    conf_text = f"conf {confidence:.1f}"
                except Exception:
                    label_text = "ErroPredict"

            risk_text = "NAO AUTORIZADO"

            # lógica de login por tempo
            if recognizer is not None and label_text != "Desconhecido" and conf_text:
                try:
                    conf_value = float(conf_text.replace("conf ", ""))

                    if conf_value >= 50:
                        risk_text = "AUTORIZADO"
                        if auth_start_time is None:
                            auth_start_time = time.time()  # início da contagem
                        else:
                            elapsed = time.time() - auth_start_time
                            if elapsed >= AUTHORIZED_TIME:
                                risk_text = "AUTORIZADO"
                                print("Login bem-sucedido para", label_text)
                                cap.release()
                                cv2.destroyAllWindows()
                                return True
                    else:
                        auth_start_time = None
                        risk_text = "NAO AUTORIZADO"
                        print("Login não autorizado para", label_text)

                except Exception:
                    risk_text = "INDEFINIDO"
            elif risk_model is not None:
                Xsim = simulate_features_from_frame(w, h)
                pred = risk_model.predict(Xsim)[0]
                risk_text = human_label_from_pred(pred)

            y_text = y - 10 if y - 10 > 10 else y + h + 20
            cv2.putText(frame, f"{label_text} {conf_text}", (x, y_text), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,255), 2)
            cv2.putText(frame, f" {risk_text}", (x, y_text+20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,128,255), 2)

        cv2.imshow(win, frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        if key == ord('s'):
            ensure_dir("examples")
            fname = f"examples/screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            cv2.imwrite(fname, frame)
            print("Salvou", fname)
    
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
