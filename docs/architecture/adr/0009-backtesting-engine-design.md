# ADR-0009: Backtesting Engine Design

* **Status:** Proposed
* **Date:** 2025-08-04
* **Deciders:** [Your Name], AI Assistant

## Context and Problem Statement

To validate trading strategies and prevent financial loss, we must have a robust backtesting engine. The engine needs to simulate strategy performance against historical market data with high fidelity. It must be designed to avoid common and catastrophic pitfalls like survivorship bias and look-ahead bias.

## Considered Options

* **Option 1: Build a Custom Backtesting Engine:** Develop a bespoke engine from scratch. This offers maximum control but is a massive, complex undertaking.
* **Option 2: Utilize an Existing Open-Source Library:** Leverage a mature, community-vetted backtesting library like `backtrader` or `Zipline`. These libraries have already solved many of the complex problems associated with historical data simulation.

## Decision Outcome

**Chosen option:** "Option 2: Utilize an Existing Open-Source Library", with `backtrader` being the primary candidate.

### Positive Consequences

* **Speed of Development:** We can build our validation system in a fraction of the time by leveraging a powerful, existing framework.
* **Reliability:** These libraries are battle-tested and well-documented, reducing the risk of subtle bugs in our simulation logic.
* **Bias Mitigation:** Mature libraries often have built-in protections or clear patterns for avoiding survivorship and look-ahead bias.
* **Focus:** We can focus our development effort on the *strategies themselves*, not on building the underlying simulation plumbing.

### Negative Consequences

* We will be dependent on an external library and its maintenance lifecycle.
* We may need to write adapter code to integrate our custom data sources and strategy format with the library's API.
