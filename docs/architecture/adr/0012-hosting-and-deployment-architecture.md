# ADR-0012: Hosting and Deployment Architecture

* **Status:** Proposed
* **Date:** 2025-08-04
* **Deciders:** [Your Name], AI Assistant

## Context and Problem Statement

We need to define the specific cloud infrastructure and deployment model for the Trade Weaver platform. The architecture must support our hybrid model (UI vs. Trading Engine), be secure, scalable, and cost-effective for our initial scale, while allowing for future growth.

## Decision Outcome

**Chosen option:** We will adopt a fully serverless architecture on Google Cloud, leveraging specific, managed services for each component of the platform.

### Architecture Components

| Component | Technology | Rationale |
| :--- | :--- | :--- |
| **UI Hosting** | Firebase Hosting | Simple, fast, global CDN for our web application assets. |
| **User Backend** | Firebase (Auth, Firestore), Cloud Functions | Provides a complete, secure, and real-time backend for the user-facing "Management Cockpit". |
| **Trading Engine** | **Google Cloud Run** | Hosts our containerized Python ADK application. It is serverless, secure, scales to zero, and is ideal for our event-driven workload. |
| **Communication** | Google Cloud Pub/Sub | Provides a reliable, asynchronous messaging backbone between the UI backend (Cloud Functions) and the Trading Engine (Cloud Run). |
| **Scheduling** | Google Cloud Scheduler | Triggers the `AnalyzerAgent` via Pub/Sub on a cron-based schedule. |
| **Security** | Google Secret Manager, IAM | Manages all secrets and enforces the principle of least privilege for our services. |

### Deployment Model

* The entire ADK application, including all agents (`analyzer`, `executor`, etc.), strategies, and core logic within the `src` directory, will be packaged into a **single container image**.
* This container image will be deployed as a **single Google Cloud Run service**.
* The application within the container will act as an event handler, listening for messages from Pub/Sub and invoking the appropriate ADK agent based on the message content.
* The modular folder structure is a **code organization and development pattern**, not a microservices deployment pattern. It ensures our single application is clean, maintainable, and easy to test.
