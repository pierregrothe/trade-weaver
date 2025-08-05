# [CONCEPT: Tradable_Markets] A Comparative Analysis of Tradable Markets

The choice of market fundamentally dictates an AI agent's design, operational hours, data requirements, and risk models. This document compares the three primary markets for day trading.

| [PARAMETER: Feature] | [MARKET: Equities_Stocks] | [MARKET: Foreign_Exchange_Forex] | [MARKET: Digital_Assets_Crypto] |
| :--- | :--- | :--- | :--- |
| **Trading Hours** | Fixed daily hours (e.g., 9:30-16:00 ET); subject to **overnight gap risk**. | 24 hours/day, 5 days/week; continuous market, no gap risk. | **24/7/365; truly continuous operation.** No concept of "market close." |
| **Volatility Profile** | Moderate to high; driven by company/sector news and market sentiment. | High; driven by macroeconomic data and central bank policy. | **Extreme;** driven by sentiment, regulation, and technological news. Rapid and large price swings are frequent. |
| **Primary Liquidity** | Centralized exchanges (NYSE, Nasdaq). High for large-cap stocks. | Decentralized, over-the-counter (OTC) market. **Highest liquidity of any asset class.** | Decentralized; liquidity varies significantly across exchanges and assets. |
| **Key Drivers** | Earnings reports, corporate actions, analyst ratings, SEC filings. | Interest rate decisions, inflation data (CPI), employment reports, geopolitical events. | Regulatory news, technological adoption/upgrades, social media trends, major wallet movements. |
| **Primary Costs** | Commissions, bid-ask spread, **ECN fees**, payment for order flow. | **Primarily the bid-ask spread.** Commissions may apply on ECN accounts. | Exchange trading fees (maker/taker model), network withdrawal fees. |
| **Capital & Leverage** | Governed by rules like **[RULE: PDT]** in the US, requiring $25k for active trading. Leverage typically up to 4:1 intraday. | High leverage is common and accessible (e.g., 30:1 or 50:1), but also highly risky. | Varies by exchange; high leverage is available but extremely risky due to high volatility. |
| **Regulatory Oversight**| High (SEC, FINRA in U.S.; CIRO, AMF in Canada). | High (CFTC, NFA in U.S.; CIRO in Canada). | Evolving and varies significantly by jurisdiction. Highly fragmented globally. |
| **Required Data Feeds**| **[DATA: Level_2]** order book, **[DATA: Time_and_Sales]**, real-time news, economic calendar. | **[DATA: Economic_Calendar]**, central bank statements, real-time news feeds. | Real-time exchange data, **[DATA: Social_Media_Sentiment]** analysis, blockchain data feeds. |
| **AI Agent Implications**| Agent must manage overnight gap risk. Can operate on a fixed schedule. Needs strong catalyst identification module. | **Agent must be designed for 24/5 operation.** Must have an integrated, real-time economic calendar API to pause/react to major data releases. | **Agent must be designed for 24/7/365 continuous operation and risk management.** Requires extremely robust, automated risk controls (circuit breakers) to survive extreme volatility. Must be able to parse non-traditional data sources like social media. |

[SOURCE_ID: Day Trading AI Agent Research, Part I, Section 1.3]
