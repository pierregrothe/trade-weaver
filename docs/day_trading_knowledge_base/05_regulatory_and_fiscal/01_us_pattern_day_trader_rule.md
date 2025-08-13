# [JURISDICTION: US] The US Pattern Day Trader (PDT) Rule

This document provides a definitive explanation of the US Financial Industry Regulatory Authority (FINRA) Rule 4210, commonly known as the Pattern Day Trader (PDT) rule. This is the single most critical regulatory constraint for any agent trading U.S. equities.

### [RULE: PDT_Definition] Definition of a Pattern Day Trader

- **[CONCEPT: Day_Trade]** A "day trade" is the purchase and sale, or the short sale and subsequent covering, of the **same security** on the **same day** within a **margin account**.
- **[RULE: PDT_Test]** An account is designated as a PDT account if the holder executes **four or more day trades within a rolling five-business-day period**, provided that the number of these day trades constitutes more than 6% of the account's total trading activity over that same period.
- **[NOTE: Proactive_Designation]** Brokerage firms may also proactively designate an account as PDT if they have a reasonable basis to believe the client will engage in such activity.

### [RULE: Minimum_Equity_Requirement] The $25,000 Minimum Equity Requirement

- **[PARAMETER: MINIMUM_EQUITY_USD=25000]** Once an account is classified as a PDT, it must maintain a net liquidation value of at least **$25,000 USD** on any day that day trading occurs.
- **[LOGIC: Pre_Session_Check]** This equity must be in the account **prior to the commencement** of any day-trading activities.
- **[CONSEQUENCE: Trading_Restriction]** If the account's equity falls below the $25,000 threshold at the close of the previous business day, the trader is **prohibited from making any day trades** until the account is restored to the minimum level.

### [CONCEPT: DTBP] Day-Trading Buying Power (DTBP)

- **[DEFINITION: Buying_Power]** A PDT's leverage is strictly governed. DTBP is the maximum value of securities that can be day-traded during a single session.
- **[FORMULA: DTBP_Calculation]** DTBP is limited to **four times the trader's maintenance margin excess** as of the close of business on the previous day.
- **[CONSEQUENCE: Margin_Call]** Exceeding this limit results in a day-trading margin call.

### [CONCEPT: AI_Implementation] AI Implementation Logic

The AI agent's core compliance module must contain the following state variables and logic:

- **[STATE_VARIABLE: `day_trade_counter`]**: A persistent counter that tracks executed day trades on a rolling 5-day basis.
  - **[LOGIC:]** `ON_TRADE_CLOSE: IF trade.is_day_trade THEN increment_day_trade_counter()`.
  - **[RULE:]** `BEFORE_NEW_TRADE: IF day_trade_counter >= 3 AND account_equity < 25000 THEN REJECT_TRADE`. This prevents triggering the PDT flag on an undercapitalized account.
- **[STATE_VARIABLE: `is_pdt_flagged`]**: A boolean flag, set to `true` once the PDT rule is triggered.
- **[LOGIC: Daily_Capital_Check]** A mandatory, non-negotiable pre-session check:
  - `ON_SESSION_START: IF is_pdt_flagged == true AND get_previous_day_closing_equity() < 25000 THEN set_system_state('LIQUIDATE_ONLY')`.
- **[LOGIC: DTBP_Constraint]** The agent must query the broker API for the official `DayTradingBuyingPower` at the start of each session and use this value as an absolute constraint for all position sizing algorithms.

### [CONCEPT: Canadian_Trader_Implication] Key Takeaway for Canadian Traders

- **[RULE: Broker_Dependence]** While this is a U.S. rule, it is **enforced by some Canadian brokers (like Interactive Brokers)** on Canadian clients who trade U.S. stocks. Other brokers (like Questrade) do not. This single rule is often the most decisive factor in broker selection for a Canadian-based trader with less than $25,000 USD in capital.

[SOURCE_ID: Day Trading AI Agent Research, Part I, Section 1.2]
[SOURCE_ID: Day Trading with Canadian Brokers, Section 1.2]
