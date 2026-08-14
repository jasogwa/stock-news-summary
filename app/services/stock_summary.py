from datetime import datetime, timezone

from app.models.summary import StockSummaryResponse
from app.services.news import NewsProvider
from app.services.summarizer import Summarizer


class NoNewsFoundError(LookupError):
    pass


class StockSummaryService:
    def __init__(self, news_provider: NewsProvider, summarizer: Summarizer) -> None:
        self.news_provider = news_provider
        self.summarizer = summarizer

    async def get_summary(self, ticker: str, limit: int) -> StockSummaryResponse:
        articles = await self.news_provider.get_latest_news(ticker, limit)
        if not articles:
            raise NoNewsFoundError(f"No recent news found for {ticker}")

        summary = await self.summarizer.summarize(ticker, articles)
        published_dates = [a.published_at for a in articles if a.published_at is not None]

        return StockSummaryResponse(
            ticker=ticker,
            generated_at=datetime.now(timezone.utc),
            newest_article_at=max(published_dates) if published_dates else None,
            summary=summary,
            sources=articles,
        )
