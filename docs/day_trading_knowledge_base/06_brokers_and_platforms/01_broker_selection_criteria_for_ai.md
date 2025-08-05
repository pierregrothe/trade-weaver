# [CONCEPT: Broker_Selection] Broker Selection Criteria for an AI Agent

The choice of brokerage is a critical architectural decision for an AI trading agent. The platform must be evaluated as a foundational component of the agent's infrastructure, not just a transactional service.

### [CONCEPT: Decision_Hierarchy] Ranked Decision-Making Hierarchy for AI Agent

The AI agent must evaluate potential brokers in a strict, hierarchical order. A failure at a higher-level criterion disqualifies the broker, regardless of its strengths in lower-level criteria.

1. **[CRITERIA_RANK: 1] API Access (Non-Negotiable Prerequisite):** Does the broker provide a robust, official, and well-documented API with access to a high-fidelity paper trading environment? If not, the broker is **disqualified**.
2. **[CRITERIA_RANK: 2] Regulatory Compliance & Market Access:** Does the broker's regulatory stance (e.g., enforcement of the PDT rule) align with the agent's available capital and target markets (US/Canada)? If the agent's capital is < $25k and it needs to trade US stocks, a broker enforcing the PDT rule is **disqualified**.
3. **[CRITERIA_RANK: 3] Total Cost Structure:** What is the total cost of trading, including not just commissions but also hidden costs like currency conversion and ECN fees? This determines the strategy's profitability threshold.
4. **[CRITERIA_RANK: 4] Execution and Data Features:** Does the platform provide the necessary low-latency data feeds and advanced order types required for the agent's strategies?

### [CRITERIA: API_Access] Detailed Criteria: API Access

- **[REQUIREMENT: Public_Official_API]** The API must be public, officially supported, and actively maintained by the broker. Reliance on unofficial, community-maintained wrappers is an unacceptable architectural risk for a production system.
- **[REQUIREMENT: API_Paper_Trading]** The API **must** provide full access to an integrated paper trading (simulation) environment. This is essential for strategy validation, forward testing, and agent training without risking capital.
- **[REQUIREMENT: Language_Support]** Strong preference for brokers with official, first-party **Python** client libraries.

### [CRITERIA: Cost_Structure] Detailed Criteria: Total Cost Structure

- **[COST: Commissions]** Per-trade or per-share fees.
- **[COST: ECN_Fees]** Fees charged for removing liquidity, which can be a significant cost for strategies using market orders. A "$0 commission" model is not truly zero if ECN fees apply.
- **[COST: Currency_Conversion]** For agents trading across borders (e.g., Canada/US), the FX fee is a critical cost. A fee of 1.5% can be more significant than commissions over many trades. Look for brokers offering near-spot rates.
- **[COST: Market_Data]** Fees for Level 1 and Level 2 data are a mandatory business expense and must be factored into the total cost.

### [CRITERIA: Execution_and_Data] Detailed Criteria: Execution and Data Features

- **[FEATURE: Low_Latency]** The broker must provide low-latency order execution to minimize **[CONCEPT: Slippage]**.
- **[FEATURE: Data_Feeds]** The broker must provide a reliable, real-time API stream for **[DATA: Level_2]** market data.
- **[FEATURE: Advanced_Orders]** The API must support advanced order types, with **[TYPE: Bracket_Orders]** being a mandatory requirement for programmatic risk management.

[SOURCE_ID: Day Trading AI Agent Research, Part II, Section 2.1]
[SOURCE_ID: Canadian Broker for AI Trading, Introduction]
