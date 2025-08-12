# Firestore Database Schema

This document provides a comprehensive definition of the Firestore database collections and schemas that form the data backbone of the Trade Weaver platform. The design prioritizes query efficiency, scalability, and cost management by following Firestore best practices, including denormalization where appropriate.

## Core Design Principles

- **Structure for Queries:** Data is modeled to match the specific read patterns of the application, minimizing the need for complex client-side joins.
- **Denormalization for Reads:** To optimize for read speed, some data is intentionally duplicated. For example, a ticker symbol is stored on a trade document, even though it could be looked up from a separate instrument document.
- **Aggregation for Cost:** High-frequency data (like market data) is aggregated into time-bucketed documents (the "roll-up" pattern) to minimize write operations.

---

## 1. Platform & Market Configuration

These collections store the global configurations for the entire platform. They are typically written to once during setup or by an administrator, and read by the `CoordinatorAgent` at the start of a session.

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

- **Purpose:** Stores detailed configuration for each supported stock exchange. This is the implementation of the "market matrix."
- **Document ID:** Human-readable string (e.g., `NASDAQ`).
- **Interactions & Usage:**
  - **Writes:** Administrator (manual setup).
  - **Reads:** `CoordinatorAgent` to get the specific configuration for each exchange pipeline (e.g., which proxy instruments to use for the TSX).

```json
// /Exchanges/NASDAQ
{
  "exchange_id": "NASDAQ",
  "market_id": "AMER", // Foreign key to Markets collection
  "name": "NASDAQ Stock Market",
  "country_code": "US",
  "trading_hours_et": "09:30-16:00",
  "pre_market_mechanism": "Continuous Trading", // Introspective
  "proxy_instruments": null,
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
    "orb_duration_mins": 15, // Default for normal volatility
    "volume_rvol_confirmation": 2.0 // Standard confirmation
  },
  "enabled": true
}
```

---

## 2. Agent & Portfolio Configuration

This new collection is critical for dynamically managing the agent's behavior on a per-portfolio basis without requiring code deployments.

### `AgentConfigurations` Collection

- **Purpose:** Stores a live, editable configuration for each portfolio. This allows administrators to tune risk parameters, enable/disable strategies, and adjust model thresholds in real-time.
- **Document ID:** `portfolio_uuid` (Foreign key to the `Portfolios` collection).
- **Interactions & Usage:**
  - **Writes:** Administrator or Portfolio Manager via the UI.
  - **Reads:** The `CoordinatorAgent` and all sub-agents read this document at the start of every run to get their precise operating instructions for that specific portfolio.

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
            "override_params": null // No override, use defaults from Strategies collection
        },
        "ORB_v1": {
            "enabled": true,
            "override_params": {
                "orb_duration_mins": 30, // Override for a specific portfolio
                "volume_rvol_confirmation": 2.5
            }
        },
        "Mean_Reversion_v1": {
            "enabled": false, // Strategy disabled for this portfolio
            "override_params": null
        }
    }
}
```

---

## 2. Operational Data

These collections store the data generated during the agent's daily operations.

### `DailyWatchlists` Collection

- **Purpose:** Stores the final, ranked output of the pre-market analysis pipeline for a given day.
- **Document ID:** `YYYY-MM-DD` (e.g., `2025-08-12`).
- **Interactions & Usage:**
  - **Writes:** The `CoordinatorAgent` writes a single document here at the end of the pre-market run.
  - **Reads:** The `ExecutionAgent` (or a human trader via the UI) reads this document to get the day's trading candidates.

```json
// /DailyWatchlists/2025-08-12
{
  "analysis_timestamp_utc": "2025-08-12T13:30:00Z",
  "exchanges_scanned": ["NASDAQ", "TSX"],
  "analysis_results": [
    // Array of ExchangeAnalysisResult objects
  ]
}
```

### `TradeSignals` Collection

- **Purpose:** An immutable log of every high-probability `StockCandidateObject` generated by the pre-market scan. This provides a granular record for the ML feedback loop.
- **Document ID:** `signal_uuid` (UUID).
- **Interactions & Usage:**
  - **Writes:** The `MarketAnalystPipeline` for each exchange writes multiple documents here.
  - **Reads:** The `PostMarketMLAgent` reads these documents and the corresponding `Trades` to train its models.

```json
// /TradeSignals/{signal_uuid}
{
  "watchlist_date": "2025-08-12",
  "ticker": "AAPL",
  "exchange_id": "NASDAQ",
  "rank": 1,
  "overall_score": 92.5,
  // ... other fields from StockCandidateObject
  "trade_outcome": {
      "executed": true,
      "trade_id": "{trade_uuid}", // Foreign key to the resulting trade
      "net_pnl": 145.50
  }
}
```

### `Trades` Collection

- **Purpose:** An immutable log of every executed trade, enhanced with post-trade analysis metrics.
- **Document ID:** `trade_uuid` (UUID).
- **Interactions & Usage:**
  - **Writes:** The `ExecutionAgent` writes a document here after a trade is completed.
  - **Reads:** The `PostMarketMLAgent` reads these for performance analysis. The UI reads this to display trade history.

```json
// /Trades/{trade_uuid}
{
  "portfolio_id": "{portfolio_uuid}",
  "signal_id": "{signal_uuid}", // Foreign key to the TradeSignal
  "status": "FILLED",
  "ticker": "AAPL",
  "market_id": "NASDAQ",
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

## 3. User & Portfolio Management

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
  - **Reads:** The `CoordinatorAgent` reads the settings (`active_strategies`, `exchanges`) to configure its run. The `RiskGovernor` reads capital and drawdown limits.

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

## 4. Auditing

This collection provides an immutable log of critical system events for compliance and debugging.

### `ConfigurationAudit` Collection

- **Purpose:** Creates a permanent, immutable audit trail of every change made to any portfolio's configuration, as required by `ADR-0015`.
- **Document ID:** `audit_uuid` (UUID).
- **Interactions & Usage:**
  - **Writes:** The `ConfigurationManagerAgent` writes a new document here every time a change is proposed, validated, and applied.
  - **Reads:** Read by administrators and compliance officers for auditing and post-incident analysis.

```json
// /ConfigurationAudit/{audit_uuid}
{
    "timestamp_utc": "...",
    "portfolio_id": "{portfolio_uuid}",
    "user_id": "{userId}", // The user who initiated the change
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

---

## 4. Auditing

This collection provides an immutable log of critical system events for compliance and debugging.

### `ConfigurationAudit` Collection

- **Purpose:** Creates a permanent, immutable audit trail of every change made to any portfolio's configuration, as required by `ADR-0015`.
- **Document ID:** `audit_uuid` (UUID).
- **Interactions & Usage:**
  - **Writes:** The `ConfigurationManagerAgent` writes a new document here every time a change is proposed, validated, and applied.
  - **Reads:** Read by administrators and compliance officers for auditing and post-incident analysis.

```json
// /ConfigurationAudit/{audit_uuid}
{
    "timestamp_utc": "...",
    "portfolio_id": "{portfolio_uuid}",
    "user_id": "{userId}", // The user who initiated the change
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
