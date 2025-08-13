# [CONCEPT: Post_Trade_Analysis] Advanced Post-Trade Analysis: MFE and MAE

This document details an advanced post-trade analysis technique using Maximum Favorable Excursion (MFE) and Maximum Adverse Excursion (MAE). This analysis is critical for quantitatively optimizing the placement of stop-loss and take-profit orders, moving from subjective guesses to data-driven parameters.

### [PRINCIPLE: MFE_MAE_Defined] Defining MFE and MAE

-   **[CONCEPT: MFE] Maximum Favorable Excursion (MFE):** For a single trade, MFE is the maximum potential profit that was reached during the life of the trade. It measures how far the trade moved in the trader's favor.
-   **[CONCEPT: MAE] Maximum Adverse Excursion (MAE):** For a single trade, MAE is the maximum potential loss that was reached during the life of the trade (i.e., the largest drawdown). It measures how far the trade moved against the trader.

### [IMPLEMENTATION: Calculation] Calculation and Data Logging

To perform this analysis, the agent's trade journaling system must be enhanced to log MFE and MAE for every single trade. This requires the system to track the highest and lowest price reached between the entry and exit of each position.

-   **For a Long Position:**
    -   `MFE = Highest_Price_During_Trade - Entry_Price`
    -   `MAE = Entry_Price - Lowest_Price_During_Trade`
-   **For a Short Position:**
    -   `MFE = Entry_Price - Lowest_Price_During_Trade`
    -   `MAE = Highest_Price_During_Trade - Entry_Price`

These values should be stored in the trade log database alongside the other performance metrics.

### [USE_CASE: Optimizing_Stops] Using MAE to Optimize Stop-Loss Placement

By analyzing the distribution of MAE values for *winning* trades, we can set more intelligent stop-losses.

-   **[ANALYSIS]** Plot a histogram or cumulative distribution function (CDF) of the MAE values for all winning trades for a given strategy. This plot answers the question: "How much heat do my winning trades typically take before moving in my favor?"
-   **[OPTIMIZATION]** If we find that 95% of our winning trades have an MAE of less than 1.5 times the ATR, then setting our initial stop-loss at 2.0 times the ATR is a statistically sound choice. It gives our trades enough room to breathe and avoids being stopped out prematurely on what would have otherwise been winning positions.

### [USE_CASE: Optimizing_Targets] Using MFE to Optimize Take-Profit Placement

By analyzing the MFE of all trades, we can set more effective profit targets.

-   **[ANALYSIS]** Plot the distribution of MFE values for all trades for a given strategy. This plot answers the question: "When my trades work, how far do they typically run?"
-   **[OPTIMIZATION]** If the analysis shows that the vast majority of trades have an MFE that clusters around a 3:1 reward-to-risk ratio, it suggests that setting a profit target at 3R is optimal. It also reveals if we are consistently leaving too much money on the table by taking profits too early.

### [CONCEPT: ADK_Implementation] ADK Implementation Pattern

-   **[TOOL: `TradeJournalingTool`]** The `FunctionTool` responsible for logging trades must be updated to calculate and store the MFE and MAE for each trade.
-   **[AGENT: `PerformanceAnalysisAgent`]** A post-market `LlmAgent` or `SequentialAgent` will be responsible for the MFE/MAE analysis. It will:
    1.  Call a `FunctionTool` to query the trade log database for all trades related to a specific strategy.
    2.  Call another `FunctionTool` that uses libraries like `pandas` and `matplotlib` to perform the statistical analysis and generate the MFE/MAE distribution plots.
    3.  The agent can then use these results to recommend or even automatically adjust the stop-loss and take-profit parameters for the strategy in the system's configuration store.

[SOURCE_ID: Maximum Favorable Excursion and Maximum Adverse Excursion in trading Research]
