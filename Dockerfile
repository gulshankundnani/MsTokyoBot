FROM python:3
WORKDIR /usr/src/app
COPY . .
CMD ["MsTokyoBot.py"]
ENTRYPOINT ["python3"]
