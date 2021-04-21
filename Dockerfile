FROM python:3.7.0-alpine
WORKDIR /usr/src/app
COPY requirements.txt main.py ./
RUN pip install --no-cache-dir -r requirements.txt
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--app-dir", "/usr/src/app", "--reload"]
ENTRYPOINT ["uvicorn", "--host", "0.0.0.0", "--port", "8080", "--reload"]
CMD ["main:app"]
