# Start from the official Python 3.11 dev container image.
FROM mcr.microsoft.com/devcontainers/python:3.13

# Switch to the root user to install new software packages.
USER root

# === INSTALL SYSTEM DEPENDENCIES ===

# 1. Install prerequisites for gcloud and Node.js.
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
        apt-transport-https \
        ca-certificates \
        gnupg \
        curl \
    && rm -rf /var/lib/apt/lists/* 

# 2. Add Node.js v20 repository and install it.
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs

# 3. Add the Google Cloud SDK repository and install the gcloud CLI.
RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg \
    && echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list \
    && apt-get update && apt-get install -y google-cloud-sdk

# 4. Install 'uv' for Python dependency management.
RUN pip install --upgrade pip
RUN pip install uv==0.6.12

# Copy only the pyproject.toml to leverage Docker layer caching.
# If this file doesn't change, Docker won't re-run the installation.
COPY --chown=vscode:vscode pyproject.toml .

# Install all dependencies from pyproject.toml using uv.
# This installs the main dependencies PLUS the [dev] optional group.
RUN uv pip install --system .[dev]

# === SWITCH TO NON-ROOT USER (for security) ===
# Now that all installations are done, switch to the non-privileged user.
# The rest of the code (mounted by VS Code) will be run by this user.
USER vscode