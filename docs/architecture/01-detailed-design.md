# Detailed Design Document

This document contains the detailed, implementation-level design decisions for the Trade Weaver platform, building upon the foundational choices recorded in our Architectural Decision Records (ADRs).

## 1. Broker Interface Contract

To ensure broker-agnosticism, all agents will interact with brokers through a standardized `BrokerInterface` defined in `src/core/broker_interface.py`. This allows us to switch between brokers like IBKR and a potential future Questrade integration with minimal changes to the core trading logic.

### Interface Definition (Python Abstract Base Class)

```python
from abc import ABC, abstractmethod

class BrokerInterface(ABC):

    @abstractmethod
    def connect(self, portfolio_id: str):
        """Establishes and authenticates the connection for a specific portfolio."""
        pass

    @abstractmethod
    def get_account_summary(self, portfolio_id: str) -> dict:
        """Retrieves account balance, margin, and currency information."""
        pass

    @abstractmethod
    def get_market_data(self, ticker: str, market: str) -> dict:
        """Fetches real-time price, volume, and Level II data for a security."""
        pass

    @abstractmethod
    def execute_order(self, trade_request: dict) -> dict:
        """Submits a trade order and returns an initial confirmation."""
        pass

    @abstractmethod
    def get_order_status(self, order_id: str) -> dict:
        """Checks the status of a previously submitted order (e.g., pending, filled, cancelled)."""
        pass
```

## 2. Firestore Database Schema (Initial Version)

The following outlines the primary collections and their intended document structures.

### `Portfolios` Collection

* **Document ID:** Auto-generated unique ID.
* **Purpose:** The central document for a single pool of capital.
* **Fields:**
  * `name`: (string) "Claude's Investment Fund"
  * `ownerId`: (string) UID from Firebase Auth.
  * `managers`: (array of strings) List of UIDs for users with Trader/PM roles.
  * `capital`: (map) `{ "CAD": 100000, "USD": 50000 }`
  * `pnl`: (map) `{ "daily": 150.75, "total": 2500.50 }`
  * `settings`: (map)
    * `yoloLiveEnabled`: (boolean) `false`
    * `yoloPaperEnabled`: (boolean) `true`
    * `activeStrategies`: (array of strings) `["Momentum_Breakout"]`
    * `maxDailyDrawdownPercent`: (number) `6`

### `Trades` Collection

* **Document ID:** Auto-generated unique ID.
* **Purpose:** An immutable log of every single trade execution.
* **Fields:**
  * `portfolioId`: (string) Foreign key to the `Portfolios` collection.
  * `status`: (string) "FILLED", "CANCELLED", "ERROR"
  * `ticker`: (string) "AAPL"
  * `market`: (string) "NASDAQ"
  * `direction`: (string) "LONG"
  * `quantity`: (number) 100
  * `executionPrice`: (number) 175.50
  * `currency`: (string) "USD"
  * `exchangeRateApplied`: (number) 1.3570
  * `totalCostInBaseCurrency`: (number) 23815.35 (which is 100 *175.50* 1.3570)
  * `timestamp`: (timestamp) Firestore timestamp of execution.
  * `mode`: (string) "live" or "paper"
  