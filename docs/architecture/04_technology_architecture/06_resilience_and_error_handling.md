# Resilience and Error Handling Patterns

This document outlines the architectural patterns required to ensure the Trade Weaver platform is resilient to common real-world failures. A profitable strategy is irrelevant if the system executing it is not fault-tolerant.

## 1. Messaging Resilience (Pub/Sub)

Given the system's reliance on Pub/Sub for asynchronous communication, handling message processing failures is critical.

### Pattern: Dead-Letter Queue (DLQ)

- **Problem:** A message from a topic cannot be processed successfully by a subscriber (e.g., the agent service) due to a bug, data corruption, or other persistent error. Retrying indefinitely would block the processing of subsequent messages.
- **Solution:** Each Pub/Sub subscription MUST be configured with a **Dead-Letter Queue (DLQ)**. If a message fails processing a configured number of times (e.g., 5), Pub/Sub will automatically move the problematic message to the DLQ.
- **Action:** An alert will be triggered when a message enters a DLQ, notifying the development team to investigate the failed message without halting the main processing pipeline.

### Pattern: Idempotent Consumers

- **Problem:** Due to the "at-least-once" delivery guarantee of Pub/Sub, it is possible for a subscriber to receive the same message more than once. If processing a message twice has unintended side effects (e.g., placing the same trade twice), the system is not safe.
- **Solution:** All agent services that consume messages MUST be designed as **idempotent consumers**. The agent must track the `event_id` of messages it has already processed. If a message with a previously processed ID is received, the agent will acknowledge and discard it without reprocessing it.

## 2. External Service Resilience (API Calls)

When interacting with external APIs (e.g., Broker, Data Provider), the system must be resilient to transient network failures and API downtime.

### Pattern: Circuit Breaker

- **Problem:** An external service is unavailable. Continuously retrying the connection can waste resources and exacerbate the problem (a "thundering herd").
- **Solution:** All external API clients MUST be wrapped in a **Circuit Breaker** pattern.
  - If calls to an API fail consistently, the circuit "opens," and the application immediately fails all further calls to that API for a configured cool-down period.
  - After the timeout, the circuit moves to a "half-open" state, allowing a single test call through.
  - If the test call succeeds, the circuit "closes" and normal operation resumes. If it fails, the circuit remains open.
- **Implementation:** This can be implemented using an ADK `before_tool_callback` on any tool that makes an external API call.

### Pattern: Exponential Backoff with Jitter

- **Problem:** An API call fails with a transient, retryable error (e.g., HTTP 503). Retrying immediately can lead to repeated, useless calls.
- **Solution:** All retry logic MUST use **exponential backoff with jitter**. The delay between retries will increase exponentially (e.g., 1s, 2s, 4s, 8s), and a small random time ("jitter") is added to prevent multiple instances from retrying at the exact same moment.

## 3. Service Health

### Pattern: Health Check Endpoints

- **Problem:** The agent service might be running but in a non-functional state (e.g., unable to connect to the database).
- **Solution:** Each Cloud Run service MUST expose a `/health` endpoint. This endpoint will perform a quick check of its critical dependencies (e.g., database connectivity). Google Cloud's load balancers and monitoring services will be configured to periodically probe this endpoint to ensure the service is not only running but is fully operational.
