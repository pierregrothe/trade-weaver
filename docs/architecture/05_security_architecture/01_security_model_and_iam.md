# Security Model and Identity & Access Management (IAM)

This document defines the security model for managing credentials and controlling user access, as decided in ADR-0002. The platform handles sensitive data, including broker API keys, and must enforce strict security controls.

## 1. Credential and Secret Management

To ensure the highest level of security for sensitive information, the platform uses a dedicated, hardened secret management service.

-   **Technology:** **Google Secret Manager**.
-   **Scope:** All secrets, including broker API keys, database credentials, and third-party API keys, MUST be stored in Google Secret Manager.
-   **Rationale:** Storing secrets in a dedicated service is significantly more secure than application-level encryption in a database. Secret Manager provides fine-grained access control via IAM, versioning, and a complete audit trail of when secrets are accessed.
-   **Access:** Cloud Run services are granted access to specific secrets via their IAM service account, adhering to the principle of least privilege.

## 2. User Authentication

User identity is managed by Firebase Authentication.

-   **Technology:** **Firebase Authentication**.
-   **Function:** It handles all aspects of the user authentication lifecycle, including sign-up, sign-in, and password management, providing a secure and scalable solution.

## 3. User Authorization (Role-Based Access Control - RBAC)

To control what authenticated users are allowed to do, the platform uses an integrated RBAC model.

-   **Technology:** **Firebase Authentication Custom Claims**.
-   **Implementation:** User roles (e.g., `Admin`, `Trader`, `Viewer`) are attached directly to a user's ID token as custom claims.
-   **Enforcement:**
    -   **Backend:** The user's role is passed in the signed authentication token with every request. Backend services (Cloud Functions, Cloud Run) verify the token and check the role claim before performing any action.
    -   **Database:** Firestore Security Rules are used to enforce access control based on the roles present in the user's token.
-   **Rationale:** This approach is highly efficient and secure. It simplifies the authorization logic in the backend and database rules, as the user's role is part of a cryptographically signed, verifiable token.
