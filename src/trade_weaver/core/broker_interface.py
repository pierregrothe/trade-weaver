# File: src/core/broker_interface.py

from abc import ABC, abstractmethod

class BrokerInterface(ABC):
    """
    An abstract base class defining the standardized interface for all broker integrations.
    This ensures that any broker can be swapped in without changing the agent logic
    that uses it.
    """

    @abstractmethod
    def connect(self, portfolio_id: str) -> bool:
        """
        Establishes and authenticates the connection to the broker for a specific portfolio.
        This method should handle loading credentials securely.
        Returns True on successful connection, False otherwise.
        """
        pass

    @abstractmethod
    def disconnect(self):
        """Closes the connection to the broker."""
        pass

    @abstractmethod
    def get_account_summary(self, portfolio_id: str) -> dict:
        """
        Retrieves key account metrics like balance, margin, and currency information.
        Returns a dictionary with the summary data.
        """
        pass

    @abstractmethod
    def get_market_data(self, ticker: str, market: str) -> dict:
        """
        Fetches real-time price, volume, and other relevant data for a security.
        Returns a dictionary containing the market data.
        """
        pass

    @abstractmethod
    def execute_order(self, trade_request: dict) -> dict:
        """
        Submits a trade order (buy/sell) to the broker.
        The trade_request dictionary should contain all necessary order details
        (ticker, quantity, order_type, etc.).
        Returns a dictionary with the initial order confirmation and order ID.
        """
        pass

    @abstractmethod
    def get_order_status(self, order_id: str) -> dict:
        """
        Checks the status of a previously submitted order.
        Returns a dictionary with the order status (e.g., 'PENDING', 'FILLED', 'CANCELLED').
        """
        pass