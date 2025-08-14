# ADR-0006: Agent Communication (A2A) Pattern

* **Status:** Accepted
* **Date:** 2025-08-04
* **Deciders:** Pierre Grothé, AI Assistant

## Context and Problem Statement

Our multi-agent system requires a mechanism for agents and services to communicate with each other. For example, the daily scheduled scan needs to trigger the `PreMarketScannerAgent` for multiple exchanges. We need a pattern that is reliable, scalable, and fits our event-driven architecture.

## Considered Options

* **Option 1: Direct API Calls (Synchronous):** One service makes a direct HTTPS call to another service's endpoint and waits for a response.
* **Option 2: Asynchronous Messaging via Pub/Sub:** A service publishes a "command" message to a Pub/Sub topic. The target service subscribes to this topic, receives the message, and processes it asynchronously. This is a form of event-driven choreography.
* **Option 3: ADK Hierarchical Control (`sub_agents`):** Use the built-in `sub_agents` and `transfer_to_agent` features of the ADK for tightly-coupled, internal tasks within a single agent's execution flow.

## Decision Outcome

**Chosen option:** A hybrid approach. We will use **"Option 2: Asynchronous Messaging via Pub/Sub"** for our primary, decoupled, event-driven workflows between major system components. We will reserve **"Option 3: ADK Hierarchical Control"** for specific, tightly-coupled tasks within a single, complex agent's internal logic.

### Justification

* **Pub/Sub for Core Workflows:** This pattern is incredibly robust and is the backbone of our system. It provides reliability, scalability, and loose coupling. The pre-market analysis workflow (ADR-0013) is the primary example: Cloud Scheduler triggers a Coordinator via Pub/Sub, which in turn fans-out jobs to the `PreMarketScannerAgent` via a second Pub/Sub topic. This is asynchronous, resilient, and highly scalable.
* **ADK Hierarchy for Internal Tasks:** Inside a complex agent, it may be efficient to have sub-agents for specific sub-tasks. For example, a single `ExecutorAgent` might have a `RiskValidationSubAgent` and an `OrderFormattingSubAgent`. In this case, using ADK's native hierarchical control is simpler and more direct for these internal, synchronous-like workflows that occur within a single invocation.
