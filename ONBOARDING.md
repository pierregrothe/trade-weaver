# Developer Onboarding Guide

Welcome to the Trade Weaver project! This guide provides a step-by-step process to set up your local development environment on Windows 11 and run your first AI agent.

## Prerequisites

Ensure you have the following software installed:

-   [Git](https://git-scm.com/)
-   [Python 3.10+](https://www.python.org/)
-   [Visual Studio Code](https://code.visualstudio.com/)
-   [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)

## Step 1: Clone the Repository

Open a terminal (Command Prompt or PowerShell) and clone the project repository.

```bash
git clone <repository_url>
cd trade-weaver
```

## Step 2: Set Up the Python Environment

This project uses a dedicated Python virtual environment to manage dependencies.

1.  **Create the virtual environment:**

    ```cmd
    python -m venv .venv
    ```

2.  **Activate the environment.** You must do this every time you open a new terminal to work on the project.

    ```cmd
    .\.venv\Scripts\activate
    ```

3.  **Install dependencies.** (Note: A `requirements.txt` file should be created and maintained at the project root).

    ```cmd
    pip install -r requirements.txt
    ```

## Step 3: Configure Visual Studio Code

1.  Open the project folder in VSCODE: `code .`
2.  VSCODE should automatically detect the virtual environment. If not, open the Command Palette (`Ctrl+Shift+P`) and select **Python: Select Interpreter**, then choose the interpreter from the `./.venv/Scripts` folder.
3.  **Recommended Extensions:** Install the following extensions in VSCODE for an optimal experience:
    -   `ms-python.python` (Python)
    -   `ms-python.vscode-pylance` (Pylance)
    -   `charliermarsh.ruff` (Ruff)

## Step 4: Authenticate with Google Cloud

To allow your local agents to interact with GCP services like Firestore and Secret Manager, you need to set up Application Default Credentials.

```bash
gcloud auth application-default login
```

Follow the prompts in the browser to log in with your Google account.

## Step 5: Your First Agent Run

While Google Jules is the primary tool for code validation and agent testing, you can perform a quick local run from the terminal to verify your setup.

1.  **Ensure your virtual environment is active.**
2.  **Run the `MarketAnalystAgent`:**

    ```cmd
    adk run --agent_path .\pre_market_analysis --input_text "Run a pre-market scan for NASDAQ."
    ```

This command will load the agent from the `pre_market_analysis` package and execute it with your input.

## Onboarding Complete

Your local environment is now fully configured. You can begin development, using Jules for your primary workflow and the local ADK tools for quick iterative testing.

For a deep understanding of the system's design, please review the documents in the `docs/architecture` directory.
