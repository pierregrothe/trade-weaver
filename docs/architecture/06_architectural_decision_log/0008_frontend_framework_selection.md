# ADR-0008: Front-End Framework Selection

* **Status:** Proposed
* **Date:** 2025-08-04
* **Deciders:** Pierre Grothé, AI Assistant

## Context and Problem Statement

We need to build a modern, real-time web interface (the "Management Cockpit") for users to manage their portfolios, view trade opportunities, and interact with the system. We need to choose a development approach that allows for rapid initial development but is powerful enough for future feature growth.

## Considered Options

* **Option 1: Firebase Studio (Low-Code/Pro-Code):** Use the integrated development environment to quickly build a data-driven UI on top of our Firestore database and Firebase Authentication.
* **Option 2: Custom Front-End Framework (e.g., React, Vue, Svelte):** Build a completely custom front end from scratch, using Firebase as the Backend-as-a-Service (BaaS) for authentication and data.

## Decision Outcome

**Chosen option:** "Option 1: Firebase Studio", for the initial phase of the project.

### Positive Consequences

* **Development Speed:** Firebase Studio is optimized for building dashboards and data-management UIs on top of Firestore. This will allow us to create a functional and secure user cockpit in a fraction of the time it would take with a custom framework.
* **Tight Integration:** It has seamless, out-of-the-box integration with the Firebase services we've already chosen (Auth, Firestore).
* **Low Risk:** Our hybrid architecture decouples the front end from the trading engine. If, in the future, Firebase Studio becomes too limiting for our UI needs (e.g., for highly custom data visualizations), we can replace it with a custom framework without changing the backend.

### Negative Consequences

* We may be limited by the component library and design patterns offered by Studio, potentially restricting highly custom UI/UX features down the line.
