FROM python:3.13.3

RUN pip install pandas dotenv schedule
RUN apt install nano
COPY . /home
