FROM python
RUN apt-get install -qy python3
RUN apt-get install -qy python3-pip
ADD requirements.txt /
ADD MsTokyoBot.py /
RUN pip-3.3 install -r requirements.txt
CMD ["python","MsTokyoBot.py"]
