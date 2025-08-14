# ADR-0004: Backend Service Communication Protocol

* **Status:** Proposed
* **Date:** 2025-08-04
* **Deciders:** [Your Name], AI Assistant

## Context and Problem Statement

In our hybrid architecture, the Firebase backend (acting on behalf of the user via the UI) needs to communicate with the separate, secure Trading Engine service running on Cloud Run. We need to select a communication protocol that is secure, reliable, and appropriate for the types of interactions required (e.g., triggering trade executions, requesting analysis).

## Considered Options

* **Option 1: Synchronous REST API:** The Cloud Run service exposes a standard RESTful API (e.g., `POST /execute-trade`). The Firebase Cloud Function makes a direct HTTPS request and waits for a response. This is a simple, well-understood pattern.

* **Option 2: Asynchronous Messaging via Pub/Sub:** The Firebase Cloud Function publishes a "command" message (e.g., a trade request) to a Google Cloud Pub/Sub topic. The Cloud Run service subscribes to this topic, receives the message, and processes it asynchronously.

* **Option 3: gRPC:** Use a high-performance RPC framework for communication. This offers higher performance than REST but adds significant complexity in defining service contracts and managing client/server stubs.

## Decision Outcome

**Chosen option:** "Option 2: Asynchronous Messaging via Pub/Sub", supplemented by a REST API for synchronous queries.

### Justification

An asynchronous, event-driven approach using Pub/Sub is strategically superior for our core trading commands.

* **Reliability & Durability:** Pub/Sub guarantees message delivery. If the Trading Engine is temporarily down for an update or is busy, the trade request message is not lost. It will be processed as soon as the service is available. A synchronous REST call would simply fail and require complex retry logic in the client (the Cloud Function).
* **Scalability:** Pub/Sub is a massively scalable service that completely decouples the front-end application from the backend trading engine. We can scale the number of trading engine instances up or down without affecting the Firebase backend.
* **Responsiveness:** For the user, the action is instantaneous. The Firebase function publishes the message in milliseconds and can immediately return a "Trade submitted" status to the UI, without waiting for the trade to actually execute. The UI can then listen for a status update from Firestore.
* **Flexibility:** While Pub/Sub is ideal for commands, we will also expose a simple, secure REST API on the Cloud Run service for synchronous, read-only queries, such as fetching real-time performance benchmarks of the brokers.

This hybrid communication model gives us the reliability of messaging for critical commands and the simplicity of REST for simple queries.
