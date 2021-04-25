FROM python:latest

WORKDIR /usr/local/bin

COPY MsTokyoBot.py .

CMD ["MsTokyoBot.py"]
