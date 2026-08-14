from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class Sentiment(StrEnum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    MIXED = "mixed"
    NEUTRAL = "neutral"


class NewsArticle(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str
    summary: str | None = None
    url: HttpUrl
    source: str = "Unknown"
    published_at: datetime | None = None


class StockSummary(BaseModel):
    model_config = ConfigDict(extra="forbid")

    overview: str = Field(description="Concise overview of the latest news")
    key_developments: list[str] = Field(min_length=1, max_length=5)
    sentiment: Sentiment
    what_to_watch: list[str] = Field(min_length=1, max_length=4)


class StockSummaryResponse(BaseModel):
    ticker: str
    generated_at: datetime
    newest_article_at: datetime | None
    summary: StockSummary
    sources: list[NewsArticle]
