# Use the official Python image from the slim-buster variant
FROM python:3.11-slim-buster

# Set environment variables to prevent Python from buffering stdout/stderr and to work within a container
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
ENV PATH="/root/.local/bin:$PATH"

# Copy pyproject.toml and poetry.lock to the working directory
COPY pyproject.toml poetry.lock ./

# Install dependencies using Poetry (without virtual environments)
RUN poetry config virtualenvs.create false && \
    poetry install --no-root

# Copy the Django project into the container
COPY . .


# Run Gunicorn server
CMD ["gunicorn", "config.wsgi", "--reload", "--bind", "0.0.0.0:8000"]
