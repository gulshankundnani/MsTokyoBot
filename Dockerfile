FROM python
MAINTAINER Gulshan
RUN apt-get update
RUN apt-get install -y python
WORKDIR /app
COPY . .
CMD ["/app/MsTokyoBot.py"]
ENTRYPOINT ["python"]
