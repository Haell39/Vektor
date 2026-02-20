from openai import OpenAI, RateLimitError, AuthenticationError


def generate_strategic_report(api_key: str, keywords: list[str], trends_summary: str) -> dict:
    if not api_key or not api_key.startswith("sk-"):
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
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
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
        return {"report": None, "error": str(e)}
