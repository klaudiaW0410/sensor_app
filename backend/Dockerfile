FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
#  Installing packages from requirements.txt and upgrading pip
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . .

#  Exposing port 8000 for the Django development server
EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
