# ADR-0005: Data Persistence Model

* **Status:** Proposed
* **Date:** 2025-08-04
* **Deciders:** Pierre Grothé, AI Assistant

## Context and Problem Statement

Trade Weaver requires a database to store all user-facing and operational data, including user profiles, portfolio details, trading strategies, historical trades, and real-time trade opportunities. The chosen database must integrate seamlessly with our hybrid architecture (Firebase and Cloud Run), support real-time updates for the UI, and be scalable for future growth.

## Considered Options

* **Option 1: Relational Database (e.g., Google Cloud SQL - PostgreSQL):** A traditional SQL database offers a rigid schema, strong consistency, and powerful querying capabilities. This is the standard for transactional integrity.
* **Option 2: NoSQL Document Database (Google Firestore):** A flexible, JSON-like document database that is part of the Firebase ecosystem. It is designed for real-time data synchronization with web and mobile clients and offers massive scalability.

## Decision Outcome

**Chosen option:** "Option 2: Google Firestore", because its native integration with our chosen Firebase/Cloud Run stack provides an unparalleled velocity and feature set for our specific needs.

### Positive Consequences

* **Real-time UI:** Firestore's real-time listeners are a killer feature for the "Management Cockpit". The UI can subscribe to data changes (e.g., new trade opportunities, P&L updates) and update instantly without needing to poll the server.
* **Seamless Integration:** It integrates natively with Firebase Authentication for security rules and with Cloud Functions for our event-driven backend logic (e.g., triggering the `ExecutorAgent`).
* **Flexible Schema:** As a NoSQL database, it allows us to easily evolve our data models as we add new features, which is ideal for an agile project.
* **Serverless & Scalable:** It's a fully managed, serverless database that scales automatically. We don't need to manage infrastructure.

### Negative Consequences

* Complex analytical queries (e.g., "show me the average holding time for all winning trades in the EMEA market for the last quarter") can be more difficult than in SQL. We can mitigate this by exporting data to BigQuery for complex analysis if needed in the future.

### High-Level Data Model

We will start with the following core Firestore collections, which are detailed exhaustively in the canonical **[Firestore Database Schema](../02-firestore-database-schema.md)** document:

* `Users`: Stores user profile information and roles.
* `Portfolios`: Main collection tracking capital, P&L, and settings for each investment pool.
* `Markets`: Configuration for addressable global markets (AMER, EMEA, APAC).
* `Exchanges`: Detailed configuration for each stock exchange, including its pre-market mechanism.
* `Strategies`: A registry of available trading strategy modules and their parameters.
* `DailyWatchlists`: Stores the ranked output of the pre-market analysis for a given day.
* `TradeSignals`: An immutable log of every potential trade identified by the analysis pipeline.
* `Trades`: An immutable log of all executed trades.
