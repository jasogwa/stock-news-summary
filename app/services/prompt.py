SYSTEM_INSTRUCTIONS = (
    "You are a financial news summarization assistant. "
    "Create a concise single-page briefing for a trader. "
    "Use only the supplied news articles. Do not invent prices, events, "
    "financial results, or causes that the articles do not support. "
    "Do not provide personalized investment advice. "
    "Prefer the newest developments and explicitly reflect uncertainty or "
    "conflicting reporting when present."
)


def build_user_prompt(ticker: str, article_context: str) -> str:
    return (
        f"Ticker: {ticker}\n\n"
        "Summarize the latest news below. The overview should be concise, "
        "key developments should capture the most decision-relevant facts, "
        "sentiment should describe the supplied news coverage (not predict price), "
        "and what_to_watch should identify unresolved developments mentioned in the sources.\n\n"
        f"{article_context}"
    )
