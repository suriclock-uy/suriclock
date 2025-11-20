FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["gunicorn", "QR_Attendance_System.wsgi:application", "--bind", "0.0.0.0:8000"]
