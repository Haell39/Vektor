# Vektor — Status do Projeto

> Última atualização: Fevereiro 2026

---

## Versão atual: v2.0

O projeto está **em produção** e acessível publicamente em:

🔗 **https://vektorapp.streamlit.app/**

---

## Infraestrutura

| Componente           | Tecnologia                                         | Status         |
| -------------------- | -------------------------------------------------- | -------------- |
| Frontend + Backend   | Streamlit ≥ 1.33                                   | ✅ Rodando     |
| Dados de tendências  | pytrends ≥ 4.9.2                                   | ✅ Estável     |
| IA generativa        | OpenAI GPT-4o-mini                                 | ✅ Operacional |
| Visualização         | Plotly ≥ 5.20                                      | ✅ Estável     |
| Previsão estatística | NumPy (regressão polinomial grau 2 + sazonalidade) | ✅ Estável     |
| Persistência local   | SQLite3 (`vektor_history.db`)                      | ✅ Automático  |
| Deploy               | Streamlit Community Cloud                          | ✅ Ativo       |
| Container (local)    | Docker + docker-compose                            | ✅ Disponível  |

---

## Estrutura de arquivos

```
vektor/
├── streamlit_app.py          # Entry point para Streamlit Cloud
├── requirements.txt          # Dependências pinadas
├── Dockerfile
├── docker-compose.yml
├── vektor_history.db         # Banco SQLite gerado automaticamente (gitignored)
├── .streamlit/
│   └── config.toml           # Tema dark, cor primária #7C5CFC
├── app/
│   ├── main.py               # Orquestrador principal (6 tabs)
│   ├── components/
│   │   ├── charts.py         # Gráficos Plotly (tendência, previsão, mapa, barras)
│   │   └── sidebar.py        # Inputs do usuário (keywords, período, geo, API key)
│   ├── services/
│   │   ├── trends.py         # Wrapper pytrends com cache 1h
│   │   ├── openai_service.py # Relatório GPT-4o-mini
│   │   ├── forecast.py       # Previsão 90 dias (numpy)
│   │   └── history.py        # CRUD SQLite
│   └── utils/
│       ├── styles.py         # PREMIUM_CSS injetado via st.markdown
│       └── helpers.py        # build_trends_summary, format_keyword_list
└── docs/
    ├── plano_acao.md         # Roadmap V2.0 → V3.0
    └── status.md             # Este arquivo
```

---

## Tabs da aplicação

| Tab | Ícone           | Conteúdo                                    |
| --- | --------------- | ------------------------------------------- |
| 1   | 📈 Tendência    | Gráfico histórico com anotação de pico      |
| 2   | 🔮 Previsão     | Projeção 90 dias com banda de confiança     |
| 3   | 🌍 Geografia    | Mapa + ranking de regiões                   |
| 4   | 🔗 Relacionadas | Queries em alta e termos associados         |
| 5   | 🤖 Relatório IA | Análise estratégica GPT-4o-mini, export .md |
| 6   | 🗂 Histórico    | Últimas 30 buscas com botão limpar          |

---

## Dependências (`requirements.txt`)

```
streamlit>=1.33.0
pytrends>=4.9.2
openai>=1.30.0
plotly>=5.20.0
pandas>=2.0.0
urllib3<2
```

> `urllib3<2` está pinada para compatibilidade com a versão de `requests` usada internamente pelo pytrends (evita `TypeError: method_whitelist`).

---

## Custos estimados

| Item                               | Custo     |
| ---------------------------------- | --------- |
| Streamlit Cloud (deploy)           | Gratuito  |
| OpenAI GPT-4o-mini (por relatório) | ~$0.00055 |
| Google Trends (pytrends)           | Gratuito  |

---

## Bugs corrigidos (histórico)

| Bug                                                             | Causa                                                                                           | Fix                                                                           |
| --------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| `ModuleNotFoundError: No module named 'app'`                    | sys.path não incluía a raiz do projeto                                                          | `sys.path.insert` em `main.py` + `streamlit_app.py` na raiz                   |
| `Retry.__init__() got unexpected keyword 'method_whitelist'`    | urllib3 ≥ 2.0 removeu esse parâmetro                                                            | `urllib3<2` em requirements.txt                                               |
| `IndentationError` em `sidebar.py`                              | Bloco `return` duplicado no final do arquivo                                                    | Remoção do bloco duplicado                                                    |
| Caracteres quebrados (â€™, ðŸ"ˆ) em `main.py`                   | PowerShell corrompeu encoding UTF-8 ao escrever o arquivo                                       | Reescrita do arquivo via `python -c "open(..., encoding='utf-8').write(...)"` |
| `TypeError: Addition/subtraction of integers and Timestamp`     | `add_vline` do Plotly faz `sum([x])` internamente; falha com `pandas.Timestamp`                 | Substituído por `add_shape` + `add_annotation` com `x=str(...)`               |
| `TypeError: unsupported operand type(s) for +: 'int' and 'str'` | `add_vline` com string também falha no Plotly (`sum(["string"])` retorna erro pois inicia de 0) | Consolidado com a correção acima (uso de `add_shape` + `add_annotation`)      |

---

## Próximas features (V3.0 — roadmap)

Ver [plano_acao.md](plano_acao.md) para detalhes.

- [ ] Export PDF com `reportlab`
- [ ] Alertas por e-mail (scheduler em background)
- [ ] Histórico em nuvem com Supabase
- [ ] Comparação entre períodos
- [ ] Score de oportunidade (índice composto)
