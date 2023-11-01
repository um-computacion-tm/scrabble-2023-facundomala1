FROM python:3-slim

WORKDIR /scrabble

RUN apk update
RUN apk add git
RUN git clone https://github.com/um-computacion-tm/scrabble-2023-facundomala1.git
WORKDIR /scrabble-2023-facundomala1
RUN git checkout develop
RUN pip install -r requirements.txt 


RUN pip install -r requirements.txt

CMD [ "sh", "-c", "coverage run -m unittest && coverage report -m && python -m game" ]