FROM ubuntu:latest
RUN apt-get update && apt-get install python3 pip vim -y
RUN pip install flask
COPY --chmod=777 . /app
WORKDIR /app

ENTRYPOINT [ "python3" ]
CMD ["app.py" ]