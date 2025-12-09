# 🧠 API de Análise de Sentimentos de Feedbacks

Este projeto apresenta uma API profissional desenvolvida com **FastAPI** e **Hugging Face Transformers** para classificar comentários, avaliações e mensagens em:

- **positivo**
- **neutro**
- **negativo**

Ou, alternativamente, no modo **binário**:

- **positivo**
- **negativo**

A solução foi criada para empresas que precisam:

- identificar rapidamente elogios e reclamações;
- priorizar atendimentos negativos;
- medir a satisfação do cliente ao longo do tempo;
- automatizar a análise de feedbacks em grande volume.

---

## 🚀 Tecnologias Utilizadas

- **Python 3.11+**
- **FastAPI**
- **Uvicorn**
- **Transformers (Hugging Face)**
- **PyTorch**
- **Pydantic**
- **Frontend simples em HTML/CSS/JS**

---

## 📁 Estrutura do Projeto

```
sentiment_api/
├── app/
│   ├── main.py              # Pontos de entrada da API
│   ├── schemas.py           # Modelos de entrada/saída
│   └── services/
│       ├── model_loader.py  # Carregamento do modelo Hugging Face
│       └── sentiment.py     # Lógica de classificação
├── frontend/
│   └── index.html           # Interface simples para demonstração
├── requirements.txt
└── README.md
```

---

## ⚙️ Instalação e Execução

### 1️⃣ Clonar o repositório

```bash
git clone https://github.com/copli/sentiment-api.git
cd sentiment-api
```

### 2️⃣ Criar o ambiente virtual

```bash
python -m venv .venv
```

Ativar:

Windows:

```bash
.venv\Scripts\activate
```

Linux/Mac:

```bash
source .venv/bin/activate
```

### 3️⃣ Instalar dependências

```bash
pip install -r requirements.txt
```

### 4️⃣ Rodar a API

```bash
uvicorn app.main:app --reload
```

A API estará disponível em:

```
http://127.0.0.1:8000
```

Documentação interativa:

```
http://127.0.0.1:8000/docs
```

---

## 🧠 Modelo de NLP

O modelo utilizado é:

**nlptown/bert-base-multilingual-uncased-sentiment**

Ele retorna uma classificação de 1 a 5 estrelas:

- ⭐ 1–2 → negativo  
- ⭐ 3 → neutro  
- ⭐ 4–5 → positivo  

A API converte esses valores em **labels legíveis**.

---

## 🔌 Endpoints da API

### 🔹 **GET /**

Retorna informações básicas sobre a API.

---

### 🔹 **GET /health**

Verifica se o serviço está operante.

Resposta:

```json
{ "status": "ok" }
```

---

### 🔹 **POST /sentimento**

Classifica o sentimento de **um único texto**.

#### Corpo da requisição:

```json
{
  "texto": "O atendimento foi excelente!",
  "modo": "triclasse"
}
```

Valores aceitos para `"modo"`:

- `"triclasse"` → positivo / neutro / negativo  
- `"binario"` → positivo / negativo  

#### Resposta:

```json
{
  "label": "positivo",
  "score": 0.98
}
```

---

### 🔹 **POST /sentimentos/lote**

Classifica **vários textos de uma só vez** e retorna estatísticas.

#### Corpo da requisição:

```json
{
  "textos": [
    "O atendimento foi excelente, muito rápido.",
    "Demorou demais, estou insatisfeito.",
    "Foi ok, nada demais."
  ],
  "modo": "triclasse"
}
```

#### Exemplo de resposta:

```json
{
  "resultados": [
    { "texto": "...", "label": "positivo", "score": 0.95 },
    { "texto": "...", "label": "negativo", "score": 0.88 },
    { "texto": "...", "label": "neutro", "score": 0.52 }
  ],
  "estatisticas": {
    "total": 3,
    "positivos": 1,
    "negativos": 1,
    "neutros": 1,
    "porcent_positivos": 33.33,
    "porcent_negativos": 33.33,
    "porcent_neutros": 33.33
  }
}
```

---

## 💻 Frontend Simples

O arquivo `frontend/index.html` permite testar:

- análise individual  
- análise em lote (um feedback por linha)  
- modo binário e triclasse  

Basta abrir o arquivo no navegador.

---

## 📊 Possíveis integrações

- Sistemas de atendimento (SAC / CRM)  
- Aplicações Web e Mobile  
- Chatbots  
- Painéis (Power BI, Tableau, Superset)  
- Monitoramento de redes sociais  

---

## 🧩 Melhorias Futuras

- Treinar modelo próprio PT-BR  
- Deploy em cloud (Railway, Render, Azure)  
- Pipeline CI/CD com GitHub Actions  
- Histórico de análises em banco de dados  
- Dashboard interativo da taxa de satisfação  

---

## 👥 Equipe

Carlos Oberto Pereira Lima – Desenvolvedor Backend

João Batista – Cientista de Dados

Gabriela Duarte do Nascimento – Engenheira de Dados

Everton Guedes – Desenvolvedor Backend

Marcos Antonio dos Santos – Cientista de Dados

Felipe Miguel – Cientista de Dados

Tainah Torres – Cientista de Dados

Márcio Pereira – Desenvolvedor Backend

Paulo Fleury – Desenvolvedor Backend

Kauê Araújo – Desenvolvedor Backend
---

## 📄 Licença

MIT — livre para uso e modificação.
