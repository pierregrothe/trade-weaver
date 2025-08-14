# 01 Logical Data Model (Firestore)

**Note on Market Analysis Output:** As per ADR-0018, the Market Analyst Agent no longer writes its results to Firestore. The schemas previously defined for `DailyWatchlists` and `TradeSignals` are now obsolete in this document. The canonical schema for the Market Analyst Agent's JSON output is now defined in the Application Architecture domain. This document remains the canonical source for all other database collections used for system configuration and operational trade logging.

## Core Design Principles

- **Structure for Queries:** Data is modeled to match the specific read patterns of the application, minimizing the need for complex client-side joins.
- **Denormalization for Reads:** To optimize for read speed, some data is intentionally duplicated. For example, a ticker symbol is stored on a trade document, even though it could be looked up from a separate instrument document.
- **Aggregation for Cost:** High-frequency data (like market data) is aggregated into time-bucketed documents (the "roll-up" pattern) to minimize write operations.

---

## 1. Platform & Market Configuration

These collections store the global configurations for the entire platform. They are typically written to once during setup or by an administrator, and read by agents at the start of a session.

### `Markets` Collection

- **Purpose:** Defines the major markets (AMER, EMEA, APAC) the agent can operate in.
- **Document ID:** Human-readable string (e.g., `AMER`).
- **Interactions & Usage:**
  - **Writes:** Administrator (manual setup).
  - **Reads:** `CoordinatorAgent` to get a list of all markets to potentially scan.

```json
// /Markets/AMER
{
  "market_id": "AMER",
  "name": "Americas",
  "description": "North and South American markets.",
  "enabled": true
}
```

### `Exchanges` Collection

- **Purpose:** Stores detailed configuration for each supported stock exchange, including properties needed for analysis by the Market Analyst Agent.
- **Document ID:** Human-readable string (e.g., `NASDAQ`).
- **Interactions & Usage:**
  - **Writes:** Administrator (manual setup).
  - **Reads:** The `MarketAnalysisCoordinator` reads this to get specific configuration for each exchange pipeline (e.g., which VIX ticker to use).

```json
// /Exchanges/NASDAQ
{
  "exchange_id": "NASDAQ",
  "market_id": "AMER",
  "name": "NASDAQ Stock Market",
  "country_code": "US",
  "trading_hours_et": "09:30-16:00",
  "vix_ticker": "^VIX",
  "market_proxy_etf": "QQQ",
  "enabled": true
}
```

### `Strategies` Collection

- **Purpose:** A registry of all available trading strategies and their quantitatively-defined default parameters, based on extensive backtesting and research.
- **Document ID:** `strategy_uuid` (UUID).
- **Interactions & Usage:** Read by the system to understand the available strategies and their baseline configurations. `Portfolio` documents can override these defaults.

```json
// /Strategies/{strategy_uuid}
{
  "strategy_id": "Mean_Reversion_v1",
  "name": "Intraday Mean Reversion",
  "description": "A counter-trend strategy based on Bollinger Band and RSI confluence.",
  "version": "1.0",
  "parameters": {
    "bb_length": 20,
    "bb_std_dev": 2.0,
    "rsi_length": 10,
    "rsi_overbought": 75,
    "rsi_oversold": 25
  },
  "enabled": true
}

// /Strategies/{strategy_uuid}
{
  "strategy_id": "Momentum_v1",
  "name": "Intraday Momentum Pullback",
  "description": "A trend-following strategy using EMA crossovers and RSI for entry triggers.",
  "version": "1.0",
  "parameters": {
    "fast_ema": 9,
    "slow_ema": 21,
    "regime_filter_ema": 50,
    "rsi_length": 9,
    "rsi_bull_support": 50,
    "rsi_bear_resistance": 50
  },
  "enabled": true
}

// /Strategies/{strategy_uuid}
{
  "strategy_id": "ORB_v1",
  "name": "Opening Range Breakout",
  "description": "A breakout strategy based on the initial market open volatility.",
  "version": "1.0",
  "parameters": {
    "orb_duration_mins": 15,
    "volume_rvol_confirmation": 2.0
  },
  "enabled": true
}```

---

## 2. Agent & Portfolio Configuration

This collection is critical for dynamically managing agent behavior on a per-portfolio basis without requiring code deployments.

### `AgentConfigurations` Collection

-   **Purpose:** Stores a live, editable configuration for each portfolio. This allows administrators to tune risk parameters, enable/disable strategies, and adjust model thresholds in real-time.
-   **Document ID:** `portfolio_uuid` (Foreign key to the `Portfolios` collection).
-   **Interactions & Usage:**
    -   **Writes:** Administrator or Portfolio Manager via the UI.
    -   **Reads:** The `CoordinatorAgent` and all sub-agents read this document at the start of every run to get their precise operating instructions for that specific portfolio.

