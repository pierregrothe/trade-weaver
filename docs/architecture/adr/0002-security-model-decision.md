# ADR-0002: Security Model for Credentials and User Access

* **Status:** Accepted
* **Date:** 2025-08-04
* **Deciders:** [Your Name], AI Assistant

## Context and Problem Statement

The platform will handle sensitive broker API keys and must enforce strict data isolation between different users and portfolios. We need a secure, industry-standard method for managing credentials and a flexible system for controlling user permissions (Role-Based Access Control - RBAC).

## Considered Options

* **Option 1: Store Credentials in an Encrypted Database:** Store broker API keys in a Firestore collection with field-level encryption managed by the application.
* **Option 2: Use a Dedicated Secrets Management Service:** Utilize Google Secret Manager to store all API keys and other secrets.
* **Option 3: Manage Roles in the Database:** Create `roles` and `permissions` collections in Firestore and write application logic to enforce them.
* **Option 4: Use Integrated Authentication with Custom Claims:** Leverage Firebase Authentication's built-in user management and attach roles directly to a user's ID token using Custom Claims.

## Decision Outcome

**Chosen option:** "Option 2: Use Google Secret Manager" and "Option 4: Use Firebase Authentication with Custom Claims".

### Positive Consequences

* **Superior Security:** Google Secret Manager is a hardened, dedicated service for storing secrets, providing IAM integration, versioning, and audit logging. It is significantly more secure than application-level encryption.
* **Simplified RBAC:** Using Firebase Custom Claims for roles is efficient and secure. The role is part of the user's signed authentication token, which can be verified on the backend. This simplifies the logic in Firestore Security Rules.
* **Scalability:** This model is the standard for building secure, multi-tenant applications on Google Cloud and scales effortlessly.

### Negative Consequences

* There is a minor learning curve for integrating with Secret Manager and setting up custom claims logic.
* Reliance on Google Cloud's IAM and Firebase security models, which is a strategic choice aligned with our overall architecture.
