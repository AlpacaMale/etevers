FROM python:3.9
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
CMD ["uwsgi", "--http", ":5000", "--workers", "2", "--threads", "10", "--master", "--vacuum", "--enable-threads", "-w", "run:app"]
