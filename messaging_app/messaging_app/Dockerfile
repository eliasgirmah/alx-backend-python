# Install Python
FROM python:3.10

WORKDIR /messaging_app

COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Expose the Django Port
EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]