
FROM python:3.8.2

RUN git clone https://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:x-oauth-basic@github.com/gulshankundnani/MsTokyoBot.git
# run this before copying requirements for cache efficiency
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools wheel googletrans
#set work directory early so remaining paths can be relative
WORKDIR /app

# Adding requirements file to current directory
# just this file first to cache the pip install step when code changes
COPY requirements.txt .
COPY MsTokyoBot.py .
COPY aiml .

#install dependencies
RUN pip install -r requirements.txt

# copy code itself from context to image
COPY . .


# run from working directory, and separate args in the json syntax
CMD ["python", "./MsTokyoBot.py"]
