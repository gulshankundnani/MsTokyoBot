FROM python:3
WORKDIR /app
COPY . .
COPY requirements.txt .
RUN pip install -r requirements.txt
CMD ["python","MsTokyoBot.py"]
ENTRYPOINT ["python3"]
