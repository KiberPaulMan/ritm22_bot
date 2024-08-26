FROM python:3.11.2-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN mkdir -p /mnt/win_share
RUN apt-get update && apt-get -y install samba cifs-utils bash nano

WORKDIR /telegram_bot

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r ./requirements.txt

COPY . .

CMD ["python", "-m", "app"]