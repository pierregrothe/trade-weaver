# [CONCEPT: Operational_Cadence] Daily Routine and Operational Cadence

A structured and disciplined routine is the primary defense against emotional and impulsive trading. For an AI agent, this routine is a formal, programmable state machine that dictates which modules are active at different times of the day, adapting to the market's distinct phases of volatility and liquidity.

### [CONCEPT: System_State_Machine] Daily State Machine

The agent's master controller will transition the system through a series of states based on the time of day. Each state enables or disables specific strategy modules and permissions.

| [STATE: State] | [PARAMETER: Time_ET] | [TASK: Primary_Function] | [MODULE: Active_Strategy_Modules] | [DATA: Key_Data_Inputs_Modules] | [RULE: Constraints] |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Pre-Market** | 7:00 - 9:30 | Analysis & Planning | Universe Filtering, Gapper Scan, Catalyst ID | Bulk EOD Data, Pre-Market Price Feeds, Real-Time News API | **NO TRADING ALLOWED**. Order execution module is disabled. |
| **Open** | 9:30 - 11:30 | High Volatility Execution | Momentum & Breakout, VWAP-Based | Real-Time WebSocket (L1, L2, Tape), Order Execution API | Full risk deployment. Primary window for trend/breakout trades. |
| **Mid-Day** | 11:30 - 14:30 | Low Volatility Observation | Mean Reversion | Real-Time WebSocket (L1), Order Execution API | Reduced position sizing may be enforced. Momentum modules disabled. |
| **Close** | 14:30 - 16:00 | Position Flattening & Logging | None | Order Execution API, Position Management Module | No new positions initiated. **All open positions must be closed by 15:55 ET** to eliminate overnight risk. |
| **Post-Market** | After 16:00 | Performance Analysis & Retraining | Data Logging, Performance Analytics, ML Feedback Loop | Trade Log Database, Historical Data Store | **NO TRADING ALLOWED**. |

### [CONCEPT: Global_Market_Schedule] Global Market Schedule (Québec EST/EDT Perspective)

This schedule provides a map of global market activity, allowing the agent to identify key periods of high activity (session opens and overlaps) and low activity.

| [TIME_BLOCK: Time_EST] | [TASK: Daily_Activities] | [TASK: Weekly_Activities] | [TASK: Monthly_Activities] |
| :--- | :--- | :--- | :--- |
| 20:00 - 21:00 | Monitor Tokyo/Sydney open (APAC). Low-volume session. | - | - |
| 02:00 - 05:00 | Monitor/Trade London open (EMEA). High volatility in Forex. | - | - |
| **07:00 - 09:20** | **CRITICAL PREP:** Run US pre-market scanner. Build watchlist. Formulate daily trading plan. | - | - |
| **09:20 - 10:30** | **MAXIMUM VOLATILITY:** Execute A+ setups from watchlist. | - | - |
| 12:00 - 14:00 | **LUNCH LULL:** Avoid trading. Enter Mid-Day state. | - | - |
| 15:30 - 16:00 | Manage positions into the close. Enter Close state. | - | - |
| **16:00 - 17:00** | **CRITICAL REVIEW:** Journal all trades. Review performance. | Review all trades from the past week. Analyze performance stats. Identify recurring patterns/mistakes. | Review monthly P&L against goals. Assess strategy performance decay. Plan adjustments. |

[SOURCE_ID: AI Day Trading Blueprint, Section 5]
[SOURCE_ID: The Definitive Day Trading Manual for the Québec-Based Trader, Part 1]
