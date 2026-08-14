from fastapi.testclient import TestClient

from app.dependencies import get_stock_summary_service
from app.main import app
from app.services.stock_summary import StockSummaryService


class FakeNewsProvider:
    def __init__(self, articles):
        self.articles = articles

    async def get_latest_news(self, ticker: str, limit: int):
        return self.articles


class FakeSummarizer:
    def __init__(self, summary):
        self.summary = summary

    async def summarize(self, ticker: str, articles):
        return self.summary


def test_summary_endpoint(sample_articles, sample_summary):
    app.dependency_overrides[get_stock_summary_service] = lambda: StockSummaryService(
        FakeNewsProvider(sample_articles), FakeSummarizer(sample_summary)
    )
    client = TestClient(app)

    response = client.get("/api/stocks/nvda/summary")

    assert response.status_code == 200
    body = response.json()
    assert body["ticker"] == "NVDA"
    assert body["summary"]["sentiment"] == "positive"
    assert len(body["sources"]) == 2

    app.dependency_overrides.clear()


def test_invalid_ticker_is_400(sample_articles, sample_summary):
    app.dependency_overrides[get_stock_summary_service] = lambda: StockSummaryService(
        FakeNewsProvider(sample_articles), FakeSummarizer(sample_summary)
    )
    client = TestClient(app)

    response = client.get("/api/stocks/INVALID%20TICKER/summary")

    assert response.status_code == 400
    app.dependency_overrides.clear()
