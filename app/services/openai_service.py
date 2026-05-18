import httpx
from openai import OpenAI, RateLimitError, AuthenticationError


def _make_client(api_key: str, base_url: str | None, timeout: int = 120) -> OpenAI:
    """Cria cliente OpenAI com httpx configurado para local ou cloud."""
    if base_url:
        # HTTP local: desativa verify SSL e usa timeout generoso para modelos lentos
        http_client = httpx.Client(verify=False, timeout=httpx.Timeout(timeout))
        return OpenAI(api_key=api_key, base_url=base_url, http_client=http_client)
    return OpenAI(api_key=api_key, timeout=timeout)


def test_connection(api_key: str, base_url: str, model: str) -> dict:
    """Testa se o servidor local está acessível e o modelo está carregado."""
    try:
        client = _make_client(api_key, base_url, timeout=10)
        client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "ping"}],
            max_tokens=5,
        )
        return {"ok": True, "error": None}
    except Exception as e:
        msg = str(e)
        if "Connection refused" in msg or "connect" in msg.lower():
            return {"ok": False, "error": "Servidor LM Studio não encontrado. Inicie o servidor em LM Studio → Local Server → Start."}
        return {"ok": False, "error": msg}


def generate_strategic_report(
    api_key: str,
    keywords: list[str],
    trends_summary: str,
    base_url: str | None = None,
    model: str = "gpt-4o-mini",
) -> dict:
    if not api_key:
        return {"report": None, "error": "Chave de API não informada."}
    if base_url is None and not api_key.startswith("sk-"):
        return {"report": None, "error": "Chave da API OpenAI inválida ou não informada."}

    prompt = f"""Você é um consultor de marketing digital e estrategista de negócios especializado em análise de tendências.

Com base nos dados do Google Trends abaixo, gere um relatório estratégico conciso e acionável sobre os termos: {', '.join(keywords)}.

DADOS DE TENDÊNCIA:
{trends_summary}

Estruture o relatório com:
1. **Visão Geral do Nicho** - O que os dados revelam sobre o mercado
2. **Oportunidades Identificadas** - 3 oportunidades concretas baseadas nos dados
3. **Público-Alvo Potencial** - Perfil inferido a partir do interesse geográfico e temporal
4. **Estratégia de Conteúdo** - 5 ideias de conteúdo com alto potencial
5. **Próximos Passos** - Plano de ação prioritário em 30/60/90 dias

Seja direto, use dados específicos do relatório e evite generalidades. Formato Markdown."""

    try:
        client = _make_client(api_key, base_url)
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1500,
        )
        return {"report": response.choices[0].message.content, "error": None}
    except AuthenticationError:
        return {"report": None, "error": "Chave da API inválida. Verifique sua OpenAI API Key."}
    except RateLimitError:
        return {"report": None, "error": "Rate limit da OpenAI atingido. Aguarde um momento e tente novamente."}
    except Exception as e:
        msg = str(e)
        if "Connection refused" in msg or "connect" in msg.lower():
            return {"report": None, "error": "Não foi possível conectar ao servidor local. Verifique se o LM Studio está rodando e o servidor iniciado."}
        return {"report": None, "error": msg}
