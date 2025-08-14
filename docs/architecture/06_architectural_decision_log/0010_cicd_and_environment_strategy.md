# ADR-010: CI/CD and Environment Strategy

* **Status:** Proposed
* **Date:** 2025-08-04
* **Deciders:** [Your Name], AI Assistant

## Context and Problem Statement

To ensure code quality and enable reliable, repeatable deployments, we need an automated Continuous Integration and Continuous Deployment (CI/CD) pipeline. We also need a clear strategy for managing different environments to test changes safely before they impact live trading with real capital.

## Considered Options

* **Option 1: Manual Deployment:** Manually build and deploy the application components from a developer's machine. This is error-prone, not repeatable, and lacks safety gates.
* **Option 2: Automated CI/CD with GitHub Actions:** Use GitHub's native automation platform to define workflows that automatically test and deploy our code when changes are pushed to specific branches.

## Decision Outcome

**Chosen option:** "Option 2: Automated CI/CD with GitHub Actions", coupled with a two-project Google Cloud setup.

### Positive Consequences

* **Automation & Reliability:** Every push to our main branches will trigger a consistent, automated process for testing and deploying, dramatically reducing human error.
* **Integrated with Source Control:** The pipeline is defined in YAML files (`.github/workflows/`) that live within our `trade-weaver` repository, making our deployment process version-controlled.
* **Safety through Isolation:** We will use separate Google Cloud Projects for a complete and isolated environment for `production` and a second one for `development`. This is a critical safety practice.

### Environment Strategy

* **`develop` branch:** All new features will be merged into this branch. A push to `develop` will trigger a CI/CD workflow that deploys to our `trade-weaver-dev` Google Cloud project.
* **`main` branch:** Only stable, tested code from the `develop` branch will be merged into `main`. A push to `main` will trigger the deployment to the `trade-weaver-prod` project, which handles real capital.
