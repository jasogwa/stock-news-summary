from datetime import datetime, timezone

import pytest

from app.models.summary import NewsArticle, Sentiment, StockSummary


@pytest.fixture
def sample_articles() -> list[NewsArticle]:
    return [
        NewsArticle(
            title="Example company reports quarterly results",
            summary="Revenue increased while management maintained its outlook.",
            url="https://example.com/article-1",
            source="Example News",
            published_at=datetime(2026, 8, 11, 12, 0, tzinfo=timezone.utc),
        ),
        NewsArticle(
            title="Analysts discuss upcoming product launch",
            summary="Attention is focused on the next product launch and guidance.",
            url="https://example.com/article-2",
            source="Example Wire",
            published_at=datetime(2026, 8, 11, 10, 0, tzinfo=timezone.utc),
        ),
    ]


@pytest.fixture
def sample_summary() -> StockSummary:
    return StockSummary(
        overview="The latest coverage focuses on quarterly results and upcoming products.",
        key_developments=["Quarterly revenue increased.", "Management maintained its outlook."],
        sentiment=Sentiment.POSITIVE,
        what_to_watch=["Upcoming product launch."],
    )
