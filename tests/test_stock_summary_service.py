import pytest

from app.services.stock_summary import NoNewsFoundError, StockSummaryService


class FakeNewsProvider:
    def __init__(self, articles):
        self.articles = articles

    async def get_latest_news(self, ticker: str, limit: int):
        return self.articles[:limit]


class FakeSummarizer:
    def __init__(self, summary):
        self.summary = summary

    async def summarize(self, ticker: str, articles):
        return self.summary


@pytest.mark.asyncio
async def test_builds_response(sample_articles, sample_summary):
    service = StockSummaryService(
        FakeNewsProvider(sample_articles), FakeSummarizer(sample_summary)
    )

    response = await service.get_summary("NVDA", limit=8)

    assert response.ticker == "NVDA"
    assert response.summary == sample_summary
    assert len(response.sources) == 2
    assert response.newest_article_at == sample_articles[0].published_at


@pytest.mark.asyncio
async def test_raises_when_no_news(sample_summary):
    service = StockSummaryService(FakeNewsProvider([]), FakeSummarizer(sample_summary))

    with pytest.raises(NoNewsFoundError):
        await service.get_summary("UNKNOWN", limit=8)
