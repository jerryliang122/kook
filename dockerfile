FROM python:3.9.1-slim-buster
WORKDIR /app
COPY . /app
RUN pip install aiohttp khl.py
CMD ["python", "main.py"]