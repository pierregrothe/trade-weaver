# File: src/trade_weaver/core/broker_interface.py

from abc import ABC, abstractmethod


class BrokerInterface(ABC):
    """
    An abstract base class that defines the standardized contract for all broker integrations.

    This ensures that any broker (e.g., IBKR, Questrade) can be swapped in without
    changing the core agent logic that uses this interface. The agents will only
    ever interact with these defined methods.
    """

    @abstractmethod
    def connect(self, portfolio_id: str) -> bool:
        """
        Establishes and authenticates the connection to the broker for a specific portfolio.
        This method is responsible for securely loading credentials (e.g., from Secret Manager)
        and initiating the API session.

        Args:
            portfolio_id (str): The ID of the portfolio to connect for, used to fetch correct credentials.

        Returns:
            bool: True on successful connection, False otherwise.
        """
        pass

    @abstractmethod
    def disconnect(self):
        """Closes the connection to the broker gracefully."""
        pass

    @abstractmethod
    def get_account_summary(self) -> dict:
        """
        Retrieves key account metrics like balance, margin, and currency information for the
        currently connected account.

        Returns:
            dict: A dictionary containing the summary data (e.g., {'totalCashValue': 100000, ...}).
        """
        pass

    @abstractmethod
    def get_market_data(self, ticker: str) -> dict:
        """
        Fetches real-time price, volume, and other relevant data for a security.

        Args:
            ticker (str): The stock symbol to fetch data for (e.g., 'AAPL').

        Returns:
            dict: A dictionary containing the market data.
        """
        pass

    @abstractmethod
    def execute_order(self, order_details: dict) -> dict:
        """
        Submits a trade order (buy/sell) to the broker.

        Args:
            order_details (dict): A structured dictionary containing all necessary order
                                  parameters (ticker, quantity, order_type, direction, etc.).

        Returns:
            dict: A dictionary with the initial order confirmation and a unique broker_order_id.
        """
        pass

    @abstractmethod
    def get_order_status(self, broker_order_id: str) -> dict:
        """
        Checks the status of a previously submitted order using the broker's unique ID.

        Args:
            broker_order_id (str): The unique ID returned by the broker after order submission.

        Returns:
            dict: A dictionary with the order status (e.g., {'status': 'FILLED', ...}).
        """
        pass
