"""
train_risk_model.py
Gera dataset sintético de comportamento de apostas e treina um RandomForest
Salva modelo em models/risk_model.pkl
"""
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
import os

MODEL_DIR = "models"
MODEL_FILE = os.path.join(MODEL_DIR, "risk_model.pkl")

def generate_synthetic(n=2000, random_state=42):
    rng = np.random.RandomState(random_state)
    # features: freq_sessions_per_week, avg_deposit, avg_session_minutes, deposit_spikes, loss_streak
    freq = rng.poisson(3, size=n)  # sessões por semana
    avg_deposit = rng.exponential(scale=50, size=n)  # reais por depósito
    session_minutes = rng.normal(loc=40, scale=25, size=n).clip(1)
    spikes = rng.binomial(1, 0.1, size=n) * rng.randint(1,5,size=n)
    loss_streak = rng.poisson(2, size=n)

    X = np.vstack([freq, avg_deposit, session_minutes, spikes, loss_streak]).T

    # regra simples para label: baixo(0), medio(1), alto(2)
    score = 0.4*(freq/10) + 0.3*(avg_deposit/200) + 0.15*(session_minutes/120) + 0.1*(spikes) + 0.2*(loss_streak/10)
    # thresholds
    y = np.digitize(score, [0.08, 0.18])  # 0,1,2
    return X, y

def train_and_save():
    os.makedirs(MODEL_DIR, exist_ok=True)
    X, y = generate_synthetic()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    clf = RandomForestClassifier(n_estimators=150, random_state=42)
    clf.fit(X_train, y_train)
    preds = clf.predict(X_test)
    print(classification_report(y_test, preds))
    joblib.dump(clf, MODEL_FILE)
    print("Modelo de risco salvo em", MODEL_FILE)

if __name__ == "__main__":
    train_and_save()
