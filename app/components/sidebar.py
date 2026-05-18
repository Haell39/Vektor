import streamlit as st
from app.services.openai_service import test_connection

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
        st.markdown(
            """
            <div style="padding: 0.5rem 0 0.2rem 0;">
                <span style="font-size:1.5rem; font-weight:800; letter-spacing:-0.5px;">⚡ Vektor</span>
                <span style="display:block; color:#555; font-size:0.78rem; margin-top:2px;">
                    Market Intelligence · v2.0
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.divider()

        st.markdown("**🧠 Provedor de IA**")
        provider = st.radio(
            "Provedor",
            ["OpenAI", "Modelo Local (LM Studio)"],
            horizontal=True,
            label_visibility="collapsed",
        )

        if provider == "OpenAI":
            st.markdown("**🔑 OpenAI API Key**")
            api_key = st.text_input(
                "OpenAI API Key",
                type="password",
                placeholder="sk-...",
                help="Usada apenas em memória, nunca armazenada.",
                label_visibility="collapsed",
            )
            base_url = None
            model_id = "gpt-4o-mini"
            if api_key:
                st.caption("✅ Chave configurada · gpt-4o-mini")
        else:
            st.markdown("**💻 LM Studio**")
            api_key = st.text_input(
                "API Key local",
                type="password",
                placeholder="sk-lm-...",
                help="A chave gerada pelo LM Studio (pode ser qualquer valor).",
                label_visibility="collapsed",
            )
            base_url = st.text_input(
                "Base URL",
                value="http://127.0.0.1:1234/v1",
                help="Endereço do servidor local do LM Studio.",
                label_visibility="collapsed",
            )
            model_id = st.text_input(
                "ID do Modelo",
                value="qwen2.5-coder-7b-instruct",
                help="Nome exato do modelo carregado no LM Studio.",
                label_visibility="collapsed",
            )
            if api_key and base_url and model_id:
                st.caption(f"✅ Local · `{model_id}`")
                if st.button("🔌 Testar Conexão", use_container_width=True):
                    with st.spinner("Testando..."):
                        res = test_connection(api_key, base_url, model_id)
                    if res["ok"]:
                        st.success("✅ Conectado! Modelo respondeu.")
                    else:
                        st.error(f"❌ {res['error']}")

        st.divider()
        st.markdown("**🔍 Parâmetros de Busca**")

        raw_keywords = st.text_area(
            "Palavras-chave",
            placeholder="ex: micro saas\nai tools\nautomação whatsapp",
            height=115,
            help="Uma por linha. Máximo de 5.",
        )
        keywords = [k.strip() for k in raw_keywords.splitlines() if k.strip()][:5]

        if keywords:
            st.caption(f"{'🟢' * len(keywords)}{'⚫' * (5 - len(keywords))}  {len(keywords)}/5 termos")

        timeframe_label = st.selectbox("Período", list(TIMEFRAMES.keys()), index=5)
        geo_label = st.selectbox("Região", list(GEO_OPTIONS.keys()), index=0)

        st.divider()
        analyze = st.button("⚡ Analisar Tendências", type="primary", use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.caption("Cache ativo · 1h · Dados: Google Trends")

    return {
        "api_key": api_key,
        "base_url": base_url,
        "model_id": model_id,
        "provider": provider,
        "keywords": keywords,
        "timeframe": TIMEFRAMES[timeframe_label],
        "geo": GEO_OPTIONS[geo_label],
        "geo_label": geo_label,
        "timeframe_label": timeframe_label,
        "analyze": analyze,
    }
