import asyncio
from datetime import datetime, timezone
from typing import Any, Protocol

import yfinance as yf

from app.models.summary import NewsArticle


class NewsProviderError(RuntimeError):
    pass


class NewsProvider(Protocol):
    async def get_latest_news(self, ticker: str, limit: int) -> list[NewsArticle]: ...


class YahooFinanceNewsProvider:
    """Adapted around yfinance.

    The rest of the application depends only on the NewsProvider protocol, so this
    provider can be replaced by a licensed production market/news feed later.
    """

    async def get_latest_news(self, ticker: str, limit: int) -> list[NewsArticle]:
        return await asyncio.to_thread(self._get_latest_news_sync, ticker, limit)

    def _get_latest_news_sync(self, ticker: str, limit: int) -> list[NewsArticle]:
        try:
            raw_items = yf.Ticker(ticker).get_news(count=limit, tab="news")
        except Exception as exc:  # provider boundary: convert library/network errors
            raise NewsProviderError("Unable to fetch financial news") from exc

        articles: list[NewsArticle] = []
        for item in raw_items or []:
            article = self._normalize(item)
            if article is not None:
                articles.append(article)

        articles.sort(
            key=lambda article: article.published_at or datetime.min.replace(tzinfo=timezone.utc),
            reverse=True,
        )
        return articles[:limit]

    @staticmethod
    def _normalize(item: dict[str, Any]) -> NewsArticle | None:
        # yfinance has returned both flat and nested Yahoo Finance news shapes over time.
        content = item.get("content") if isinstance(item.get("content"), dict) else item

        title = content.get("title") or item.get("title")
        if not title:
            return None

        provider = content.get("provider") or {}
        source = (
            provider.get("displayName")
            or item.get("publisher")
            or item.get("provider")
            or "Unknown"
        )
        if isinstance(source, dict):
            source = source.get("displayName", "Unknown")

        url = YahooFinanceNewsProvider._extract_url(content, item)
        if not url:
            return None

        summary = (
            content.get("summary")
            or content.get("description")
            or item.get("summary")
            or item.get("description")
        )
        published_at = YahooFinanceNewsProvider._extract_published_at(content, item)

        try:
            return NewsArticle(
                title=str(title),
                summary=str(summary) if summary else None,
                url=url,
                source=str(source),
                published_at=published_at,
            )
        except ValueError:
            return None

    @staticmethod
    def _extract_url(content: dict[str, Any], item: dict[str, Any]) -> str | None:
        canonical = content.get("canonicalUrl")
        if isinstance(canonical, dict) and canonical.get("url"):
            return canonical["url"]

        click = content.get("clickThroughUrl")
        if isinstance(click, dict) and click.get("url"):
            return click["url"]

        return item.get("link") or item.get("url")

    @staticmethod
    def _extract_published_at(
        content: dict[str, Any], item: dict[str, Any]
    ) -> datetime | None:
        iso_value = content.get("pubDate") or content.get("displayTime")
        if isinstance(iso_value, str):
            try:
                return datetime.fromisoformat(iso_value.replace("Z", "+00:00"))
            except ValueError:
                pass

        timestamp = item.get("providerPublishTime")
        if isinstance(timestamp, (int, float)):
            return datetime.fromtimestamp(timestamp, tz=timezone.utc)

        return None
