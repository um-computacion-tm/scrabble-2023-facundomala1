FROM python:3-slim

WORKDIR /scrabble

RUN apt update
#RUN apk add bash

#RUN git clone 

COPY . .

RUN pip install -r requirements.txt

CMD [ "sh", "-c", "coverage run -m unittest && coverage report -m && python -m game.main " ]