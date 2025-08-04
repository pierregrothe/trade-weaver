# ADR-0006: Agent Communication (A2A) Pattern

* **Status:** Proposed
* **Date:** 2025-08-04
* **Deciders:** [Your Name], AI Assistant

## Context and Problem Statement

Our multi-agent system requires a mechanism for agents to communicate with each other. For example, the `SchedulerAgent` needs to trigger the `AnalyzerAgent`, and user actions need to trigger the `ExecutorAgent`. We need a pattern that is reliable, scalable, and fits our event-driven architecture.

## Considered Options

* **Option 1: Direct API Calls (Synchronous):** One agent (or a Cloud Function) makes a direct HTTPS call to another agent's service endpoint and waits for a response.
* **Option 2: Database as a Message Queue (Firestore-Triggered):** An agent writes a "command" document to a specific Firestore collection. A Cloud Function, triggered by this write, invokes the target agent.
* **Option 3: ADK Direct Delegation:** Use the built-in `sub_agents` and `transfer_to_agent` features of the ADK for tightly-coupled, hierarchical tasks.

## Decision Outcome

**Chosen option:** A hybrid approach. We will use **"Option 2: Database as a Message Queue"** for our primary, asynchronous, event-driven workflows between the main system components. We will reserve **"Option 3: ADK Direct Delegation"** for specific, tightly-coupled tasks within a single, complex agent's internal logic.

### Justification

* **Firestore-Triggered for Core Workflow:** This pattern is incredibly robust and fits perfectly with our chosen stack. When the UI writes a `trade_request`, a Cloud Function is triggered which then invokes the `ExecutorAgent`. This is asynchronous, reliable, and decouples our core components beautifully. It's the backbone of our system.
* **ADK Delegation for Internal Tasks:** Inside a complex agent, it might make sense to have sub-agents for specific sub-tasks. For example, an `AnalyzerAgent` might have a `DataFetchingSubAgent` and a `PatternRecognitionSubAgent`. In this case, using ADK's native delegation is simpler and more direct for these internal, synchronous-like workflows.
