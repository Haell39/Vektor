import streamlit as st

TIMEFRAMES = {
    "Últimas 4 horas": "now 4-H",
    "Último dia": "now 1-d",
    "Última semana": "now 7-d",
    "Último mês": "today 1-m",
    "Últimos 3 meses": "today 3-m",
    "Último ano": "today 12-m",
    "Últimos 5 anos": "today 5-y",
}

GEO_OPTIONS = {
    "Mundial": "",
    "Brasil": "BR",
    "Estados Unidos": "US",
    "Portugal": "PT",
    "Reino Unido": "GB",
    "Alemanha": "DE",
    "Índia": "IN",
}


def render_sidebar() -> dict:
    with st.sidebar:
        st.markdown("## ⚡ Vektor")
        st.caption("Análise de Tendências por IA")

        st.divider()

        st.subheader("Configurações")

        api_key = st.text_input(
            "OpenAI API Key",
            type="password",
            placeholder="sk-...",
            help="Sua chave é usada apenas localmente, nunca armazenada.",
        )

        st.divider()
        st.subheader("Parâmetros de Busca")

        raw_keywords = st.text_area(
            "Palavras-chave",
            placeholder="ex: marketing digital\nprodutividade\nia generativa",
            height=110,
            help="Uma por linha. Máximo de 5.",
        )

        keywords = [k.strip() for k in raw_keywords.splitlines() if k.strip()][:5]

        if keywords:
            st.caption(f"{len(keywords)}/5 termo(s) adicionado(s)")

        timeframe_label = st.selectbox("Período", list(TIMEFRAMES.keys()), index=5)
        geo_label = st.selectbox("Região", list(GEO_OPTIONS.keys()), index=0)

        st.divider()
        analyze = st.button("Analisar Tendências", type="primary", use_container_width=True)

        st.divider()
        st.caption("Vektor v1.0 · Dados via Google Trends")

    return {
        "api_key": api_key,
        "keywords": keywords,
        "timeframe": TIMEFRAMES[timeframe_label],
        "geo": GEO_OPTIONS[geo_label],
        "geo_label": geo_label,
        "timeframe_label": timeframe_label,
        "analyze": analyze,
    }
