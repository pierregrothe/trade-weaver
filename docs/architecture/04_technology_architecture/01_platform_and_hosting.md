# Platform and Hosting Architecture

This document defines the specific cloud infrastructure and deployment model for the Trade Weaver platform, as decided in ADR-0012. The architecture is fully serverless on Google Cloud, leveraging specific, managed services for each component.

## 1. Architecture Components

The platform is composed of the following managed services:

| Component | Technology | Rationale |
| :--- | :--- | :--- |
| **UI Hosting** | Firebase Hosting | Simple, fast, global CDN for our web application assets. |
| **User Backend** | Firebase (Auth, Firestore), Cloud Functions | Provides a complete, secure, and real-time backend for the user-facing "Management Cockpit". |
| **Trading Engine** | **Google Cloud Run** | Hosts our containerized Python ADK application. It is serverless, secure, scales to zero, and is ideal for our event-driven workload. |
| **Communication** | Google Cloud Pub/Sub | Provides a reliable, asynchronous messaging backbone between the UI backend (Cloud Functions) and the Trading Engine (Cloud Run). |
| **Scheduling** | Google Cloud Scheduler | Triggers the `AnalyzerAgent` via Pub/Sub on a cron-based schedule. |
| **Security** | Google Secret Manager, IAM | Manages all secrets and enforces the principle of least privilege for our services. |

## 2. Deployment Model

The deployment model is designed for simplicity and maintainability:

- The entire ADK application, including all agents (`analyzer`, `executor`, etc.), strategies, and core logic, will be packaged into a **single container image**.
- This container image will be deployed as a **single Google Cloud Run service**.
- The application within the container acts as an event handler, listening for messages from Pub/Sub and invoking the appropriate ADK agent based on the message content.
- The modular folder structure (e.g., `pre_market_analysis/`) is a **code organization and development pattern**, not a microservices deployment pattern. It ensures our single application is clean, maintainable, and easy to test.
