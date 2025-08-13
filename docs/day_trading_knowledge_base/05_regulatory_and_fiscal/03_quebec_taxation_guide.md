# [JURISDICTION: Quebec] Québec Taxation Guide for Day Traders

This document is a detailed fiscal guide for day traders based in Québec. A professional day trader's activities will, by definition, be classified as a business. This is not optional; it is a determination based on the pattern of activity.

### [CONCEPT: Business_Income] Business Income vs. Capital Gains

The Canada Revenue Agency (CRA) and Revenu Québec use a multi-factor test to determine a trader's status. A day trader exhibiting high frequency, short holding periods, specialized knowledge, and significant time commitment will be deemed to be **carrying on a business**.

The following table compares the two tax treatments in Québec.

| [PARAMETER: Factor] | [CLASSIFICATION: Business_Income_Trader] | [CLASSIFICATION: Capital_Gains_Investor] |
| :--- | :--- | :--- |
| **Inclusion Rate** | **100% of net income is taxable** at the trader's progressive marginal rate (up to 53.31%). | **50% of the net capital gain** is included in income and taxed at the investor's marginal rate. |
| **Treatment of Losses** | Business losses are **fully deductible against any other source of income** (e.g., employment income). | Capital losses can **only be used to offset capital gains**. |
| **Deductible Expenses** | A wide range of legitimate business expenses are **fully deductible**. | Deductibility is extremely limited to direct transaction costs. |
| **CPP/QPP Contributions**| Net business income is self-employment income and is **subject to mandatory CPP/QPP contributions**. | Capital gains are investment income and are **not subject to CPP/QPP contributions**. |

### [CONCEPT: Corporate_Structure] Sole Proprietorship vs. Corporation in Québec

The optimal legal structure evolves with the profitability of the trading operation.

- **[PHASE: Startup] Startup / Unproven Profitability: Sole Proprietorship.**
  - **[RATIONALE: Loss_Deductibility]** The ability to deduct initial business losses against other personal income is a critical financial advantage.
  - **[RATIONALE: Low_Overhead]** Administrative complexity and costs are minimal.

- **[PHASE: Profitable] Consistent Profitability: Consider Incorporation.**
  - **[PARAMETER: Tipping_Point]** The "tipping point" to consider incorporation is reached when annual net trading profits consistently exceed **CAD $150,000**.
  - **[RATIONALE: Tax_Deferral]** The corporate tax rate (General: 26.50%) is substantially lower than high personal marginal rates, allowing more capital to be retained for compounding.
  - **[RATIONALE: Liability_Protection]** A corporation provides limited liability, protecting personal assets.
  - **[HURDLE: SBD_Eligibility]** To qualify for the preferential Small Business Deduction (SBD) rate of 12.20%, Québec requires that the corporation's employees be paid for at least **5,500 hours annually**, a difficult threshold for a single owner-operator. A consultation with a tax professional is mandatory.

### [CONCEPT: AI_Directives] Key AI Agent Directives

The AI's financial and logging module must be programmed with the following directives:

1. **[DIRECTIVE: Default_Status]** The agent's default operational status is **Sole Proprietor**.
2. **[DIRECTIVE: Tax_Forms]** The agent's annual reporting module must be configured to output data formatted for **Form T2125** (Statement of Business or Professional Activities).
3. **[DIRECTIVE: Expense_Tracking]** The agent must meticulously log all operational costs into a database with the category "Deductible Business Expense." This includes:
    - `Data Feed Subscriptions`
    - `Charting and Journaling Software Fees`
    - `Computer Hardware (for Capital Cost Allowance calculation)`
    - `Home Office Expenses (proportionate share of rent, utilities, internet)`
    - `Accounting and Legal Fees`
    - `Interest on money borrowed to trade (margin interest)`
4. **[DIRECTIVE: Incorporation_Alert]** The agent must track its rolling 12-month net profit. `IF rolling_12_month_net_profit > 150000 CAD THEN TRIGGER_ALERT("High-Priority: Consult tax professional regarding incorporation benefits.")`.

[SOURCE_ID: AI Day Trading Blueprint, Section 1.1]
[SOURCE_ID: The Definitive Day Trading Manual for the Québec-Based Trader, Part 2]
