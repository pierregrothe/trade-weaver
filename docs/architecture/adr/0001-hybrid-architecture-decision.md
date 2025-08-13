# ADR-0001: Hybrid Architecture for Application and Trading Engine

* **Status:** Accepted
* **Date:** 2025-08-04
* **Deciders:** [Your Name], AI Assistant

## Context and Problem Statement

The Trade Weaver platform requires two distinct but connected components: a modern, real-time user-facing web application and a high-performance, low-latency trading engine. The user application needs to handle user authentication, data display, and portfolio management, prioritizing rapid development. The trading engine needs to handle market data analysis and trade execution, prioritizing performance, security, and operational control. We need an architecture that allows each component to excel without compromising the other.

## Considered Options

* **Option 1: Monolithic Architecture:** Build the entire application (front end, user management, trading logic) as a single, unified service.
* **Option 2: Hybrid Architecture:** Decouple the system into two specialized services:
    1. A **User-Facing Application** built on the Firebase ecosystem (including Firebase Studio, Authentication, Firestore) for the UI, user management, and data storage.
    2. A separate **Trading Engine** built with Google ADK, running as a containerized service on Google Cloud Run for maximum performance and isolation.

## Decision Outcome

**Chosen option:** "Option 2: Hybrid Architecture", because it allows us to use the best tool for each job.

### Positive Consequences

* **Performance:** The trading engine can be optimized purely for low-latency execution on Cloud Run without the overhead of serving a UI.
* **Rapid Development:** We can leverage Firebase and its tools to build the user management and dashboard components very quickly.
* **Security:** The sensitive trading logic and broker API keys are completely isolated in the Cloud Run service, creating a smaller, more secure attack surface.
* **Scalability & Modularity:** Each component can be scaled, updated, and maintained independently. This is a clean, professional architecture that supports future growth.

### Negative Consequences

* We will need to define and maintain a clear API contract for communication between the Firebase backend (e.g., via Cloud Functions) and the Cloud Run trading engine.
* Initial setup is slightly more complex as it involves managing two separate deployment targets.
