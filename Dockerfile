FROM python
ADD requirements.txt /
ADD MsTokyoBot.py /
RUN pip-3.3 install -r requirements.txt
CMD ["python","MsTokyoBot.py"]
