from functools import lru_cache

from fastapi import HTTPException

from app.config import get_settings
from app.services.news import YahooFinanceNewsProvider
from app.services.stock_summary import StockSummaryService
from app.services.summarizer import OpenAISummarizer


@lru_cache
def get_stock_summary_service() -> StockSummaryService:
    settings = get_settings()
    if not settings.openai_api_key:
        raise HTTPException(
            status_code=503,
            detail="OPENAI_API_KEY is not configured. See .env.example.",
        )

    return StockSummaryService(
        news_provider=YahooFinanceNewsProvider(),
        summarizer=OpenAISummarizer(
            api_key=settings.openai_api_key,
            model=settings.openai_model,
        ),
    )
