FROM python:3
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["MsTokyoBot.py"]
ENTRYPOINT ["python3"]
