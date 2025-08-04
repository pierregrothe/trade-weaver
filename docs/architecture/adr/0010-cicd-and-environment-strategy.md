# ADR-0010: CI/CD and Environment Strategy

* **Status:** Proposed
* **Date:** 2025-08-04
* **Deciders:** [Your Name], AI Assistant

## Context and Problem Statement

To ensure code quality and enable reliable, repeatable deployments, we need an automated Continuous Integration and Continuous Deployment (CI/CD) pipeline. We also need a clear strategy for managing different environments (development, staging, production) to test changes safely before they impact live trading.

## Considered Options

* **Option 1: Manual Deployment:** Manually build and deploy the application components (Cloud Run, Firebase) from a developer's machine. This is fast for a single developer but is error-prone and not scalable.
* **Option 2: Automated CI/CD with GitHub Actions:** Use GitHub's native automation platform to define workflows that automatically test and deploy our code when changes are pushed to specific branches.

## Decision Outcome

**Chosen option:** "Option 2: Automated CI/CD with GitHub Actions".

### Positive Consequences

* **Automation & Reliability:** Every push to our main branch can trigger a consistent, automated process for testing and deploying, reducing human error.
* **Integrated with Source Control:** The pipeline is defined in YAML files (`.github/workflows/`) that live within our project repository.
* **Environment Separation:** We will use separate Google Cloud Projects to create a complete and isolated environment for `production` and a second one for `development/staging`. This is a critical best practice for safety. Our GitHub Actions workflow will be configured to deploy to the appropriate project based on the git branch.

### Environment Strategy

* **`develop` branch:** Pushing to this branch will trigger a deployment to our `trade-weaver-dev` Google Cloud project.
* **`main` branch:** Pushing to this branch (typically via a pull request from `develop`) will trigger deployment to the `trade-weaver-prod` project, which handles real capital.
