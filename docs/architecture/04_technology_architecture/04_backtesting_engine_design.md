# Backtesting Engine Design

This document describes the design and technology choice for the backtesting engine used to validate all trading strategies, as decided in ADR-0009.

## 1. Core Requirement

To validate trading strategies and prevent financial loss, the project requires a robust backtesting engine that can simulate strategy performance against historical market data with high fidelity. The engine must be designed to avoid common and catastrophic pitfalls like survivorship bias and look-ahead bias.

## 2. Design Decision: Leverage Open Source

Instead of building a complex, time-consuming custom backtesting engine from scratch, the project will **utilize an existing, mature open-source backtesting library**. This approach provides several key advantages:

-   **Speed of Development:** Allows the team to focus on strategy development and alpha generation, which is the unique value of the project.
-   **Reliability:** Leverages battle-tested and well-documented libraries, reducing the risk of subtle bugs in the core simulation logic.
-   **Bias Mitigation:** Mature libraries provide clear patterns and tools for handling historical data correctly, helping to avoid common biases.

## 3. Recommended Technology

The primary candidate for initial implementation is the **`backtrader`** library.

-   **Rationale:** `backtrader` is a powerful, popular, and well-documented Python library for backtesting trading strategies. It has a strong community and has solved many of the complex problems associated with historical data simulation.

## 4. Implementation Note: The Adapter Layer

To integrate our proprietary agent and strategy formats with the chosen backtesting library, we will need to develop an **"adapter" layer**. This layer will be responsible for translating our internal data structures and strategy signals into the format required by the `backtrader` API. This is a standard and accepted trade-off for the significant development speed gained by using an external library.
