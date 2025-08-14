# CI/CD and Environment Strategy

This document defines the strategy for Continuous Integration, Continuous Deployment (CI/CD), and environment management for the Trade Weaver platform, as decided in ADR-0010.

## 1. CI/CD Pipeline

The project uses an automated CI/CD pipeline built with **GitHub Actions**. This approach ensures that all deployments are reliable, repeatable, and version-controlled.

- **Automation:** Every push to the `develop` and `main` branches triggers a consistent, automated process for testing and deploying, dramatically reducing human error.
- **Infrastructure as Code:** The pipeline is defined in YAML files located in the `.github/workflows/` directory of the repository, making the deployment process itself version-controlled.

## 2. Environment Strategy

A two-tiered environment strategy is used to ensure maximum safety and isolation between development and production workloads.

- **Development Environment (`develop` branch):**
  - **GCP Project:** `trade-weaver-dev`
  - **Trigger:** All new features are merged into the `develop` branch.
  - **Action:** A push to `develop` automatically triggers a CI/CD workflow that deploys the latest version of the application to the development GCP project.

- **Production Environment (`main` branch):**
  - **GCP Project:** `trade-weaver-prod`
  - **Trigger:** Only stable, tested, and reviewed code from the `develop` branch is merged into `main`.
  - **Action:** A push to `main` automatically triggers the deployment workflow to the production GCP project, which is connected to live brokerage accounts and handles real capital.

This separation provides a critical safety gate, ensuring that no code is deployed to production without first being validated in an identical-but-isolated development environment.
