# Agent Evaluation Methodology

This document defines the methodology for evaluating the performance and correctness of AI agents using the Google ADK's native evaluation tool, `adk eval`. This process is critical for iterating on agent design and ensuring they behave as expected.

## 1. The `adk eval` Framework

`adk eval` runs an agent against a predefined set of test cases (an "evaluation set") and compares the agent's actual output to an expected "golden" output. This allows for automated, repeatable testing of an agent's behavior.

## 2. The Golden Dataset

To evaluate our agents, we will create and maintain a **Golden Dataset**, which will be a collection of `eval_set.jsonl` files. Each file will contain a series of test cases representing different scenarios the agent might encounter.

-   **Location:** `tests/evaluation/`
-   **Scenarios:** We will create separate evaluation sets for different market regimes and use cases, for example:
    -   `eval_set_trending_market.jsonl`
    -   `eval_set_volatile_market.jsonl`
    -   `eval_set_invalid_inputs.jsonl`

### Evaluation Set Example (`eval_set.jsonl`)

Each line in the file is a JSON object representing one test case. For the `ExecutionAgent`, a test case would involve providing a `MarketAnalysisReport` as input and defining the expected tool call as the output.

```json
{"input": {"report_id": "...", "exchange_reports": [{"exchange_id": "NASDAQ", "market_regime": {"vix_value": 15.5, "adx_value": 28.9}, "observed_instruments": [{"ticker": "ACME", "gapper_data": {"gap_percent": 5.0}, "catalyst_analysis": {"primary_catalyst_type": "Earnings Beat"}, "..."}]}]}}, "output": {"tool_code": "print(default_api.execute_trade(symbol='ACME', strategy='ORB_v1', direction='LONG'))"}}
{"input": {"report_id": "...", "exchange_reports": [{"exchange_id": "NASDAQ", "market_regime": {"vix_value": 38.0, "adx_value": 15.0}, "observed_instruments": [{"ticker": "ZYX", "..."}]}]}, "output": {"text": "No trade signal generated due to high volatility and ranging market."}}
```

## 3. Evaluation Metrics

We will track the following key metrics from the `adk eval` output:

1.  **Task Completion Rate:** What percentage of test cases completed successfully without errors?
2.  **Tool Call Accuracy:** For cases that expected a tool call, did the agent call the *correct* tool with the *exact* correct parameters?
3.  **Output Accuracy:** For cases that expected a text response, how closely did the agent's response match the golden output?
4.  **Safety & Compliance:** For test cases involving invalid or dangerous inputs (e.g., a trade that should be blocked by the Risk Governor), did the agent correctly refuse to act? This is measured by comparing the agent's output to a golden response that expects a rejection.

## 4. CI/CD Integration

The `adk eval` process will be integrated into the CI/CD pipeline. Every pull request that modifies an agent's logic MUST pass the full evaluation suite before it can be merged into the `develop` branch. This ensures that no change is introduced that causes a regression in agent behavior.
