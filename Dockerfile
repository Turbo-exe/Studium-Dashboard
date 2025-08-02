FROM python:3.13.3-slim

ENV PYTHONUNBUFFERED=1
ENV SQLITE_PATH="/data/db"

WORKDIR /usr/local/study-dashboard
COPY . .

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev \
    locales \
    && rm -rf /var/lib/apt/lists/*

# Set the locale (english and german)
RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    sed -i -e 's/# de_DE.UTF-8 UTF-8/de_DE.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Setup database
RUN mkdir -p ${SQLITE_PATH}
RUN python manage.py migrate --noinput
RUN python manage.py prefill_database # This step is only for the prototype to have some data for evaluation purposes

# Expose port 8000
EXPOSE 8000

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
