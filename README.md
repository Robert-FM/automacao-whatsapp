# 📱 Automação de Envio de Mensagens pelo WhatsApp Web

Script em Python para enviar uma mensagem para contatos listados em uma planilha Excel usando o WhatsApp Web e Selenium.

O programa normaliza números brasileiros, remove duplicidades, lê a mensagem de um arquivo de texto e aguarda um intervalo aleatório entre os envios. Também oferece modo de simulação (`dry-run`), envio para um único número e reutilização de um perfil separado do Chrome.

## ✨ Funcionalidades

- Leitura dos contatos a partir de uma planilha `.xlsx`.
- Seleção da coluna de telefones por nome do cabeçalho.
- Normalização de números: remoção de caracteres não numéricos e inclusão do código do Brasil (`55`) para números com 10 ou 11 dígitos.
- Remoção de contatos duplicados.
- Leitura da mensagem a partir de um arquivo `.txt`.
- Envio pelo WhatsApp Web com Selenium.
- Intervalo aleatório entre os envios.
- Persistência de sessão por meio de um diretório de perfil do Chrome.
- Modo `dry-run`, que valida e lista os contatos sem enviar mensagens.
- Opção de envio para apenas um número com `--numero`.
- Registro de progresso, avisos e falhas no terminal.
- Opção de execução sem janela visível com `--headless`.

## 🛠️ Tecnologias utilizadas

- Python 3.14, conforme `.python-version` e `pyproject.toml`.
- Selenium `>=4.20` para controlar o navegador e o WhatsApp Web.
- OpenPyXL `>=3.1` para leitura da planilha Excel.
- ChromeDriver incluído em `chromedriver/win64/154.0.8037.92/`.
- `uv` para sincronização do ambiente a partir de `pyproject.toml` e `uv.lock`.

## 📁 Estrutura do projeto

```text
whatsapp_automation/
├── chromedriver/win64/154.0.8037.92/chromedriver.exe
├── contatos_exemplo.csv
├── main.py
├── msm.txt
├── msm2.txt
├── pyproject.toml
├── README.md
├── uv.lock
├── whatsapp_sender.py
└── zap cursistas.xlsx
```

Arquivos gerados durante a execução, como `.venv/`, `__pycache__/` e os perfis `.chrome_whatsapp/`, não fazem parte do fluxo documentado.

## 📋 Pré-requisitos

- Python 3.14.
- Google Chrome instalado.
- Uma conta com acesso ao WhatsApp Web.
- `uv` para a instalação recomendada ou `pip` para a alternativa tradicional.
- Uma planilha Excel com uma linha de cabeçalho contendo a coluna de telefones.

Na primeira execução interativa, o WhatsApp Web pode solicitar autenticação por QR Code. O perfil padrão usado pelo script é `.chrome_whatsapp`, separado do perfil pessoal do Chrome.

## 📦 Instalação

### Com `uv`

Na raiz do projeto:

```bash
uv sync
```

### Com ambiente virtual e `pip`

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Windows Prompt de Comando:

```cmd
.venv\Scripts\activate
```

Instale as dependências definidas no `pyproject.toml`:

```bash
python -m pip install .
```

## ⚙️ Preparação dos arquivos

### Planilha de contatos

Por padrão, o script procura `zap cursistas.xlsx` e a coluna `zap`. O cabeçalho é comparado sem distinção entre maiúsculas e minúsculas.

Exemplo:

```text
Nome | Zap             | E-mail
Ana  | (41) 99948-0821 | ana@example.com
```

O programa utiliza apenas a coluna informada em `--coluna`. Linhas vazias são ignoradas e números inválidos são registrados como avisos.

### Arquivo da mensagem

Por padrão, a mensagem é lida de `msm2.txt`. O arquivo deve estar em UTF-8 e não pode estar vazio. O projeto também contém `msm.txt` como outra mensagem disponível.

## ▶️ Como executar

Com `uv`:

```bash
uv run python main.py
```

Com o ambiente virtual ativado:

```bash
python main.py
```

### Simulação sem envio

```bash
uv run python main.py --dry-run
```

### Envio para um único número

```bash
uv run python main.py --numero 5581999999999
```

Quando `--numero` é informado, ele substitui a lista carregada da planilha.

### Usar outros arquivos ou parâmetros

```bash
uv run python main.py --excel "outra_planilha.xlsx" --mensagem msm.txt --coluna telefone --minimo 8 --maximo 15 --timeout 60
```

Os argumentos disponíveis podem ser consultados com:

```bash
uv run python main.py --help
```

### Parâmetros disponíveis

| Parâmetro | Padrão | Descrição |
|---|---|---|
| `--excel` | `zap cursistas.xlsx` | Caminho da planilha de contatos. |
| `--mensagem` | `msm2.txt` | Arquivo `.txt` com a mensagem. |
| `--coluna` | `zap` | Nome da coluna que contém os telefones. |
| `--perfil` | `.chrome_whatsapp` | Diretório do perfil separado do Chrome pessoal. |
| `--perfil-chrome` | `Default` | Nome do perfil do Chrome utilizado. |
| `--minimo` | `5` | Intervalo mínimo entre envios, em segundos. |
| `--maximo` | `10` | Intervalo máximo entre envios, em segundos. |
| `--timeout` | `45` | Tempo máximo de espera por elemento do WhatsApp Web. |
| `--dry-run` | desativado | Lista os contatos sem realizar envios. |
| `--numero` | nenhum | Substitui a planilha e envia para um único número. |
| `--headless` | desativado | Executa o Chrome sem janela visível. |

