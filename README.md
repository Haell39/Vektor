<div align="center">

# ⚡ Vektor

**Inteligência de mercado em tempo real.**  
Combine Google Trends + OpenAI para descobrir nichos, validar ideias e gerar relatórios estratégicos em segundos.

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white&style=flat-square)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.33+-FF4B4B?logo=streamlit&logoColor=white&style=flat-square)](https://streamlit.io)
[![OpenAI](https://img.shields.io/badge/GPT--4o--mini-412991?logo=openai&logoColor=white&style=flat-square)](https://openai.com)
[![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)](LICENSE)

</div>

---

## O que é

Vektor é um micro-SaaS de análise de tendências que cruza dados do **Google Trends** com análise de **IA generativa** para entregar insights acionáveis sobre qualquer nicho de mercado — em menos de 30 segundos.

## Features

- 📈 **Tendência temporal** — interesse ao longo do tempo para até 5 termos simultâneos
- 🌍 **Mapa geográfico** — ranking dos países/regiões com maior demanda
- 🔗 **Consultas relacionadas** — queries em alta e termos associados ao nicho
- 🤖 **Relatório IA** — análise estratégica gerada por GPT-4o-mini com oportunidades, público-alvo e plano de ação 30/60/90 dias  
- ⬇️ **Export .md** — baixe o relatório para usar onde quiser
- ⚡ **Cache inteligente** — resultados cacheados por 1h para evitar bloqueios do Google

## Stack

| Layer | Tech |
|---|---|
| Frontend & Backend | Streamlit |
| Dados | pytrends (Google Trends) |
| IA | OpenAI GPT-4o-mini |
| Visualização | Plotly |
| Deploy | Streamlit Cloud / Docker |

## Como rodar

```bash
# 1. Clone e entre na pasta
git clone https://github.com/seu-usuario/vektor.git && cd vektor

# 2. Ambiente virtual
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # macOS/Linux

# 3. Dependências
pip install -r requirements.txt

# 4. Rodar
streamlit run streamlit_app.py
```

> A OpenAI API Key é inserida diretamente na interface. Nenhuma variável de ambiente necessária.

## Deploy com Docker

```bash
docker-compose up --build
```

## Deploy Streamlit Cloud

1. Suba o projeto no GitHub
2. Acesse [share.streamlit.io](https://share.streamlit.io)
3. Selecione o repo e defina `streamlit_app.py` como entry point
4. Deploy ✅

---

<div align="center">
  <sub>Feito com Python · Streamlit · OpenAI</sub>
</div>
