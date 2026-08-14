interface ArticleSource {
  title: string;
  source: string;
  url: string;
  published_at?: string;
}

interface StockSummaryData {
  overview: string;
  sentiment: string;
  key_developments: string[];
  what_to_watch: string[];
}

interface SummaryResponse {
  ticker: string;
  generated_at: string;
  newest_article_at: string | null;
  summary: StockSummaryData;
  sources: ArticleSource[];
  detail?: string;
}

export class StockSummaryApp {
  form = document.getElementById("summary-form") as HTMLFormElement | null;
  tickerInput = document.getElementById("ticker") as HTMLInputElement | null;
  statusEl = document.getElementById("status") as HTMLParagraphElement | null;
  errorEl = document.getElementById("error") as HTMLParagraphElement | null;
  resultEl = document.getElementById("result") as HTMLElement | null;

  constructor() {
    this.init();
  }

  init = (): void => {
    if (this.form) {
      this.form.addEventListener("submit", this.handleSubmit);
    }
  };

  fillList = (id: string, items: string[]): void => {
    const list = document.getElementById(id);
    if (!list) return;

    list.replaceChildren(
      ...items.map((text: string) => {
        const li = document.createElement("li");
        li.textContent = text;
        return li;
      }),
    );
  };

  renderSources = (sources: ArticleSource[]): void => {
    const sourceList = document.getElementById("sources");
    if (!sourceList) return;

    sourceList.replaceChildren(
      ...sources.map((source: ArticleSource) => {
        const li = document.createElement("li");
        const link = document.createElement("a");
        link.href = source.url;
        link.target = "_blank";
        link.rel = "noreferrer";
        link.textContent = `${source.title} — ${source.source}`;
        li.appendChild(link);
        return li;
      }),
    );
  };

  renderResult = (data: SummaryResponse): void => {
    const headingEl = document.getElementById("heading");
    if (headingEl) headingEl.textContent = `${data.ticker} briefing`;

    const overviewEl = document.getElementById("overview");
    if (overviewEl) overviewEl.textContent = data.summary.overview;

    const sentimentEl = document.getElementById("sentiment");
    if (sentimentEl) sentimentEl.textContent = data.summary.sentiment;

    const freshnessEl = document.getElementById("freshness");
    if (freshnessEl) {
      freshnessEl.textContent =
        `Generated ${new Date(data.generated_at).toLocaleString()}` +
        (data.newest_article_at
          ? ` · newest source ${new Date(data.newest_article_at).toLocaleString()}`
          : "");
    }

    this.fillList("developments", data.summary.key_developments);
    this.fillList("watch", data.summary.what_to_watch);
    this.renderSources(data.sources);

    if (this.resultEl) this.resultEl.classList.remove("hidden");
    if (this.statusEl) this.statusEl.textContent = "";
  };

  setStatus = (message: string): void => {
    if (this.statusEl) this.statusEl.textContent = message;
  };

  setError = (error: unknown): void => {
    this.setStatus("");
    if (this.errorEl) {
      if (error instanceof Error) {
        this.errorEl.textContent = error.message;
      } else {
        this.errorEl.textContent = "An unknown error occurred";
      }
      this.errorEl.classList.remove("hidden");
    }
  };

  resetUI = (): void => {
    if (this.resultEl) this.resultEl.classList.add("hidden");
    if (this.errorEl) this.errorEl.classList.add("hidden");
  };

  handleSubmit = async (event: SubmitEvent): Promise<void> => {
    event.preventDefault();
    if (!this.tickerInput) return;

    const ticker = this.tickerInput.value.trim().toUpperCase();
    this.resetUI();
    this.setStatus(`Loading latest news for ${ticker}…`);

    try {
      const response = await fetch(
        `/api/stocks/${encodeURIComponent(ticker)}/summary`,
      );
      const data = (await response.json()) as SummaryResponse;

      if (!response.ok) {
        throw new Error(data.detail || "Unable to generate summary");
      }

      this.renderResult(data);
    } catch (err: unknown) {
      this.setError(err);
    }
  };
}

new StockSummaryApp();
