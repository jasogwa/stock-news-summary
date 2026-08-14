from app.services.news import YahooFinanceNewsProvider


def test_normalizes_nested_yfinance_shape():
    article = YahooFinanceNewsProvider._normalize(
        {
            "content": {
                "title": "A company headline",
                "summary": "A short excerpt",
                "provider": {"displayName": "Example Publisher"},
                "pubDate": "2026-08-11T12:00:00Z",
                "canonicalUrl": {"url": "https://example.com/story"},
            }
        }
    )

    assert article is not None
    assert article.title == "A company headline"
    assert article.source == "Example Publisher"
    assert article.published_at is not None


def test_ignores_news_without_title_or_url():
    assert YahooFinanceNewsProvider._normalize({"content": {}}) is None
