FROM python:3.8-slim

# Install OS dependencies
RUN apt-get update -y \
    && apt-get install -y build-essential python3-dev busybox vim \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set the application home directory
ENV APP_HOME /opt/app
RUN mkdir -p $APP_HOME
WORKDIR $APP_HOME

# Install poetry
RUN pip install poetry poetry-core>=1.0.2

# Set Python configuration
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install Python dependencies
COPY pyproject.toml $APP_HOME/
COPY poetry.lock $APP_HOME/
RUN poetry install --no-root

# Add all files for the project
COPY . $APP_HOME/

# Expose a port for the server
EXPOSE 8000

# Start the production server
CMD ["bin/start_server"]
