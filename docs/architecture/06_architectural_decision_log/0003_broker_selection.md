# ADR-0003: Primary Broker API Selection

* **Status:** Accepted
* **Date:** 2025-08-04
* **Deciders:** Pierre Grothé, AI Assistant

## Context and Problem Statement

The Trade Weaver platform requires a brokerage partner that can support its core functional and non-functional requirements. The primary requirements are:

1. A robust, low-latency API for algorithmic trade execution.
2. Direct and reliable data feeds for global equity markets (AMER, EMEA, APAC).
3. A cost structure, particularly for currency conversion, that is viable for an active, multi-market trading strategy.
4. A high-fidelity paper trading environment accessible via the API for agent training and validation.

## Considered Options

* **Option 1: Interactive Brokers (IBKR) Canada:** A broker known for its professional-grade platform, extensive API ecosystem, and broad international market access.
* **Option 2: Questrade:** A leading Canadian retail broker known for its user-friendly platform, modern REST API, and not enforcing the US PDT rule.

## Decision Outcome

**Chosen option:** "Option 1: Interactive Brokers (IBKR) Canada" will be the primary and initial broker integrated into the Trade Weaver platform.

### Justification

IBKR is strategically aligned with all of Trade Weaver's core, high-performance requirements:

* **Performance:** IBKR's offering of Direct Market Access (DMA) and a low-latency, socket-based TWS API provides a significant performance advantage over standard REST APIs for the high-frequency trading strategies we intend to deploy.
* **Global Reach:** IBKR's native support for over 150 global markets is a fundamental enabler for the platform's vision to operate across AMER, EMEA, and APAC.
* **Cost Efficiency:** The extremely low currency conversion fees at IBKR (vs. the high fees at Questrade) are a critical factor for the profitability of any strategy that trades non-CAD securities. This single factor makes IBKR the superior financial choice for a global trading system.
* **Professional Tooling:** The mature API and high-fidelity paper trading environment are better suited for the development and validation of a sophisticated AI agent.

Questrade remains a strong secondary option and a potential future integration, especially to cater to users who may not meet the US$25,000 PDT capital requirement for trading US stocks. However, for the primary goals of Trade Weaver, IBKR is the unequivocal choice.
