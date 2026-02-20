import time
import streamlit as st
from pytrends.request import TrendReq
from pytrends.exceptions import ResponseError


def _build_client() -> TrendReq:
    return TrendReq(hl="pt-BR", tz=360, timeout=(10, 25), retries=2, backoff_factor=0.5)


@st.cache_data(ttl=3600, show_spinner=False)
def get_interest_over_time(keywords: list[str], timeframe: str, geo: str) -> dict:
    try:
        pt = _build_client()
        pt.build_payload(keywords, timeframe=timeframe, geo=geo)
        df = pt.interest_over_time()
        if df.empty:
            return {"data": None, "error": "Nenhum dado encontrado para essa combinação."}
        df = df.drop(columns=["isPartial"], errors="ignore")
        return {"data": df, "error": None}
    except ResponseError as e:
        return {"data": None, "error": f"Google Trends bloqueou a requisição (rate limit). Aguarde e tente novamente. [{e}]"}
    except Exception as e:
        return {"data": None, "error": str(e)}


@st.cache_data(ttl=3600, show_spinner=False)
def get_interest_by_region(keywords: list[str], timeframe: str, geo: str) -> dict:
    try:
        pt = _build_client()
        pt.build_payload(keywords, timeframe=timeframe, geo=geo)
        df = pt.interest_by_region(resolution="COUNTRY", inc_low_vol=False)
        df = df[df.sum(axis=1) > 0]
        if df.empty:
            return {"data": None, "error": "Sem dados geográficos disponíveis."}
        return {"data": df.nlargest(20, keywords[0]), "error": None}
    except ResponseError as e:
        return {"data": None, "error": f"Rate limit atingido. Tente novamente em alguns minutos. [{e}]"}
    except Exception as e:
        return {"data": None, "error": str(e)}


@st.cache_data(ttl=3600, show_spinner=False)
def get_related_queries(keyword: str, timeframe: str, geo: str) -> dict:
    try:
        pt = _build_client()
        pt.build_payload([keyword], timeframe=timeframe, geo=geo)
        related = pt.related_queries()
        result = related.get(keyword, {})
        return {"top": result.get("top"), "rising": result.get("rising"), "error": None}
    except ResponseError as e:
        return {"top": None, "rising": None, "error": f"Rate limit. Tente novamente mais tarde. [{e}]"}
    except Exception as e:
        return {"top": None, "rising": None, "error": str(e)}
