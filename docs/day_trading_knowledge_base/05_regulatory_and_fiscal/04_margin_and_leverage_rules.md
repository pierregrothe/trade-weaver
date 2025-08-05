# [CONCEPT: Margin_and_Leverage] Margin and Leverage Rules

This document explains the mechanics of margin accounts, which are a necessity for day trading, and the power and peril of leverage.

### [CONCEPT: Margin_Account] Understanding Margin Accounts

- **[DEFINITION: Margin_Account]** A margin account is a brokerage account that functions as a **secured line of credit**. The broker lends the client money, using the securities in the account as collateral.
- **[REQUIREMENT: Day_Trading]** Day trading must be conducted in a margin account. A cash account is unsuitable due to trade settlement rules (T+1), which prevent the rapid redeployment of capital. In a margin account, buying power is instantly available after a trade is closed.

### [CONCEPT: Margin_Requirements] Margin Requirements (MR)

- **[DEFINITION: MR]** The Margin Requirement (MR) is the percentage of the trade's value that the trader must cover with their own equity (the "down payment").
- **[REGULATOR: CIRO]** In Canada, minimum MRs are set by CIRO, but brokerage firms can set stricter "house" requirements.
- **[LOGIC: Risk_Based_MR]** MRs vary by security risk: Low Risk (e.g., 30%), Standard (e.g., 50%), High Risk (100% - not marginable).
- **[RISK: Dynamic_MR]** Brokers can change the MR for any security at any time without notice, especially during high volatility.

### [CONCEPT: Leverage] Demystifying Leverage

- **[DEFINITION: Leverage]** Leverage is the resulting **amplification** of buying power from using margin.
- **[FORMULA: Leverage_Calculation]** `Leverage = 1 / Margin Requirement`.
  - 50% MR provides **2:1 leverage**.
  - 30% MR provides **3.33:1 leverage**.
- **[PRINCIPLE: Dual_Edged_Sword]** Leverage magnifies **both gains and losses** with equal force.

### [RISK: Margin_Call] Margin Calls: When Risk Becomes Reality

- **[TRIGGER: Equity_Drop]** A margin call is triggered when the trader's equity in the account (Market Value of Securities - Loan Balance) falls below a specified **maintenance margin** level (e.g., 25% of the market value).
- **[CONSEQUENCE: Forced_Liquidation]** If the trader fails to meet the call by depositing more funds, the brokerage has the **right to forcibly liquidate positions** without the trader's consent.

### [CONCEPT: Margin_Call_Example] Quantitative Example of a Margin Call

An AI agent must be able to run this calculation continuously to monitor its margin health.

- **Setup:**
  - Trader deposits **$10,000** cash (Initial Equity).
  - Broker has a **50%** initial margin and a **30%** maintenance margin requirement.
  - Trader uses 2:1 leverage to buy **$20,000** of stock XYZ.
    - Account State:
      - Market Value of XYZ: $20,000
      - Loan from Broker: $10,000
      - Trader's Equity: $10,000 ($20,000 - $10,000)

- **Market Price Drops:**
  - The market value of XYZ drops by 20% to **$16,000**.
    - Account State:
      - Market Value of XYZ: $16,000
      - Loan from Broker: $10,000 (this is fixed)
      - Trader's Equity: **$6,000** ($16,000 - $10,000)

- **Margin Call Check:**
    1. **Calculate Required Maintenance Equity:** `Market Value * Maintenance Margin %`
        `$16,000 * 30% = $4,800`. The trader must have at least $4,800 of their own equity.
    2. **Compare Actual vs. Required:**
        - Actual Equity: **$6,000**
        - Required Equity: **$4,800**
    3. **Result:** Since `$6,000 > $4,800`, there is **no margin call** yet. The trader has an excess margin of $1,200.

- **Further Price Drop (Triggering the Call):**
  - The market value of XYZ drops to **$14,000**.
    - Account State:
      - Market Value of XYZ: $14,000
      - Loan from Broker: $10,000
      - Trader's Equity: **$4,000** ($14,000 - $10,000)
  - **Margin Call Check:**
        1. Required Maintenance Equity: `$14,000 * 30% = $4,200`.
        2. Compare: Actual Equity ($4,000) is **less than** Required Equity ($4,200).
        3. **Result: MARGIN CALL ISSUED.** The trader must deposit funds or the broker will begin to forcibly sell their shares.

[SOURCE_ID: Day Trading with Canadian Brokers, Part II]
