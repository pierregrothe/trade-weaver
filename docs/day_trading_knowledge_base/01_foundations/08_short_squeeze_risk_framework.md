# [CONCEPT: Short_Squeeze_Risk] A Quantitative Framework for Pre-Trade Short Squeeze Risk Assessment

This document provides a systematic, multi-factor framework for assessing the probability and potential magnitude of a short squeeze. Its core output is a composite **Squeeze Risk Score** designed as a robust, pre-trade diagnostic tool to prevent catastrophic losses.

### [PRINCIPLE: Anatomy_of_a_Squeeze] 1. Anatomy of a Short Squeeze: Core Diagnostic Variables

A short squeeze is a feedback loop of forced buying into a constrained supply of shares. The key variables measure this imbalance.

- **[VARIABLE: Short_Interest_Float] Short Interest % of Float:** The percentage of a company's tradable shares that are sold short. This is the fuel for the squeeze. *Data Nuance: This data is self-reported by brokers and published with a significant lag (twice a month), making it a useful but incomplete indicator.*
- **[VARIABLE: Days_to_Cover_DTC] Days to Cover (DTC):** Estimates the number of days it would take for all shorts to cover their positions based on average volume. It measures exit congestion.
- **[VARIABLE: Float_and_Float_Rotation] Float Size and Rotation:** The float is the available supply of shares. Low-float stocks (<20M shares) are more fragile. Float Rotation (`Current Day's Volume / Float Size`) is the intraday accelerator; a value > 1.0 indicates a speculative frenzy.
- **[VARIABLE: Borrow_Rate_and_Utilization] Cost to Borrow (CTB) & Utilization:** The most important real-time indicators. Utilization is the percentage of the lendable supply currently on loan. A high CTB (>50%) and Utilization (>90%) signal that the supply of lendable shares is nearly exhausted, meaning bearish pressure is capped.

### [CONCEPT: Risk_Score_Model] 2. The Squeeze Risk Score: A Composite Model

This model assigns points to each metric to create a single, actionable score. A high score indicates a fragile market structure where any catalyst could trigger a violent squeeze.

| Metric | Low Risk (0 pts) | Moderate Risk (1 pt) | High Risk (2 pts) | Extreme Risk (3 pts) |
| :--- | :--- | :--- | :--- | :--- |
| **Short Interest %** | < 10% | 10% - 20% | 20% - 40% | > 40% |
| **Days to Cover (DTC)** | < 3 Days | 3 - 7 Days | 7 - 10 Days | > 10 Days |
| **Cost to Borrow (CTB)**| < 20% | 20% - 80% | > 80% | - |
| **Utilization Rate** | < 90% | 90% - 95% | > 95% | - |
| **On Reg SHO List** | No | - | Yes | - |

**Risk Level Calculation:**
- **Total Score 1-3: Low Squeeze Risk.** Standard trading protocols apply.
- **Total Score 4-6: Elevated Squeeze Risk.** The stock is vulnerable. Shorting requires a clear invalidation level, a 50% reduction in standard position size, and a strict time stop.
- **Total Score 7+: Extreme Squeeze Risk.** The market structure is critically fragile. **Shorting should be avoided entirely.** Common bearish patterns will likely fail.

### [CONCEPT: Intraday_Risk_Protocol] 3. Intraday Risk Mitigation Protocol for High-Score Stocks

When the Squeeze Risk Score is 4 or higher, standard risk management is insufficient. The following protocol is designed to prioritize survival.

- **[RULE: Position_Sizing] Score-Adjusted Position Sizing:** The percentage of capital risked per trade must be dynamically adjusted.
    - **Score 4-6 (Elevated):** Max risk must be reduced to **0.5%** of account equity.
    - **Score 7+ (Extreme):** Max risk must be reduced to **0.25%** of account equity, or preferably, the trade should be avoided.
- **[RULE: Stop-Loss_Placement] Volatility-Adjusted Stops:** Use wider stops based on the Average True Range (ATR) to prevent being stopped out by noise. A stop placed at **2 to 3 times the current 5-minute ATR** is appropriate.
- **[RULE: Time_Stops] The Time Stop for Stagnant Setups:** The thesis for shorting a high-risk stock is that it should be a quick "fake-out." If it consolidates near its highs instead of reversing, the risk increases with every passing minute. **Rule:** *If a short position in a stock with a score > 4 has not shown positive P&L within 30 minutes of entry, the position must be closed.*

### [CONCEPT: Regulatory_Interaction] 4. The SSR-LULD Whip: A Predictable Failure Pattern

The interaction between the Short Sale Restriction (SSR) and a Limit Up-Limit Down (LULD) halt creates a predictable trap for short sellers.

- **The Mechanism:** A sharp sell-off triggers the SSR. The lack of short-selling pressure makes the order book fragile. A long-seller can now more easily trigger a LULD halt to the downside. During the halt, the market recognizes that the reopening auction is **structurally biased to the upside** because the SSR prevents shorts from placing aggressive sell orders. Buyers bid aggressively into the auction, and the stock reopens with a violent gap up, creating the "whip."
- **The Counter-Intuitive Trade:** This pattern is so reliable that it can become an actionable, high-risk **long** setup for traders who understand the mechanics.

[SOURCE_ID: Day Trader Short Squeeze Risk Score Analysis]
[SOURCE_ID: SSR and LULD Trading Interactions]