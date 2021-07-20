

FROM python:3.8.2
EXPOSE 3000
RUN docker run -p z4adf28f0-gtw.qovery.io:3000
RUN git clone https://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:x-oauth-basic@github.com/gulshankundnani/MsTokyoBot.git
# run this before copying requirements for cache efficiency
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir --upgrade setuptools wheel
# Adding requirements file to current directory
# just this file first to cache the pip install step when code changes
COPY requirements.txt .
#install dependencies
RUN pip install --no-cache-dir -r requirements.txt
COPY MsTokyoBot.py .
# copy code itself from context to image
COPY . .
# run from working directory, and separate args in the json syntax
CMD ["python", "MsTokyoBot.py",host='z4adf28f0-gtw.qovery.io',port=3000]
