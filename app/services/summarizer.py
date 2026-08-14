import json
from typing import Protocol

from openai import AsyncOpenAI

from app.models.summary import NewsArticle, StockSummary
from app.services.prompt import SYSTEM_INSTRUCTIONS, build_user_prompt


class SummaryError(RuntimeError):
    pass


class Summarizer(Protocol):
    async def summarize(self, ticker: str, articles: list[NewsArticle]) -> StockSummary: ...


class OpenAISummarizer:
    def __init__(self, api_key: str, model: str = "gpt-5-mini") -> None:
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = model

    async def summarize(self, ticker: str, articles: list[NewsArticle]) -> StockSummary:
        if not articles:
            raise SummaryError("At least one article is required")

        article_context = "\n\n".join(
            self._format_article(index, article)
            for index, article in enumerate(articles, start=1)
        )

        instructions = SYSTEM_INSTRUCTIONS
        user_input = build_user_prompt(ticker, article_context)

        try:
            response = await self.client.responses.create(
                model=self.model,
                instructions=instructions,
                input=user_input,
                store=False,
                text={
                    "format": {
                        "type": "json_schema",
                        "name": "stock_news_summary",
                        "strict": True,
                        "schema": self._summary_schema(),
                    }
                },
            )
            return StockSummary.model_validate(json.loads(response.output_text))
        except Exception as exc:
            raise SummaryError("Unable to generate AI summary") from exc

    @staticmethod
    def _format_article(index: int, article: NewsArticle) -> str:
        published = article.published_at.isoformat() if article.published_at else "unknown"
        summary = article.summary or "No article excerpt available."
        return (
            f"[Article {index}]\n"
            f"Title: {article.title}\n"
            f"Source: {article.source}\n"
            f"Published: {published}\n"
            f"Excerpt: {summary}\n"
            f"URL: {article.url}"
        )

    @staticmethod
    def _summary_schema() -> dict:
        return {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "overview": {"type": "string"},
                "key_developments": {
                    "type": "array",
                    "items": {"type": "string"},
                    "minItems": 1,
                    "maxItems": 5,
                },
                "sentiment": {
                    "type": "string",
                    "enum": ["positive", "negative", "mixed", "neutral"],
                },
                "what_to_watch": {
                    "type": "array",
                    "items": {"type": "string"},
                    "minItems": 1,
                    "maxItems": 4,
                },
            },
            "required": [
                "overview",
                "key_developments",
                "sentiment",
                "what_to_watch",
            ],
        }
