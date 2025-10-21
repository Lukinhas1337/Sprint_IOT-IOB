# Valoriza – Reconhecimento Facial com Classificação de Risco

## Novidades

- Interface de login via Tkinter: permite autenticação por reconhecimento facial com botão "Login".
- Execução robusta do reconhecimento facial: tratamento de erros na chamada do `main.py` e exibição de janela de sucesso apenas quando o login é bem-sucedido.
- Instruções atualizadas para rodar a interface de login e o reconhecimento facial.


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
- subprocess
- tkinter


## (NOVO) Sistema de Login
Sistema de autenticação por reconhecimento facial integrado à interface gráfica.

### Exemplo de uso

Ao executar:
```powershell
python src/interface_login.py
```
Você verá uma janela como esta:

```
┌─────────────────────────────┐
│  Interface de Login         │
│ ────────────────────────── │
│                             │
│        [ Login ]            │
└─────────────────────────────┘
```

Ao clicar em **Login**, o sistema executa o reconhecimento facial. Se o login for bem-sucedido, aparece:

```
┌─────────────────────────────┐
│        Sucesso              │
│ ────────────────────────── │
│  Login bem-sucedido ✅      │
│        [ OK ]               │
└─────────────────────────────┘
```

Se houver erro (por exemplo, dependência faltando ou falha no reconhecimento), uma mensagem de erro será exibida na interface e detalhes aparecerão no console.

### Fluxo de autenticação
1. Usuário clica em **Login**.
2. O sistema executa `main.py` usando o mesmo Python do ambiente.
3. Se o reconhecimento facial for bem-sucedido (exit code 0), mostra janela de sucesso.
4. Se houver erro, mostra mensagem de erro.

### Dicas de depuração
- Verifique o console para mensagens detalhadas de erro.
- Certifique-se de que todas as dependências estão instaladas no ambiente virtual.
- Se a webcam não for detectada, verifique permissões e drivers.
- Para rodar em ambiente sem interface gráfica, adapte o código para modo headless (sem Tkinter/OpenCV GUI).

### Como usar a interface de login

1. Execute o arquivo de interface:
   ```powershell
   python src/interface_login.py
   ```
2. Clique no botão **Login** para iniciar o reconhecimento facial.
3. Se o reconhecimento for bem-sucedido, uma janela de sucesso será exibida.
4. Se houver erro na execução do reconhecimento, uma mensagem de erro será mostrada.

### Observações técnicas
- O botão de login executa o `main.py` usando o mesmo interpretador Python do ambiente.
- O sistema trata erros de execução e só mostra a janela de sucesso se o processo terminar corretamente.
- É necessário ambiente gráfico para rodar a interface (Tkinter) e o reconhecimento facial (OpenCV com suporte a janelas).

### Dicas de resolução de problemas
- Se aparecer erro de dependência (ex: `ModuleNotFoundError: No module named 'sklearn'`), instale as dependências com:
  ```powershell
  pip install -r requirements.txt
  ```
- Se o OpenCV lançar erro de janela (`NULL window`), verifique se está rodando em ambiente gráfico e se o pacote instalado é `opencv-contrib-python`.

---

Projeto acadêmico da disciplina **IoT & IOB** – Faculdade de Engenharia de Software.  
Parte integrante do **Valoriza – Mentor Financeiro Consciente (XP Inc. Partnership)**.
