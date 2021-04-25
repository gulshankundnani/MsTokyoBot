FROM python:3

ADD MsTokyoBot.py /

RUN pip install -r requirements.txt

CMD [ "python", "./MsTokyoBot.py" ]
