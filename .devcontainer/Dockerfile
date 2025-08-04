# Use an official Python runtime as a parent image
FROM mcr.microsoft.com/devcontainers/python:3.13

# Switch to the root user to install new software packages.
USER root

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y     build-essential     curl     git     && rm -rf /var/lib/apt/lists/*

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.cargo/bin:${PATH}"

# Copy the project requirements file
COPY pyproject.toml ./

# Install project dependencies using uv
RUN uv pip install --system -r pyproject.toml

# Copy the rest of the application code
COPY . .

# Switch back to the non-root 'vscode' user for security.
USER vscode

# Command to run when the container starts
CMD ["tail", "-f", "/dev/null"]
