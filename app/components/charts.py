import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

PALETTE = px.colors.qualitative.Vivid
CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color="#e0e0e0"),
    legend=dict(orientation="h", y=-0.15),
    margin=dict(l=0, r=0, t=30, b=0),
    xaxis=dict(gridcolor="rgba(255,255,255,0.06)", showline=False),
    yaxis=dict(gridcolor="rgba(255,255,255,0.06)", showline=False),
)


def interest_over_time_chart(df: pd.DataFrame) -> go.Figure:
    fig = px.line(
        df,
        x=df.index,
        y=df.columns.tolist(),
        color_discrete_sequence=PALETTE,
        labels={"value": "Interesse (0-100)", "variable": "Termo", "index": ""},
        title="Interesse ao Longo do Tempo",
    )
    fig.update_traces(line_width=2.5)
    fig.update_layout(**CHART_LAYOUT)
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
