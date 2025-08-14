# ADR-0009: Backtesting Engine Design

* **Status:** Proposed
* **Date:** 2025-08-04
* **Deciders:** [Your Name], AI Assistant

## Context and Problem Statement

To validate trading strategies and prevent financial loss, we must have a robust backtesting engine. The engine needs to simulate strategy performance against historical market data with high fidelity. It must be designed to avoid common and catastrophic pitfalls like survivorship bias and look-ahead bias. A custom-built engine is a massive, complex undertaking that would divert focus from our core goal of creating effective trading strategies.

## Considered Options

* **Option 1: Build a Custom Backtesting Engine:** Develop a bespoke engine from scratch. This offers maximum control but is a major software project in itself.
* **Option 2: Utilize an Existing Open-Source Library:** Leverage a mature, community-vetted backtesting library like `backtrader` or `Zipline`. These libraries have already solved many of the complex problems associated with historical data simulation.

## Decision Outcome

**Chosen option:** "Option 2: Utilize an Existing Open-Source Library", with **`backtrader`** being the primary candidate for initial implementation.

### Positive Consequences

* **Speed of Development:** We can build our validation system in a fraction of the time by leveraging a powerful, existing framework. This lets us focus on strategy development, which is our unique value.
* **Reliability:** `backtrader` is a battle-tested and well-documented library, reducing the risk of subtle bugs in our simulation logic.
* **Bias Mitigation:** Mature libraries provide clear patterns and tools for handling historical data correctly, helping us avoid common biases.

### Negative Consequences

* We will be dependent on an external library's API and maintenance lifecycle.
* We will need to write an "adapter" layer to make our custom strategy format compatible with the `backtrader` API. This is a standard and acceptable trade-off.
