# Broker Interface Contract

To ensure broker-agnosticism, all agents will interact with brokers through a standardized `BrokerInterface`. As per the revised architecture in ADR-0007, this shared interface will be defined in `shared_libs/core/broker_interface.py`. This allows us to switch between brokers like IBKR and a potential future Questrade integration with minimal changes to the core trading logic of any agent that uses it.

## Interface Definition (Python Abstract Base Class)

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
