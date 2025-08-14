# [CONCEPT: Alternative_Data] Using SEC Filings as a Trade Signal

This document details the strategy and methodology for using real-time SEC filings as a primary source of alternative data to generate high-alpha trading signals. While this data is public, a significant competitive edge can be gained by systematically accessing, parsing, and analyzing these filings faster and more intelligently than the broader market.

## 1. The Alpha in Regulatory Filings

Traditional data sources like earnings reports are widely disseminated and quickly priced into the market. The true edge lies in processing unstructured, text-based regulatory filings to identify material events *before* they become a mainstream news headline. This requires a specialized data feed and an NLP-driven analysis pipeline.

- **EODHD Data Gap:** While EODHD provides fundamental data, it does **not** provide the real-time, granular access to SEC filings needed for this strategy. Therefore, a supplementary, specialized API is a **non-negotiable requirement**.
- **Recommended Provider:** **sec-api.io** is the recommended provider due to its real-time streaming API, full-text search capabilities, and pre-parsed JSON outputs for key forms, which drastically reduces development time.

## 2. Key Forms for Day Traders

### Form 8-K: Material Events

- **Purpose:** An "unscheduled" filing used to notify investors of any material event that is important for them to know about. It is the most critical source of immediate, high-impact catalysts.
- **High-Volatility Keywords & Event Types:** The agent's NLP model should be programmed to scan for and assign a high `Catalyst_Strength_Score` to filings containing the following:
  - **Financial Distress:** `bankruptcy`, `receivership`, `delisting`, `default`, `material impairment`.
  - **Leadership Changes:** `unexpected departure` of a CEO or CFO.
  - **Corporate Actions:** `entry into a material definitive agreement`, `completion of acquisition`, `mergers & acquisitions`.
  - **Regulatory & Legal:** `SEC investigation`, `internal investigation`, `material weakness`.
  - **Operational:** `cybersecurity incident`, `data breach`, `product recall`.

### Form 4: Insider Trading

- **Purpose:** Filed whenever a corporate insider (director, officer, or >10% owner) buys or sells shares of their own company. It must be filed within two business days of the transaction.
- **Interpretation as a Signal:**
  - **Bullish Signal:** A **cluster of buys** by multiple insiders is a strong positive signal, indicating that the people with the most information believe the stock is undervalued.
  - **Bearish Signal:** A **cluster of sells** can be a negative signal. However, it requires more nuance, as insiders may sell for reasons unrelated to company performance (e.g., diversification, tax planning).
  - **Noise vs. Signal:** A single insider trade is often just noise. The agent must be programmed to detect **clusters** of activity.

## 3. ADK Implementation: `SecFilingsTool`

The agent will use a `FunctionTool` that leverages the `sec-api` Python library to fetch and parse these filings.

### Python Example: Fetching Recent 8-K Filings

```python
# [TOOL_CODE: fetch_recent_8k_filings]
from sec_api import QueryApi

# This tool would be part of the MarketAnalystPipeline
def fetch_recent_8k_filings(tool_context: ToolContext, ticker: str) -> list:
    """Fetches the most recent 8-K filings for a given ticker."""
    api_key = tool_context.state.get("secrets.sec_api_key")
    query_api = QueryApi(api_key=api_key)
    
    query = {
      "query": { "query_string": { "query": f"ticker:{ticker} AND formType:\"8-K\"" } },
      "from": "0",
      "size": "5",
      "sort": [{ "filedAt": { "order": "desc" } }]
    }
    
    try:
        response = query_api.get_filings(query)
        # In a real implementation, you would parse the full text of the filing
        # to search for the high-volatility keywords.
        return response.get('filings', [])
    except Exception as e:
        print(f"Error fetching SEC filings for {ticker}: {e}")
        return []
```