### Exemplo completo

O exemplo abaixo usa uma planilha diferente, uma mensagem alternativa, uma coluna chamada `telefone`, intervalo de 10 a 20 segundos e tempo limite de 60 segundos:

```bash
uv run python main.py --excel "contatos.xlsx" --mensagem msm.txt --coluna telefone --minimo 10 --maximo 20 --timeout 60
```

Antes de executar um envio real, valide a entrada com:

```bash
uv run python main.py --excel "contatos.xlsx" --mensagem msm.txt --coluna telefone --dry-run
```

## 🔄 Fluxo de processamento

1. `main.py` configura os logs, interpreta os argumentos e chama o executor.
2. `whatsapp_sender.py` abre a planilha e identifica a coluna configurada.
3. Os números são normalizados, validados e deduplicados.
4. A mensagem é lida do arquivo informado.
5. O Selenium inicia o Chrome e acessa o WhatsApp Web para cada número.
6. A mensagem é enviada com `Enter` e o script aguarda um intervalo aleatório entre `--minimo` e `--maximo`.
7. Ao final, o navegador é encerrado e o terminal informa a quantidade de envios e falhas.

## 🏗️ Organização do código

O projeto possui uma organização simples, dividida entre o ponto de entrada e o módulo responsável pela automação:

- `main.py`: configura o logging e inicia a execução.
- `whatsapp_sender.py`: contém a configuração, leitura dos contatos, leitura das mensagens, automação do navegador e interpretação dos argumentos.
- `pyproject.toml`: define o pacote, a versão mínima do Python e as dependências.
- `uv.lock`: registra as versões resolvidas pelo `uv`.
- `zap cursistas.xlsx`: planilha usada como entrada padrão.
- `msm.txt` e `msm2.txt`: mensagens disponíveis para envio.
- `chromedriver/`: driver local do Chrome incluído no repositório.

Não há servidor, banco de dados, API própria ou interface gráfica implementados. A interação ocorre diretamente no navegador controlado pelo Selenium.

## 📤 Entradas e saídas

### Entradas

- Planilha Excel com os números de telefone.
- Arquivo de texto contendo a mensagem.
- Argumentos opcionais da linha de comando.
- Sessão autenticada do WhatsApp Web no perfil do Chrome.

### Saídas

- Mensagens enviadas pelo WhatsApp Web.
- Logs no terminal com contatos carregados, progresso, avisos e falhas.
- Diretório de perfil do Chrome criado ou atualizado durante a execução.

O script não gera um relatório persistente de envios. O resumo final permanece apenas no log exibido no terminal.

## 🧪 Testes

Não foram encontrados testes automatizados no projeto. O modo `--dry-run` pode ser usado para verificar a leitura, normalização e deduplicação dos contatos antes de um envio real.

## ⚠️ Limitações e cuidados

- O fluxo depende da interface do WhatsApp Web e pode ser afetado por alterações nessa interface.
- O script não configura credenciais nem variáveis de ambiente; a autenticação é feita no navegador.
- O envio pode falhar por números inválidos, indisponibilidade do WhatsApp Web, alterações no navegador ou expiração do tempo limite.
- O uso deve respeitar as regras do WhatsApp, a legislação aplicável e o consentimento dos destinatários.
- O diretório de perfil do Chrome pode conter dados de sessão e deve ser tratado como informação privada.

## 🧰 Solução de problemas

### A coluna não foi encontrada

Confirme se o nome usado em `--coluna` corresponde ao cabeçalho da primeira linha da planilha. Por exemplo:

```bash
uv run python main.py --coluna Zap --dry-run
```

A comparação não diferencia letras maiúsculas e minúsculas, mas o nome precisa existir.

### A planilha ou a mensagem não foi encontrada

Informe o caminho correto explicitamente:

```bash
uv run python main.py --excel "dados/contatos.xlsx" --mensagem "mensagens/boas-vindas.txt" --dry-run
```

### O WhatsApp Web não conclui o carregamento

Verifique se o Chrome está instalado, se a conta foi autenticada e se o tempo limite é suficiente:

```bash
uv run python main.py --timeout 90
```

### O perfil do Chrome está em uso

Feche outras instâncias que estejam usando o mesmo diretório ou informe outro perfil:

```bash
uv run python main.py --perfil .chrome_whatsapp_novo
```

Não compartilhe nem publique diretórios de perfil, pois eles podem conter dados de sessão.

### Um número é considerado inválido

O código aceita números que, após a limpeza, tenham pelo menos 12 dígitos. Números brasileiros com 10 ou 11 dígitos recebem automaticamente o prefixo `55`; outros formatos devem ser fornecidos já com o código do país.

## 👨‍💻 Autor

**Robert Melo**

🔗 LinkedIn: [linkedin.com/in/robertdemelo](https://www.linkedin.com/in/robertdemelo/)

🐍 Python | Selenium | OpenPyXL | Automação de processos
