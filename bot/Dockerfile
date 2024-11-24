FROM python:3.9-slim

WORKDIR /usr/src/app

COPY . .

RUN pip install --no-cache-dir python-telegram-bot paho-mqtt

CMD ["python", "bot.py"]
