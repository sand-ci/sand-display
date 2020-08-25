FROM python:alpine

#MAINTANER Derek Weitzel "dweitzel@unl.edu"

COPY ./requirements.txt /app/requirements.txt
WORKDIR /app

RUN pip install -r requirements.txt

COPY src /app/src
ENV PYTHONPATH=/app/src

ENTRYPOINT [ "python" ]

CMD [ "src/sand_display/app.py" ]