import pandas as pd


def build_trends_summary(
    df_time: pd.DataFrame,
    df_region: pd.DataFrame | None,
    keywords: list[str],
    timeframe_label: str,
    geo_label: str,
) -> str:
    lines = [f"Período: {timeframe_label} | Região: {geo_label}", ""]

    lines.append("=== TENDÊNCIA TEMPORAL ===")
    for kw in keywords:
        if kw in df_time.columns:
            series = df_time[kw]
            peak = series.idxmax()
            lines.append(
                f"- {kw}: máximo={series.max()}, mínimo={series.min()}, "
                f"média={series.mean():.1f}, pico em {peak.strftime('%d/%m/%Y') if hasattr(peak, 'strftime') else peak}"
            )

    if df_region is not None and not df_region.empty:
        lines.append("\n=== TOP 5 REGIÕES (1º termo) ===")
        top5 = df_region[keywords[0]].nlargest(5)
        for country, val in top5.items():
            lines.append(f"- {country}: {val}")

    return "\n".join(lines)


def format_keyword_list(keywords: list[str]) -> str:
    return ", ".join(f"**{k}**" for k in keywords)
