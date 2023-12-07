FROM python:3.10 as build-stage

WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /app

# Install Poetry
RUN pip install poetry

# Copy pyproject.toml and poetry.lock (if available)
COPY pyproject.toml poetry.lock* /app/

# Install dependencies without dev dependencies
RUN poetry config virtualenvs.create false
RUN poetry install 

# Copy the entire application
COPY app /app/app

# Copy test code
COPY tests /app/tests

# Install all dependencies including dev dependencies for running tests
RUN poetry install

# Run the tests
RUN pytest ./tests

# Final Stage: Building the application
FROM python:3.10-slim as build-release-stage

WORKDIR /app

# Copy installed dependencies from the build stage
COPY --from=build-stage /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=build-stage /usr/local/bin /usr/local/bin
COPY --from=build-stage /app /app

EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]