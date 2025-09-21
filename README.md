# Valoriza – Reconhecimento Facial com Classificação de Risco

Este projeto demonstra **reconhecimento facial em tempo real** usando **OpenCV** e classifica o **risco do usuário reconhecido** com base na **confiabilidade da verificação facial**.  
Ele faz parte do trabalho **IoT & IOB** (Case: Apostas Compulsivas) e é um módulo local do projeto **Valoriza – Mentor Financeiro Consciente**, que visa monitorar comportamentos de risco e promover decisões financeiras mais saudáveis.

## Estrutura do Projeto

```
├── dataset/                       # Imagens capturadas (faces de cada pessoa)
│   └── <id>/
├── models/
│   ├── face_recognizer.yml         # Modelo facial treinado (LBPH)
│   ├── labels.json                 # Mapeamento ID ↔ Nome
│   └── risk_model.pkl              # Modelo opcional de risco sintético
├── src/
│   ├── capture_faces.py            # Captura faces da webcam
│   ├── train_face_recognizer.py    # Treina o modelo facial
│   ├── train_risk_model.py         # (Opcional) Treina modelo de risco sintético
│   ├── main.py                     # Reconhecimento facial em tempo real
│   └── utils.py                    # Funções utilitárias
├── requirements.txt
└── README.md
```

## Instalação

1. **Crie e ative um ambiente virtual (Windows PowerShell):**
   ```powershell
   python -m venv .venv
   & .venv\Scripts\Activate.ps1
   ```

2. **Instale as dependências:**
   ```powershell
   pip install -r requirements.txt
   ```

## Uso

### 1. Capturar faces
Capture imagens do usuário a partir da webcam:
```powershell
python src/capture_faces.py --id NOME_USUARIO --num 30
```
- Pressione **barra de espaço** para salvar cada foto.
- Pressione **q** para sair a qualquer momento.

### 2. Treinar o modelo facial
Treine o reconhecedor LBPH com as imagens capturadas:
```powershell
python src/train_face_recognizer.py
```

### 3. (Opcional) Treinar o modelo de risco
Cria um modelo sintético para demonstração de classificação de risco:
```powershell
python src/train_risk_model.py
```

### 4. Executar o reconhecimento facial
Inicia a detecção e identificação em tempo real:
```powershell
python src/main.py
```

## Como funciona a classificação de risco
- O **risco** é derivado da **confiabilidade do reconhecimento facial** (valor `confidence` do LBPH):
  - **Baixo risco**  → confiança < 50  
  - **Médio risco** → confiança < 80  
  - **Alto risco**  → confiança ≥ 80  
- Quanto **maior o valor de confiança**, **menor a certeza** do modelo, portanto maior o risco.

## Contexto do Projeto (Case IoT & IOB)
- **Problema**: o crescimento das apostas compulsivas gera riscos financeiros e sociais.
- **Solução Valoriza**: um mentor financeiro inteligente que:
  - Monitora comportamentos de risco em tempo real.
  - Fornece alertas e orientações personalizadas.
  - Explica suas decisões usando técnicas de IA explicável (XAI).
- Este módulo **não coleta dados financeiros reais**: serve apenas para demonstrar a captura, verificação facial e cálculo de risco em um ambiente local.

## Parâmetros importantes
- **scaleFactor** (Haar Cascade): ajuste a sensibilidade da detecção de face.
- **minNeighbors**: reduz falsos positivos.
- **LBPH parameters**: podem ser ajustados em `train_face_recognizer.py` para testar impacto.

## Ética e LGPD
- Imagens faciais são **dados biométricos sensíveis**.
- **Use apenas com consentimento** dos participantes.
- Os datasets de teste devem ser sintéticos ou licenciados (CC0/CC BY).
- O código é aberto sob licença **MIT**.

## Requisitos
- Python 3.10+
- OpenCV (`opencv-contrib-python`)
- scikit-learn
- joblib
- numpy, pandas

---

Projeto acadêmico da disciplina **IoT & IOB** – Faculdade de Engenharia de Software.  
Parte integrante do **Valoriza – Mentor Financeiro Consciente (XP Inc. Partnership)**.
