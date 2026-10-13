# 🚀 WhatsApp Automation with Selenium

Automação de envio de mensagens no WhatsApp Web utilizando **Python + Selenium**, com suporte para múltiplos contatos e manutenção de sessão/login.

---

## 📌 Funcionalidades

- Envio automático de mensagens pelo WhatsApp Web
- Suporte para múltiplos números
- Persistência de login com perfil do Chrome
- Estrutura simples e fácil de modificar
- Base pronta para expansão com:
  - envio de imagens
  - envio de arquivos
  - integração com planilhas
  - automações com PyAutoGUI
  - migração futura para Playwright

---

## 🛠️ Tecnologias utilizadas

- Python 3
- Selenium
- ChromeDriver
- PyAutoGUI *(opcional para automações complementares)*

---

## 📂 Estrutura do projeto

```bash
project_zap/
│
├── .env.example
├── .gitignore
├── .python-version
├── README.md
├── main.py
├── whatsapp_service.py
├── contatos_excel.py
└── .venv/
```

---

## ⚙️ Instalação

### 1️⃣ Clone o repositório

```bash
git clone https://github.com/seu-usuario/project_zap.git
```

---

### 2️⃣ Acesse a pasta do projeto

```bash
cd project_zap
```

---

### 3️⃣ Crie o ambiente virtual

Usando `uv`:

```bash
uv venv
```

Ative o ambiente:

#### Linux/macOS

```bash
source .venv/bin/activate
```

#### Windows

```bash
.venv\Scripts\activate
```

---

### 4️⃣ Instale as dependências

```bash
uv pip install selenium pyautogui
```

ou

```bash
pip install selenium pyautogui
```

---

## ▶️ Como executar

```bash
python main.py
```

Na primeira execução:

- O Chrome será aberto
- Faça login no WhatsApp Web via QR Code
- O perfil será salvo automaticamente

---

## 📱 Exemplo de código

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Lista de números com DDI + DDD + número
numeros = [
    "5581999999999",
    "5581988888888"
]

mensagem = "Olá! Mensagem automática via WhatsApp."

# Configuração do Chrome
options = webdriver.ChromeOptions()
options.add_argument("--user-data-dir=./profile")

driver = webdriver.Chrome(options=options)

def enviar_mensagem(numero):
    link = f"https://wa.me/{numero}"

    driver.get(link)

    time.sleep(3)

    try:
        botao_abrir = driver.find_element(
            By.XPATH,
            '//a[contains(@href,"web.whatsapp.com/send")]'
        )

        botao_abrir.click()

        time.sleep(5)

        caixa_mensagem = driver.find_element(
            By.XPATH,
            '//div[@contenteditable="true"][@data-tab="10"]'
        )

        caixa_mensagem.send_keys(mensagem)
        caixa_mensagem.send_keys(Keys.ENTER)

        print(f"Mensagem enviada para {numero}")

    except Exception as e:
        print(f"Erro ao enviar para {numero}: {e}")

for numero in numeros:
    enviar_mensagem(numero)

driver.quit()
```

---

## 🔥 Melhorias futuras

- [ ] Migração para Playwright
- [ ] Interface gráfica com CustomTkinter
- [ ] Integração com Excel/CSV
- [ ] Agendamento de mensagens
- [ ] Dashboard de envio
- [ ] Sistema de logs
- [ ] Retry automático
- [ ] Envio de imagens e PDFs

---

## ⚠️ Aviso

Este projeto é apenas para fins educacionais e automação pessoal.

O uso excessivo pode violar os termos de uso do WhatsApp.

Use com responsabilidade.

---

## 👨‍💻 Autor

### Robert Fernandes de Melo

- Python Developer
- Automação de processos
- Web Scraping
- Data Science & IA

#### GitHub

```txt
https://github.com/seu-usuario
```

#### LinkedIn

```txt
https://linkedin.com/in/seu-link
```

---

## ⭐ Contribuição

Pull requests são bem-vindos.

Caso encontre bugs ou queira sugerir melhorias, abra uma issue.