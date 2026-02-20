# ⚡ Vektor — Análise de Tendências com IA

Plataforma de inteligência de mercado que combina **Google Trends** com **OpenAI** para gerar relatórios estratégicos sobre nichos, palavras-chave e oportunidades de conteúdo.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.33+-FF4B4B?logo=streamlit&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-412991?logo=openai&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-ready-2496ED?logo=docker&logoColor=white)

---

## Funcionalidades

- **Tendência temporal** — gráfico de interesse ao longo do tempo para até 5 termos simultâneos
- **Análise geográfica** — ranking dos países com maior interesse por termo
- **Consultas relacionadas** — top queries e termos em alta associados ao nicho
- **Correlação entre termos** — heatmap de correlação entre os termos pesquisados
- **Relatório estratégico IA** — análise via GPT-4o-mini com oportunidades, perfil de público e plano de ação
- **Cache inteligente** — resultados do Google Trends são cacheados por 1 hora
- **Download do relatório** — exporta o relatório gerado em `.md`

---

## Estrutura do Projeto

```
Vektor/
├── app/
│   ├── main.py                  # Entry point Streamlit
│   ├── components/
│   │   ├── sidebar.py           # Sidebar com inputs e configurações
│   │   └── charts.py            # Gráficos Plotly
│   ├── services/
│   │   ├── trends.py            # Integração pytrends + cache
│   │   └── openai_service.py    # Integração OpenAI
│   └── utils/
│       └── helpers.py           # Funções auxiliares
├── .streamlit/
│   └── config.toml              # Tema dark premium
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## Como Rodar

### Opção 1 — Local

**Pré-requisitos:** Python 3.10+

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS/Linux

pip install -r requirements.txt
streamlit run app/main.py
```

Acesse: http://localhost:8501

---

### Opção 2 — Docker

```bash
docker-compose up --build
# background:
docker-compose up -d
```

Para parar: `docker-compose down`

---

### Opção 3 — Streamlit Community Cloud (deploy gratuito)

1. Push para um repositório GitHub
2. Acesse [share.streamlit.io](https://share.streamlit.io)
3. Selecione o repo, branch `main` e arquivo `app/main.py`
4. Clique em **Deploy**

> A OpenAI API Key é inserida pela interface — sem secrets de ambiente necessários.

---

## OpenAI API Key

Inserida diretamente na sidebar da aplicação. Usada apenas em memória, nunca persistida.

---

## Dependências

| Pacote      | Uso                       |
| ----------- | ------------------------- |
| `streamlit` | Frontend e servidor       |
| `pytrends`  | Dados do Google Trends    |
| `openai`    | Relatórios estratégicos   |
| `plotly`    | Visualizações interativas |
| `pandas`    | Manipulação de dados      |

---

## Notas

- Rate limit do Google Trends é tratado com mensagem amigável e instrução de aguardar.
- Cache de 1h evita requisições repetidas para os mesmos parâmetros.
- Modelo padrão: `gpt-4o-mini`. Para trocar, edite `app/services/openai_service.py`.

---

## Licença

MIT
