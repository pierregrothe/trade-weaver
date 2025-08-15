# [CONCEPT: Operational_Cadence] The Agent's Daily Operational State Machine

A structured and disciplined routine is the primary defense against impulsive, unanalyzed trading. For an AI agent, this routine is a formal, programmable state machine that dictates which modules are active at different times of the day, adapting to the market's distinct phases of volatility and liquidity.

### [CONCEPT: System_State_Machine] The Daily State Machine

The agent's master controller transitions the system through a series of states based on time and event triggers. Each state enables or disables specific strategy modules and risk parameters.

| State | Trigger | Primary Function | Key Output/Artifact | Constraints |
| :--- | :--- | :--- | :--- | :--- |
| **Offline** | System Start / EOD Complete | System is idle. | - | All modules inactive. |
| **Pre-Market** | 7:00 AM ET | **Analysis & Planning:** Distill market universe into a small, actionable watchlist. | `ranked_watchlist.json` | **NO TRADING ALLOWED**. Order execution module is disabled. |
| **Open** | 9:30 AM ET | **High Volatility Execution:** Capitalize on opening momentum and breakouts. | Live Trade Log | Full risk deployment (Max Risk = 1%). Momentum & Breakout modules enabled. |
| **Mid-Day** | 11:30 AM ET | **Low Volatility Observation:** Shift to mean-reversion and range-bound logic. | Live Trade Log | Reduced risk (Max Risk = 0.5%). Momentum modules disabled. Mean Reversion enabled. |
| **Close** | 2:30 PM ET | **Position Flattening & Logging:** Cease new entries and prepare for EOD. | Finalized Trade Log | No new positions initiated. **All open positions must be closed by 15:55 ET.** |
| **Post-Market** | 4:00 PM ET | **Performance Analysis & Retraining:** Journal, analyze, and adapt. | `performance_report.md`, `updated_model_parameters.json` | **NO TRADING ALLOWED**. |

### [CONCEPT: Global_Market_Schedule] Global Market Schedule (Québec EST/EDT Perspective)

This schedule provides a map of global market activity, allowing the agent to identify key periods of high activity (session opens and overlaps) that can influence U.S. market sentiment.

| Time Block (EST) | Daily Activities & Rationale | Weekly Activities | Monthly Activities |
| :--- | :--- | :--- | :--- |
| 20:00 - 21:00 | Monitor Tokyo/Sydney open (APAC). Low-volume session, but can set early tone for currency/commodity markets. | - | - |
| 02:00 - 05:00 | Monitor/Trade London open (EMEA). **High volatility in Forex & ADRs.** The London open often dictates the directional bias for the early part of the U.S. session. | - | - |
| **07:00 - 09:20** | **CRITICAL PREP:** Run US pre-market scanner. Ingest news. Build watchlist. Formulate daily trading plan and set initial market regime state. | - | - |
| **09:30 - 10:30** | **MAXIMUM VOLATILITY:** Execute A+ setups from watchlist. Focus on high-conviction breakout and momentum strategies. | - | - |
| 12:00 - 14:00 | **LUNCH LULL:** Avoid new trend-based trades. Shift to Mid-Day state. Monitor for mean-reversion opportunities. | - | - |
| 15:30 - 16:00 | Manage positions into the close. Enter Close state. No new entries. | - | - |
| **16:00 - 17:00** | **CRITICAL REVIEW:** Journal all trades. Run performance analytics module. Identify strategy decay or areas for optimization. | Review all trades from the past week. Analyze performance stats. Identify recurring patterns/mistakes. | Review monthly P&L against goals. Assess strategy performance decay. Plan adjustments. |

[SOURCE_ID: AI Day Trading Blueprint, Section 5]
[SOURCE_ID: The Definitive Day Trading Manual for the Québec-Based Trader, Part 1]
[SOURCE_ID: Algorithmic Trading State Machine Design Patterns]