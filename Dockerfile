FROM python:3.13.3

RUN pip install pandas dotenv schedule
COPY . /home
