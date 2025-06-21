# ✅ Base image
FROM python:3.10

# ✅ Set env variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ✅ Set working dir
WORKDIR /app

# ✅ Copy requirements and install
COPY Requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r Requirements.txt

# ✅ Copy all app code
COPY . /app/

# ✅ Expose port
EXPOSE 8000

# ✅ Run Django dev server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
