FROM python
RUN apt-get -y upgrade
RUN aapt-get install -y python3.8
RUN pip install --no-cache-dir --upgrade pip
ADD requirements.txt /
ADD MsTokyoBot.py /
RUN pip-3.3 install -r requirements.txt
CMD ["python","MsTokyoBot.py"]
