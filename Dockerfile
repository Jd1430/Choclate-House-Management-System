FROM python
WORKDIR /app
COPY . .
CMD ["python", "app.py"]
