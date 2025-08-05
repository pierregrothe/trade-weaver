# [CONCEPT: Broker_Comparison] Broker Comparison and Strategic Recommendations

The optimal broker choice is a function of the AI agent's available capital, target markets, and primary strategic objectives. This document provides a direct comparison and a decision-making framework.

### [CONCEPT: Head_to_Head_Comparison] Head-to-Head Feature Comparison

| [PARAMETER: Feature] | [BROKER: Interactive_Brokers] | [BROKER: Questrade] | [ANALYSIS: Key_Differentiator] |
| :--- | :--- | :--- | :--- |
| **PDT Rule (U.S. Stocks)**| **Enforced.** Requires **US$25,000** min. equity. | **Not Enforced.** No minimum equity for U.S. trading. | **This is the primary decision gate for under-capitalized agents.** |
| **Currency Conversion Cost** | **Extremely Low (~0.002%)** | **High (~1.5%)** | **This is the primary cost differentiator for cross-border trading.** |
| **Commissions (Active)** | Low (Per-share model) | Moderate (ECN fees apply on liquidity-taking orders) | IBKR is generally cheaper for high-frequency trading. |
| **API Complexity** | High (Powerful, steep learning curve) | Moderate (Modern REST API, easier integration) | Trade-off between power and ease of development. |
| **Platform Complexity** | High (TWS is for professionals) | Moderate (Edge is more user-friendly) | TWS offers more power at the cost of complexity. |

### [CONCEPT: Decision_Flowchart] Decision Flowchart for AI Agent

The agent should follow this logic to determine the optimal broker:

1. **[QUESTION: Capital_and_Market]** Does the agent need to trade U.S. stocks AND have less than $25,000 USD in capital?
    - **[ANSWER: Yes]** -> **[CHOICE: Questrade]**. It is the only viable option to bypass the PDT rule. The agent's architecture **must** include a module to manage a USD cash balance to mitigate the high FX fees.
    - **[ANSWER: No]** -> Proceed to Question 2.

2. **[QUESTION: Primary_Objective]** Is the agent's primary objective to minimize long-term operational costs for a high-frequency, cross-border strategy?
    - **[ANSWER: Yes]** -> **[CHOICE: Interactive_Brokers]**. The massive savings on currency conversion and lower margin rates provide a superior Total Cost of Ownership (TCO), justifying the higher complexity.
    - **[ANSWER: No]** -> Proceed to Question 3.

3. **[QUESTION: Focus_Market]** Is the agent's focus primarily on Canadian markets with a lower trade frequency?
    - **[ANSWER: Yes]** -> **[CHOICE: Questrade]**. The user-friendly platform and simpler commission model (with no FX fees to consider) can be more advantageous and easier to manage.
    - **[ANSWER: No]** -> Default to **[CHOICE: Interactive_Brokers]** for its superior cost structure and professional-grade infrastructure.

### [CONCEPT: Architectural_Summary] Architectural Summary

- **Choose Interactive Brokers for a `PERFORMANCE_AND_COST_OPTIMIZED` architecture.** This choice accepts higher development complexity in exchange for the lowest possible long-term operational costs and the most powerful toolset. It is the professional-grade choice for well-capitalized systems.
- **Choose Questrade for an `ACCESSIBILITY_OPTIMIZED` architecture.** This choice prioritizes easier market access for under-capitalized systems and a simpler development experience, at the cost of significantly higher fees (especially currency conversion) that must be actively managed.

[SOURCE_ID: Day Trading with Canadian Brokers, Part III & Section 4.2]
