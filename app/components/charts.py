import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

PALETTE = px.colors.qualitative.Vivid
CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color="#e0e0e0"),
    legend=dict(orientation="h", y=-0.15),
    margin=dict(l=0, r=0, t=40, b=0),
    xaxis=dict(gridcolor="rgba(255,255,255,0.05)", showline=False),
    yaxis=dict(gridcolor="rgba(255,255,255,0.05)", showline=False, range=[0, 110]),
)


def interest_over_time_chart(df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    for i, col in enumerate(df.columns):
        color = PALETTE[i % len(PALETTE)]
        fig.add_trace(go.Scatter(
            x=df.index, y=df[col], name=col,
            line=dict(color=color, width=2.5),
            mode="lines",
            hovertemplate=f"<b>{col}</b><br>%{{x|%d %b %Y}}<br>Interesse: %{{y}}<extra></extra>",
        ))
        peak_idx = df[col].idxmax()
        peak_val = int(df[col].max())
        fig.add_annotation(
            x=peak_idx, y=peak_val,
            text=f"▲ {peak_val}",
            showarrow=True, arrowhead=2, arrowsize=0.8, arrowwidth=1.5,
            arrowcolor=color, font=dict(size=10, color=color),
            bgcolor="rgba(14,14,18,0.85)", bordercolor=color, borderwidth=1, borderpad=4,
            ax=0, ay=-36,
        )
    fig.update_layout(title="Interesse ao Longo do Tempo", **CHART_LAYOUT)
    return fig


def forecast_chart(series: pd.Series, forecast_df: pd.DataFrame, keyword: str) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=list(forecast_df.index) + list(forecast_df.index[::-1]),
        y=list(forecast_df["yhat_upper"]) + list(forecast_df["yhat_lower"][::-1]),
        fill="toself", fillcolor="rgba(124,92,252,0.12)",
        line=dict(color="rgba(0,0,0,0)"),
        name="Intervalo de Confiança", showlegend=True,
        hoverinfo="skip",
    ))
    fig.add_trace(go.Scatter(
        x=series.index, y=series.values, name="Histórico",
        line=dict(color="#7C5CFC", width=2.5),
        hovertemplate="%{x|%d %b %Y}<br>Interesse: %{y}<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=forecast_df.index, y=forecast_df["yhat"],
        name="Projeção 90 dias",
        line=dict(color="#a78bfa", width=2, dash="dash"),
        hovertemplate="%{x|%d %b %Y}<br>Projeção: %{y:.0f}<extra></extra>",
    ))
    _now_x = str(series.index[-1])
    fig.add_shape(
        type="line",
        x0=_now_x, x1=_now_x,
        y0=0, y1=1,
        xref="x", yref="paper",
        line=dict(dash="dot", color="rgba(255,255,255,0.25)", width=1),
    )
    fig.add_annotation(
        x=_now_x, y=1,
        xref="x", yref="paper",
        text="Agora",
        showarrow=False,
        font=dict(color="rgba(255,255,255,0.4)", size=11),
        xanchor="left", yanchor="bottom",
    )
    layout = {**CHART_LAYOUT, "yaxis": {**CHART_LAYOUT["yaxis"], "range": [0, 115]}}
    fig.update_layout(title=f"Projeção de Tendência — {keyword} (próximos 90 dias)", **layout)
    return fig


def interest_by_region_chart(df: pd.DataFrame, keyword: str) -> go.Figure:
    df_sorted = df.sort_values(keyword, ascending=True).tail(15)
    fig = px.bar(
        df_sorted,
        x=keyword,
        y=df_sorted.index,
        orientation="h",
        color=keyword,
        color_continuous_scale="Bluyl",
        labels={keyword: "Índice de Interesse", "y": "País"},
        title=f"Top Regiões — {keyword}",
    )
    fig.update_layout(**CHART_LAYOUT, coloraxis_showscale=False)
    return fig


def related_queries_chart(df: pd.DataFrame, title: str) -> go.Figure:
    df = df.head(10).sort_values("value", ascending=True)
    fig = px.bar(
        df,
        x="value",
        y="query",
        orientation="h",
        color="value",
        color_continuous_scale="Teal",
        labels={"value": "Pontuação", "query": ""},
        title=title,
    )
    fig.update_layout(**CHART_LAYOUT, coloraxis_showscale=False)
    return fig


def trend_heatmap(df: pd.DataFrame) -> go.Figure:
    if df.shape[1] < 2:
        return None
    corr = df.corr()
    fig = px.imshow(
        corr,
        color_continuous_scale="RdBu_r",
        zmin=-1, zmax=1,
        title="Correlação entre Termos",
        text_auto=".2f",
    )
    fig.update_layout(**CHART_LAYOUT)
    return fig
