import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st

st.set_page_config(
    page_title="Vektor · Análise de Tendências",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

from app.components.sidebar import render_sidebar
from app.components.charts import (
    interest_over_time_chart,
    interest_by_region_chart,
    related_queries_chart,
    trend_heatmap,
)
from app.services.trends import (
    get_interest_over_time,
    get_interest_by_region,
    get_related_queries,
)
from app.services.openai_service import generate_strategic_report
from app.utils.helpers import build_trends_summary, format_keyword_list


def render_empty_state():
    st.markdown("<br>" * 2, unsafe_allow_html=True)
    col = st.columns([1, 2, 1])[1]
    with col:
        st.markdown(
            """
            <div style="text-align:center; padding: 3rem 2rem; border: 1px solid rgba(255,255,255,0.08);
                        border-radius: 16px; background: rgba(255,255,255,0.02);">
                <h1 style="font-size: 3rem; margin-bottom: 0.5rem;">⚡</h1>
                <h2 style="margin-bottom: 0.5rem;">Bem-vindo ao Vektor</h2>
                <p style="color: #888; font-size: 0.95rem;">
                    Insira palavras-chave na barra lateral e clique em<br>
                    <strong>Analisar Tendências</strong> para começar.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_metrics(df):
    cols = st.columns(len(df.columns))
    for col, kw in zip(cols, df.columns):
        current = int(df[kw].iloc[-1])
        peak = int(df[kw].max())
        delta = current - int(df[kw].iloc[-2]) if len(df) > 1 else 0
        col.metric(label=kw, value=f"{current}/100", delta=f"{delta:+d} pts", help=f"Pico histórico: {peak}/100")


def main():
    params = render_sidebar()

    st.markdown(
        "<h1 style='margin-bottom:0;'>⚡ Vektor</h1>"
        "<p style='color:#888; margin-top:4px;'>Inteligência de mercado em tempo real via Google Trends + OpenAI</p>",
        unsafe_allow_html=True,
    )
    st.divider()

    if not params["analyze"] and "trend_data" not in st.session_state:
        render_empty_state()
        return

    if params["analyze"]:
        if not params["keywords"]:
            st.warning("Adicione ao menos uma palavra-chave na barra lateral.")
            return

        with st.spinner("Coletando dados do Google Trends..."):
            iot = get_interest_over_time(
                params["keywords"], params["timeframe"], params["geo"]
            )
            ibr = get_interest_by_region(
                params["keywords"], params["timeframe"], params["geo"]
            )
            rq = get_related_queries(
                params["keywords"][0], params["timeframe"], params["geo"]
            )

        if iot["error"]:
            st.error(f"Erro ao buscar tendências: {iot['error']}")
            return

        st.session_state["trend_data"] = {
            "iot": iot, "ibr": ibr, "rq": rq, "params": params
        }

    data = st.session_state.get("trend_data")
    if not data:
        render_empty_state()
        return

    iot = data["iot"]
    ibr = data["ibr"]
    rq = data["rq"]
    p = data["params"]
    df = iot["data"]

    st.markdown(
        f"Analisando {format_keyword_list(p['keywords'])} · "
        f"**{p['timeframe_label']}** · Região: **{p['geo_label']}**"
    )
    st.markdown("<br>", unsafe_allow_html=True)
    render_metrics(df)
    st.markdown("<br>", unsafe_allow_html=True)

    tab_overview, tab_geo, tab_related, tab_ai = st.tabs(
        ["📈 Tendência", "🌍 Geografia", "🔗 Consultas Relacionadas", "🤖 Relatório IA"]
    )

    with tab_overview:
        st.plotly_chart(interest_over_time_chart(df), use_container_width=True)
        hm = trend_heatmap(df)
        if hm:
            st.plotly_chart(hm, use_container_width=True)

    with tab_geo:
        if ibr["error"]:
            st.warning(ibr["error"])
        elif ibr["data"] is not None:
            for kw in p["keywords"]:
                if kw in ibr["data"].columns:
                    st.plotly_chart(
                        interest_by_region_chart(ibr["data"], kw),
                        use_container_width=True,
                    )
        else:
            st.info("Dados geográficos não disponíveis para esse filtro.")

    with tab_related:
        if rq["error"]:
            st.warning(rq["error"])
        else:
            c1, c2 = st.columns(2)
            with c1:
                if rq["top"] is not None and not rq["top"].empty:
                    st.plotly_chart(
                        related_queries_chart(rq["top"], f"Top Consultas — {p['keywords'][0]}"),
                        use_container_width=True,
                    )
                else:
                    st.info("Sem dados de top consultas.")
            with c2:
                if rq["rising"] is not None and not rq["rising"].empty:
                    st.plotly_chart(
                        related_queries_chart(rq["rising"], f"Em Alta — {p['keywords'][0]}"),
                        use_container_width=True,
                    )
                else:
                    st.info("Sem dados de consultas em alta.")

    with tab_ai:
        if not p["api_key"]:
            st.info(
                "Insira sua **OpenAI API Key** na barra lateral para gerar o relatório estratégico.",
                icon="🔑",
            )
        else:
            gen_col, _ = st.columns([1, 3])
            generate = gen_col.button("Gerar Relatório Estratégico", type="primary")

            if generate or "ai_report" in st.session_state:
                if generate:
                    summary = build_trends_summary(
                        df,
                        ibr["data"] if not ibr["error"] else None,
                        p["keywords"],
                        p["timeframe_label"],
                        p["geo_label"],
                    )
                    with st.spinner("Analisando dados com IA..."):
                        result = generate_strategic_report(p["api_key"], p["keywords"], summary)
                    if result["error"]:
                        st.error(result["error"])
                        return
                    st.session_state["ai_report"] = result["report"]

                report = st.session_state.get("ai_report")
                if report:
                    st.markdown(
                        "<div style='background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08);"
                        " border-radius: 12px; padding: 2rem;'>",
                        unsafe_allow_html=True,
                    )
                    st.markdown(report)
                    st.markdown("</div>", unsafe_allow_html=True)
                    st.download_button(
                        "⬇ Baixar Relatório (.md)",
                        data=report,
                        file_name=f"vektor_report_{'_'.join(p['keywords'][:2])}.md",
                        mime="text/markdown",
                    )


if __name__ == "__main__":
    main()
