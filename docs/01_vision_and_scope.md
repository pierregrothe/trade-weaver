
# 1. Vision and Scope

## 1.1. Vision

To create a highly efficient, AI-driven trading platform that empowers a select group of sophisticated traders to optimize their investment strategies across global markets. The platform will prioritize execution speed, modularity, and robust portfolio tracking to deliver a distinct performance edge.

## 1.2. Target Audience

The initial user base is a small, private group of experienced traders who understand the risks associated with day trading. The application is a personal tool for the primary stakeholder and their close associates. It is not intended for the general public or novice investors at this stage.

## 1.3. Business Objectives

* **Personal Investment Optimization:** To serve as a primary tool for managing the personal investment portfolios of the initial user group.
* **Multi-Portfolio Management:** To accurately track capital, trades, and P&L for multiple distinct portfolios (e.g., for different friends contributing capital).
* **Efficiency and Latency:** To achieve the lowest possible latency in trade execution by leveraging high-performance APIs and a streamlined architecture.
* **Scalable Foundation:** To build a modular system that, while initially small-scale, is architected to be scalable for potential future growth without a complete redesign.

## 1.4. Scope

### In-Scope Features (Phase 1 - MVP)

*   User and Role Management (Admin, Tenant Manager, Portfolio Manager, Trader, Client).
*   Secure management of Broker API keys.
*   Multi-portfolio tracking with multi-currency support.
*   A configurable system for managing active markets and exchanges.
*   A `PreMarketAnalysis` to identify trade opportunities based on a quantitative, catalyst-driven scanning process.

### In-Scope Features (Phase 2 and Beyond)

*   A UI to display, approve, or reject trade opportunities generated in Phase 1.
*   An `Executor` to place trades in both "Live" and "Paper" modes.
*   Fully autonomous "YOLO" modes for both live and paper trading.
*   Compliance with Canadian (CIRO) trading regulations.

### Out-of-Scope Features (Future Considerations)

* Real-time, continuous online learning for the AI models. (Initial learning will be offline).
* Direct public/retail sign-up. Access is by invitation only.
* Compliance with regulations outside of Canada and the USA.
* Trading of asset classes other than public equities.
