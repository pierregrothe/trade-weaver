# ADR-0015: Agent Configuration Management and Validation

* **Status:** Proposed
* **Date:** 2025-08-12
* **Deciders:** Pierre Grothé, Tommy (AI Assistant)

## Context and Problem Statement

The trading agent's behavior is heavily dependent on a complex set of parameters stored in the `AgentConfigurations` and `Strategies` Firestore collections. A single incorrect change to a risk parameter, strategy setting, or model threshold could lead to significant financial loss. We need a robust, auditable, and safe process for managing and deploying these configuration changes that balances the need for agility with the requirement for absolute control.

## Decision Outcome

**Chosen option:** We will adopt a formalized, CI/CD-based **Configuration Validation Lifecycle**. All configuration changes will be managed through a Git workflow (Infrastructure as Code) and subjected to a multi-stage, automated **Pre-Deployment Validation Gauntlet** before being applied to the live production environment. This approach treats configuration changes with the same rigor as code changes.

### The Unified Configuration Validation Lifecycle

1. **Initiation (Request for Change):** A developer proposes a change by creating a pull request against a version-controlled repository containing the configuration files (e.g., in JSON or YAML format).
2. **Static Validation:** The CI/CD pipeline automatically triggers static analysis to check for syntax errors, schema violations, and basic rule validation (e.g., ensuring a percentage is between 0 and 100).
3. **Peer & Risk Review (Four-Eyes Principle):** The pull request must be reviewed and approved by at least one other qualified team member. Changes to critical risk parameters must also receive a formal, auditable sign-off from a designated risk manager.
4. **Automated Impact Analysis (The Gauntlet):** Upon approval, the pipeline executes a series of automated tests:
    * **Automated Backtesting:** A comparative backtest is run using the new configuration against the old one on recent historical data (e.g., last 90 days). The system generates a report showing the delta in P&L, Sharpe Ratio, and Maximum Drawdown.
    * **"What-If" Scenario Analysis:** The new configuration is tested against a set of predefined scenarios (e.g., market volatility +50%, correlation breakdowns) to assess its robustness.
5. **Live Simulation (Paper Trading):** If the gauntlet is passed, the configuration is deployed to a live paper trading environment to validate its end-to-end performance with real market data but without risking capital.
6. **Deployment:** After a successful simulation and final business sign-off, the change is deployed to production.

### Positive Consequences

* **Safety & Stability:** Drastically reduces the risk of deploying a misconfigured or unprofitable parameter set.
* **Auditability:** Creates an immutable, Git-based audit trail of every proposed, reviewed, and deployed configuration change.
* **Agility with Control:** Allows for rapid iteration on strategy parameters while maintaining rigorous, automated safety checks.

### Negative Consequences

* **Increased Overhead:** This process is more complex than manual changes in a database console.
* **Infrastructure Cost:** Requires a dedicated CI/CD pipeline and a robust backtesting environment.
