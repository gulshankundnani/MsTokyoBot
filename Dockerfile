# set base image (host OS)
FROM python:3.8

# set the working directory in the container
WORKDIR /usr/src/app

# copy the dependencies file to the working directory
ADD requirements.txt .
ADD MsTokyoBot.py .

# install dependencies
RUN pip install -r requirements.txt

# command to run on container start
CMD [ "python", "./MsTokyoBot.py" ]
