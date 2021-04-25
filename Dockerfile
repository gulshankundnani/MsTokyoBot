FROM python:3
WORKDIR /app
COPY . .
CMD ["MsTokyoBot.py"]
ENTRYPOINT ["python3"]
