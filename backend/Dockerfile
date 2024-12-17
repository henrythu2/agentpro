FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install poetry
RUN pip install --no-cache-dir poetry

# Configure poetry
RUN poetry config virtualenvs.create false

# Copy only dependency files first
COPY pyproject.toml poetry.lock ./

# Clean install dependencies
RUN rm -rf /root/.cache/pip && \
    poetry install --no-interaction --no-ansi --no-root --no-cache

# Copy application code
COPY . .

# Clean install project
RUN rm -rf /root/.cache/pip && \
    poetry install --no-interaction --no-ansi --no-cache

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
