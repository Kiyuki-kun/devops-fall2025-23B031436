FROM python:3.10

# install cron
RUN apt-get update && apt-get install -y cron

WORKDIR /app
COPY batch.py .
COPY crontab.txt /etc/cron.d/batch-cron

RUN chmod 0644 /etc/cron.d/batch-cron
RUN crontab /etc/cron.d/batch-cron

CMD ["cron", "-f"]
