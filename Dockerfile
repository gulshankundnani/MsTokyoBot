FROM python:3.8.2
EXPOSE 443/udp
EXPOSE 443/tcp
RUN git clone https://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:x-oauth-basic@github.com/gulshankundnani/MsTokyoBot.git
RUN apt-get update
# run this before copying requirements for cache efficiency
RUN pip install --no-cache-dir --upgrade pip setuptools wheel
# Adding requirements file to current directory
# just this file first to cache the pip install step when code changes
COPY requirements.txt .
#install dependencies
RUN pip install -r requirements.txt
COPY MsTokyoBot.py .
# copy code itself from context to image
COPY . .
# run from working directory, and separate args in the json syntax
CMD ["python", "MsTokyoBot.py"]
