# Stock News Summary

A small FastAPI application that gives traders a concise, AI-generated briefing of the latest news for a stock ticker. It fetches recent ticker news, normalizes the provider-specific response, asks OpenAI to create a structured summary, and returns the source articles alongside the generated briefing.

The take-home brief asked for a solution that can be understood and extended easily, so this implementation intentionally favors a small number of clear components over additional infrastructure.
