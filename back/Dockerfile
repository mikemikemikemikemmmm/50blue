FROM python:3.12-alpine
WORKDIR /app
COPY pyproject.toml poetry.lock* ./
RUN pip install poetry==1.8.3 &&\
    poetry export -f requirements.txt --output requirements.txt --without-hashes &&\
    pip install --no-cache-dir -r requirements.txt
COPY ./ ./
EXPOSE 8000
CMD ["python", "run.py","--prod"]