```json
// /AgentConfigurations/{portfolio_uuid}
{
    "risk_parameters": {
        "max_daily_drawdown_percent": 6,
        "max_risk_per_trade_percent": 1,
        "vix_circuit_breaker_threshold": 35
    },
    "ml_model_parameters": {
        "primary_model_id": "gbm_v3.2.1",
        "meta_model_id": "logistic_v1.2.0",
        "confidence_threshold": 0.60
    },
    "active_strategies": {
        "Momentum_v1": {
            "enabled": true,
            "override_params": null
        },
        "ORB_v1": {
            "enabled": true,
            "override_params": {
                "orb_duration_mins": 30,
                "volume_rvol_confirmation": 2.5
            }
        },
        "Mean_Reversion_v1": {
            "enabled": false,
            "override_params": null
        }
    }
}```

---

## 3. Operational Trade Logs

This collection stores the data generated by the **Strategy & Execution Agent** during its daily operations.

### `Trades` Collection

-   **Purpose:** An immutable log of every executed trade, enhanced with post-trade analysis metrics.
-   **Document ID:** `trade_uuid` (UUID).
-   **Interactions & Usage:**
    -   **Writes:** The **Strategy & Execution Agent** writes a document here after receiving a fill confirmation from the broker.
    -   **Reads:** The `PostMarketMLAgent` reads these for performance analysis. The UI reads this to display trade history.

```json
// /Trades/{trade_uuid}
{
  "portfolio_id": "{portfolio_uuid}",
  "status": "FILLED",
  "ticker": "AAPL",
  "exchange_id": "NASDAQ",
  "strategy_id": "ORB_v1",
  "direction": "LONG",
  "quantity": 100,
  "entry_price": 175.50,
  "exit_price": 177.00,
  "entry_timestamp_utc": "...",
  "exit_timestamp_utc": "...",
  "gross_pnl": 150.00,
  "net_pnl": 145.50,
  "mfe": 1.75,
  "mae": -0.25
}
```

---

## 4. User & Portfolio Management

These collections manage user and portfolio-specific data.

### `Users` Collection

- **Purpose:** Stores user profile information.
- **Document ID:** Firebase Auth UID.
- **Interactions & Usage:** Standard user profile data, read by the application UI.

```json
// /Users/{userId}
{
  "displayName": "Pierre G.",
  "email": "pierre@example.com",
  "roles": ["Admin", "Trader"]
}
```

### `Portfolios` Collection

- **Purpose:** The central document for a single pool of capital.
- **Document ID:** `portfolio_uuid` (UUID).
- **Interactions & Usage:**
  - **Writes:** An administrator or manager creates a new portfolio.
  - **Reads:** The `MarketAnalysisCoordinator` reads the `exchange_ids` to configure its run if they are not provided in the initial request. The `Strategy & Execution Agent` reads risk limits.

```json
// /Portfolios/{portfolio_uuid}
{
  "name": "Pierre's Momentum Fund",
  "owner_id": "{userId}",
  "managers": ["{userId}"],
  "capital": {"CAD": 100000, "USD": 50000},
  "settings": {
    "active_strategy_ids": ["{strategy_uuid}"],
    "max_daily_drawdown_percent": 6,
    "exchange_ids": ["NASDAQ", "TSX"]
  }
}
```

---

## 5. Auditing

This collection provides an immutable log of critical system events for compliance and debugging.

### `ConfigurationAudit` Collection

- **Purpose:** Creates a permanent, immutable audit trail of every change made to any portfolio's configuration, as required by ADR-0015.
- **Document ID:** `audit_uuid` (UUID).
- **Interactions & Usage:**
  - **Writes:** A dedicated configuration management service writes a new document here after a change is validated and applied.
  - **Reads:** Read by administrators and compliance officers for auditing and post-incident analysis.

```json
// /ConfigurationAudit/{audit_uuid}
{
    "timestamp_utc": "...",
    "portfolio_id": "{portfolio_uuid}",
    "user_id": "{userId}",
    "change_summary": "Increased max_risk_per_trade_percent from 1 to 1.5 for Momentum_v1",
    "changed_parameters": {
        "risk_parameters.max_risk_per_trade_percent": {
            "old_value": 1,
            "new_value": 1.5
        }
    },
    "validation_results": {
        "backtest_sharpe_ratio_delta": 0.15,
        "stress_test_max_drawdown_delta": -0.02
    },
    "approver_id": "{approver_userId}",
    "status": "APPLIED"
}
```
