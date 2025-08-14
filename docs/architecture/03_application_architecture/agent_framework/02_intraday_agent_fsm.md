# Intraday Agent Finite State Machine (FSM)

This document describes the architecture for the core of the intraday trading agent, which is designed as a **Hierarchical State Machine (HSM)**. This approach provides a formal, resilient, and modular framework for managing the agent's lifecycle and its response to market and system events. This design was decided in ADR-0016.

## 1. Rationale

The agent requires a robust, deterministic, and auditable logical structure to manage its operations throughout the trading day. It must handle a variety of asynchronous events—market data, broker confirmations, time-based triggers—without entering a compromised or undefined state. A simple linear script or a monolithic block of conditional statements is insufficient to handle this complexity and is prone to catastrophic failure.

The FSM does not run in a loop but reacts to a stream of events from the event bus (GCP Pub/Sub), decoupling the agent's logic from the event producers.

## 2. High-Level State Model

The agent's lifecycle is defined by a set of high-level operational states. The agent can only be in one state at any given time, and transitions are triggered by specific, well-defined events as defined in the `02_integration_and_messaging.md` document.

| State | Description | Key Responsibilities |
| :--- | :--- | :--- |
| `INITIALIZING` | Agent startup and setup. Inert, no connections. | Load configurations, API keys, risk limits. Initialize logging. |
| `AWAITING_MARKET_OPEN` | Pre-market readiness. Connected but no trading. | Monitor pre-market data, warm up indicators, perform health checks. |
| `MONITORING_WATCHLIST` | Primary search mode during market hours with no open positions. | Consume real-time data, run signal generation logic. |
| `ENTERING_POSITION` | Transient state to open a new position. | Perform pre-trade risk checks, construct and submit the order. |
| `MANAGING_POSITION` | Actively managing an open position. **This is a superstate (HSM).** | Monitor P&L, track against stop-loss/take-profit, evaluate exit conditions. |
| `EXITING_POSITION` | Transient state to close an existing position. | Construct and submit the closing order. |
| `LIQUIDATING_POSITIONS` | End-of-day risk management. | Cancel all open orders and flatten any existing positions. |
| `AWAITING_MARKET_CLOSE`| Post-liquidation, waiting for the session to end. | Read-only data monitoring. All trading is disabled. |
| `POST_TRADE_PROCESSING` | End-of-day bookkeeping and reporting. | Reconcile trades, calculate P&L, generate reports. |
| `SYSTEM_FAILURE` | Critical safe mode upon unrecoverable error. | Halt all trading, cancel all orders, alert human operator. |

## 3. Hierarchical State Machine (HSM) for Position Management

To manage the complexity of an open trade, the `MANAGING_POSITION` state is not a single state but a **superstate** containing its own nested FSM. This allows for modular and reusable trade management logic (e.g., different trailing stop algorithms) to be plugged in as needed.

-   **Superstate: `MANAGING_POSITION`**
    -   **Inherited Transitions:** Defines global exit conditions (e.g., `RISK_LIMIT_BREACH_EVENT` -> `EXITING_POSITION`).
    -   **Substates:**
        -   `INITIAL_RISK`: Manages the initial, fixed stop-loss and profit targets.
        -   `TRAILING_STOP`: Entered after a significant favorable move; dynamically adjusts the stop-loss.
        -   `SCALING_OUT`: Manages partial profit-taking at multiple predefined targets.

## 4. Implementation

-   **Recommended Library:** The recommended Python library for implementation is **`python-statemachine`** due to its strictness, correctness guarantees, and native `asyncio` support, which is ideal for this application.
