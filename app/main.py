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
    forecast_chart,
)
from app.services.trends import (
    get_interest_over_time,
    get_interest_by_region,
    get_related_queries,
)
from app.services.openai_service import generate_strategic_report
from app.services.forecast import forecast_trend
from app.services.history import save_search, get_history, clear_history
from app.utils.helpers import build_trends_summary, format_keyword_list
from app.utils.styles import PREMIUM_CSS


def render_empty_state():
    st.markdown("<br>" * 2, unsafe_allow_html=True)
    col = st.columns([1, 2, 1])[1]
    with col:
        st.markdown(
            """
            <div style="text-align:center; padding: 3.5rem 2rem; border: 1px solid rgba(255,255,255,0.07);
                        border-radius: 18px; background: rgba(255,255,255,0.02);">
                <div style="font-size:3.5rem; margin-bottom:0.8rem;">⚡</div>
                <h2 style="margin-bottom:0.4rem; font-weight:700;">Bem-vindo ao Vektor</h2>
                <p style="color:#666; font-size:0.92rem; line-height:1.6;">
                    Insira palavras-chave na barra lateral e clique em<br>
                    <strong style="color:#a78bfa;">Analisar Tendências</strong> para começar.
                </p>
                <div style="margin-top:1.5rem; display:flex; justify-content:center; gap:0.6rem; flex-wrap:nowrap;">
                    <span style="background:rgba(124,92,252,0.12); border:1px solid rgba(124,92,252,0.25);
                           color:#c4b0ff; border-radius:20px; padding:4px 12px; font-size:0.76rem; white-space:nowrap;">
                        📈 Tendência Temporal
                    </span>
                    <span style="background:rgba(124,92,252,0.12); border:1px solid rgba(124,92,252,0.25);
                           color:#c4b0ff; border-radius:20px; padding:4px 12px; font-size:0.76rem; white-space:nowrap;">
                        🔮 Previsão 90 dias
                    </span>
                    <span style="background:rgba(124,92,252,0.12); border:1px solid rgba(124,92,252,0.25);
                           color:#c4b0ff; border-radius:20px; padding:4px 12px; font-size:0.76rem; white-space:nowrap;">
                        🤖 Relatório com IA
                    </span>
                    <span style="background:rgba(124,92,252,0.12); border:1px solid rgba(124,92,252,0.25);
                           color:#c4b0ff; border-radius:20px; padding:4px 12px; font-size:0.76rem; white-space:nowrap;">
                        🗂 Histórico
                    </span>
                </div>
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
        col.metric(
            label=kw,
            value=f"{current}/100",
            delta=f"{delta:+d} pts",
            help=f"Pico histórico no período: {peak}/100",
        )


def render_history_tab():
    df = get_history()
    if df.empty:
        st.info("Nenhuma análise salva ainda. As buscas são registradas automaticamente.", icon="🗂")
        return

    st.markdown(f"**{len(df)} análise(s) registrada(s)**")
    st.markdown("<br>", unsafe_allow_html=True)

    for _, row in df.iterrows():
        kws = ", ".join(row["keywords"]) if isinstance(row["keywords"], list) else row["keywords"]
        st.markdown(
            f"""
            <div style="background:rgba(255,255,255,0.025); border:1px solid rgba(255,255,255,0.07);
                        border-radius:10px; padding:0.9rem 1.2rem; margin-bottom:0.6rem;
                        display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.5rem;">
                <div>
                    <span style="font-weight:600; color:#e0e0e0;">{kws}</span>
                    <span style="color:#666; font-size:0.82rem; margin-left:0.8rem;">
                        {row['timeframe']} · {row['geo']}
                    </span>
                </div>
                <div style="display:flex; align-items:center; gap:1rem;">
                    <span style="background:rgba(124,92,252,0.15); color:#c4b0ff;
                           border-radius:6px; padding:2px 10px; font-size:0.8rem; font-weight:600;">
                        pico: {row['peak_term']} {row['peak_value']}/100
                    </span>
                    <span style="color:#555; font-size:0.78rem;">{row['created_at']}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🗑 Limpar Histórico", type="secondary"):
        clear_history()
        st.rerun()


def main():
    st.markdown(PREMIUM_CSS, unsafe_allow_html=True)
    params = render_sidebar()

    st.markdown(
        """
        <div style="display:flex; align-items:baseline; gap:0.7rem; margin-bottom:0.2rem;">
            <h1 style="margin:0; font-size:2rem; font-weight:800; letter-spacing:-0.5px;">⚡ Vektor</h1>
            <span class="vektor-badge">v2.0</span>
        </div>
        <p style="color:#555; margin-top:0; font-size:0.9rem;">
            Inteligência de mercado em tempo real · Google Trends + OpenAI + Forecasting
        </p>
        """,
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

        with st.status("Coletando dados...", expanded=True) as status:
            st.write("📡 Conectando ao Google Trends...")
            iot = get_interest_over_time(params["keywords"], params["timeframe"], params["geo"])

            if iot["error"]:
                status.update(label="Erro na coleta", state="error")
                st.error(f"Erro ao buscar tendências: {iot['error']}")
                return

            st.write("🌍 Processando dados geográficos...")
            ibr = get_interest_by_region(params["keywords"], params["timeframe"], params["geo"])

            st.write("🔗 Buscando consultas relacionadas...")
            rq = get_related_queries(params["keywords"][0], params["timeframe"], params["geo"])

            st.write("✅ Dados coletados com sucesso.")
            status.update(label="Análise concluída", state="complete", expanded=False)

        st.session_state["trend_data"] = {"iot": iot, "ibr": ibr, "rq": rq, "params": params}
        st.session_state.pop("ai_report", None)
        save_search(params["keywords"], params["timeframe_label"], params["geo_label"], iot["data"])

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
        f"<p style='color:#666; font-size:0.88rem; margin-bottom:0.8rem;'>"
        f"Analisando {format_keyword_list(p['keywords'])} · "
        f"<b style='color:#888'>{p['timeframe_label']}</b> · "
        f"<b style='color:#888'>{p['geo_label']}</b></p>",
        unsafe_allow_html=True,
    )
    render_metrics(df)
    st.markdown("<br>", unsafe_allow_html=True)

    tab_overview, tab_forecast, tab_geo, tab_related, tab_ai, tab_history = st.tabs([
        "📈 Tendência", "🔮 Previsão", "🌍 Geografia",
        "🔗 Relacionadas", "🤖 Relatório IA", "🗂 Histórico",
    ])

    with tab_overview:
        st.plotly_chart(interest_over_time_chart(df), use_container_width=True)
        hm = trend_heatmap(df)
        if hm:
            st.plotly_chart(hm, use_container_width=True)

    with tab_forecast:
        st.markdown(
            '<div class="forecast-note">⚠️ Previsão estatística baseada em tendência histórica e sazonalidade. '
            'Não considera eventos externos. Use como referência estratégica, não como certeza.</div>',
            unsafe_allow_html=True,
        )
        for kw in p["keywords"]:
            if kw not in df.columns:
                continue
            series = df[kw].dropna()
            fc = forecast_trend(series)
            if fc is not None:
                st.plotly_chart(forecast_chart(series, fc, kw), use_container_width=True)
                end_val = fc["yhat"].iloc[-1]
                start_val = series.iloc[-1]
                direction = "alta 📈" if end_val > start_val + 5 else ("baixa 📉" if end_val < start_val - 5 else "estável ➡️")
                c1, c2, c3 = st.columns(3)
                c1.metric("Interesse Atual", f"{int(start_val)}/100")
                c2.metric("Projeção (90d)", f"{int(end_val)}/100", f"{int(end_val - start_val):+d} pts")
                c3.metric("Tendência", direction)
                st.divider()
            else:
                st.info(f"Dados insuficientes para prever **{kw}**. Use um período mais longo.")

    with tab_geo:
        if ibr["error"]:
            st.warning(ibr["error"])
        elif ibr["data"] is not None:
            for kw in p["keywords"]:
                if kw in ibr["data"].columns:
                    st.plotly_chart(interest_by_region_chart(ibr["data"], kw), use_container_width=True)
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
            st.info("Insira sua **OpenAI API Key** na barra lateral para gerar o relatório estratégico.", icon="🔑")
        else:
            gen_col, _ = st.columns([1, 3])
            generate = gen_col.button("Gerar Relatório Estratégico", type="primary")

            if generate or "ai_report" in st.session_state:
                if generate:
                    summary = build_trends_summary(
                        df,
                        ibr["data"] if not ibr["error"] else None,
                        p["keywords"], p["timeframe_label"], p["geo_label"],
                    )
                    with st.spinner("Analisando dados com IA..."):
                        result = generate_strategic_report(p["api_key"], p["keywords"], summary)
                    if result["error"]:
                        st.error(result["error"])
                        return
                    st.session_state["ai_report"] = result["report"]

                report = st.session_state.get("ai_report")
                if report:
                    st.markdown('<div class="vektor-card">', unsafe_allow_html=True)
                    st.markdown(report)
                    st.markdown("</div>", unsafe_allow_html=True)
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.download_button(
                        "⬇ Baixar Relatório (.md)",
                        data=report,
                        file_name=f"vektor_report_{'_'.join(p['keywords'][:2])}.md",
                        mime="text/markdown",
                    )

    with tab_history:
        render_history_tab()


if __name__ == "__main__":
    main()
