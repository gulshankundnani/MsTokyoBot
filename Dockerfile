FROM python
ADD requirements.txt /
ADD MsTokyoBot.py /
RUN pip3 install --no-cache-dir -r requirements.txt
CMD ["python","MsTokyoBot.py"]
