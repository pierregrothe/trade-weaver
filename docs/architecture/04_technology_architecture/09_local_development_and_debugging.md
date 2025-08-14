# Local Development and Debugging Workflow

This document provides a practical guide for developers to run, debug, and test their agents locally using the Google ADK's command-line interface (CLI) tools. A robust local testing loop is essential for rapid, iterative development.

## 1. The Local Testing Toolkit

The ADK provides three primary tools for local agent interaction:

-   **`adk run`**: For direct command-line interaction.
-   **`adk web`**: For interactive testing in a simple web UI.
-   **`adk api_server`**: For exposing the agent as a REST API for programmatic testing (e.g., with Postman).

## 2. `adk run`: Command-Line Interaction

This is the quickest way to test an agent's response to a single input.

-   **Use Case:** Quickly verifying a change to an agent's logic or a tool's functionality from the terminal.
-   **Example Command:**

    ```bash
    # Run the MarketAnalystAgent with a simple text input
    adk run --agent_path ./pre_market_analysis --input_text "Analyze the NASDAQ and TSX exchanges for pre-market opportunities."
    ```

## 3. `adk web`: Interactive Web UI

This command launches a local, browser-based chat interface for more interactive and conversational testing.

-   **Use Case:** Debugging conversational flows, demonstrating an agent's capabilities, or for developers who prefer a GUI.
-   **Example Command:**

    ```bash
    # Launch the web UI for the ExecutionAgent
    adk web --agent_path ./execution_agent
    ```

## 4. `adk api_server`: REST API for Programmatic Testing

This is the most powerful tool for local testing, as it exposes the agent via a standard REST API, allowing for integration with tools like Postman or automated test scripts.

-   **Use Case:** Testing the agent's response to complex JSON inputs (like a `MarketAnalysisReport`) or integrating the agent into a local integration test suite.
-   **Example Command:**

    ```bash
    # Start the API server for the ExecutionAgent on the default port
    adk api_server --agent_path ./execution_agent
    ```

### Testing with Postman

Once the API server is running, you can interact with it using any API client. To test the `ExecutionAgent`, you would configure Postman as follows:

1.  **URL:** `POST http://127.0.0.1:8080/:run`
2.  **Headers:** `Content-Type: application/json`
3.  **Body (Raw JSON):**

    ```json
    {
        "input": {
            "files": [
                {
                    "path": "path/to/your/test_market_analysis_report.json",
                    "content_type": "application/json"
                }
            ]
        },
        "state": {
            "account.capital": 50000,
            "account.max_risk_per_trade": 0.01
        }
    }
    ```

This allows for precise, repeatable testing of how the agent processes complex, structured data inputs and makes decisions based on a given state.
