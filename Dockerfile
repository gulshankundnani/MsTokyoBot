FROM python
ADD requirements.txt /
ADD MsTokyoBot.py /
RUN pip install -r requirements.txt
CMD ["python","MsTokyoBot.py"]
